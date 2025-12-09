"""
Session Manager for ADK Agents

Manages short-term working memory for active conversations,
following production security and performance best practices.
"""

import asyncio
import json
import re
import uuid
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional
from dataclasses import dataclass
from enum import Enum

# Import PII detection utility
from .pii_detection import PiiDetector


class SessionStatus(Enum):
    """Status of a session."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    ARCHIVED = "archived"


@dataclass
class Message:
    """Represents a single message in the conversation history."""
    id: str
    role: str  # 'user', 'assistant', 'system', 'tool'
    content: str
    timestamp: datetime
    tool_calls: Optional[List[Dict]] = None
    tool_responses: Optional[List[Dict]] = None

    def to_dict(self):
        """Convert to dictionary for storage/serialization."""
        return {
            'id': self.id,
            'role': self.role,
            'content': self.content,
            'timestamp': self.timestamp.isoformat(),
            'tool_calls': self.tool_calls,
            'tool_responses': self.tool_responses
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Create Message instance from dictionary."""
        data['timestamp'] = datetime.fromisoformat(data['timestamp'])
        return cls(**data)


@dataclass
class Session:
    """Represents a single conversation session."""
    id: str
    user_id: str
    created_at: datetime
    last_accessed: datetime
    status: SessionStatus
    history: List[Message]
    metadata: Dict[str, Any]  # Additional session data

    def to_dict(self):
        """Convert to dictionary for storage/serialization."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat(),
            'last_accessed': self.last_accessed.isoformat(),
            'status': self.status.value,
            'history': [msg.to_dict() for msg in self.history],
            'metadata': self.metadata
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Create Session instance from dictionary."""
        data['created_at'] = datetime.fromisoformat(data['created_at'])
        data['last_accessed'] = datetime.fromisoformat(data['last_accessed'])
        data['status'] = SessionStatus(data['status'])
        data['history'] = [Message.from_dict(msg) for msg in data['history']]
        return cls(**data)


class SessionManager:
    """Manages session data for ADK agents with security and performance optimizations."""
    
    def __init__(self, storage_client=None, max_token_limit: int = 3000, ttl_days: int = 7):
        """
        Initialize the session manager.
        
        Args:
            storage_client: Client for session storage (e.g., Redis, database)
            max_token_limit: Maximum tokens allowed in session history
            ttl_days: Time-to-live for inactive sessions (in days)
        """
        self.storage = storage_client
        self.max_token_limit = max_token_limit
        self.ttl_days = ttl_days
        self.pii_detector = PiiDetector()
        self._cache = {}  # In-memory cache for active sessions

    async def create_session(self, user_id: str, initial_context: str = "") -> Session:
        """Create a new session with initial context."""
        session_id = f"session_{uuid.uuid4()}"
        
        # Create initial system message if context provided
        initial_messages = []
        if initial_context:
            initial_messages.append(Message(
                id=f"msg_{uuid.uuid4()}",
                role="system",
                content=initial_context,
                timestamp=datetime.now()
            ))
        
        session = Session(
            id=session_id,
            user_id=user_id,
            created_at=datetime.now(),
            last_accessed=datetime.now(),
            status=SessionStatus.ACTIVE,
            history=initial_messages,
            metadata={}
        )
        
        # Store session
        await self._store_session(session)
        
        # Update cache
        self._cache[session_id] = session
        
        return session

    async def get_session(self, session_id: str, user_id: str) -> Optional[Session]:
        """Get a session, validating user access."""
        # Check cache first
        if session_id in self._cache:
            session = self._cache[session_id]
            if session.user_id == user_id and session.status == SessionStatus.ACTIVE:
                return session
        
        # Fetch from storage
        session = await self._fetch_session_from_storage(session_id)
        
        # Verify access and status
        if session and session.user_id == user_id and session.status == SessionStatus.ACTIVE:
            # Update last accessed time
            session.last_accessed = datetime.now()
            
            # Update cache
            self._cache[session_id] = session
            
            # Update storage in background (non-blocking)
            asyncio.create_task(self._store_session(session))
            
            return session
        
        return None

    async def add_message(self, session_id: str, user_id: str, message: Message) -> bool:
        """Add a message to a session after applying security measures."""
        session = await self.get_session(session_id, user_id)
        if not session:
            return False
        
        # Apply PII redaction before storing
        redacted_message = await self._redact_pii(message)
        
        # Apply context window management
        session.history.append(redacted_message)
        await self._manage_context_window(session)
        
        # Update session metadata
        session.last_accessed = datetime.now()
        session.metadata['message_count'] = session.metadata.get('message_count', 0) + 1
        
        # Store updated session
        await self._store_session(session)
        
        # Update cache
        self._cache[session_id] = session
        
        return True

    async def get_session_history(
        self, 
        session_id: str, 
        user_id: str, 
        max_messages: Optional[int] = None
    ) -> List[Message]:
        """Retrieve session history with security and optimization."""
        session = await self.get_session(session_id, user_id)
        if not session:
            return []
        
        # Return history, optionally limited
        history = session.history
        if max_messages:
            history = history[-max_messages:]
        
        return history

    async def end_session(self, session_id: str, user_id: str) -> bool:
        """End a session and mark it as inactive."""
        session = await self.get_session(session_id, user_id)
        if not session:
            return False
        
        session.status = SessionStatus.INACTIVE
        session.last_accessed = datetime.now()
        
        # Store updated session
        success = await self._store_session(session)
        
        # Remove from cache
        if session_id in self._cache:
            del self._cache[session_id]
        
        return success

    async def cleanup_expired_sessions(self) -> int:
        """Clean up expired sessions based on TTL policy."""
        cutoff_time = datetime.now() - timedelta(days=self.ttl_days)
        
        expired_sessions = await self._find_expired_sessions(cutoff_time)
        cleaned_count = 0
        
        for session_id in expired_sessions:
            try:
                await self._archive_session(session_id)
                cleaned_count += 1
            except Exception as e:
                print(f"Failed to clean up session {session_id}: {str(e)}")
        
        return cleaned_count

    async def _redact_pii(self, message: Message) -> Message:
        """Apply PII redaction to a message."""
        redacted_content = self.pii_detector.redact(message.content)
        message.content = redacted_content
        return message

    async def _manage_context_window(self, session: Session):
        """Manage the context window to stay within token limits."""
        # Strategy 1: Token-based truncation
        current_tokens = await self._estimate_tokens(session.history)
        
        if current_tokens > self.max_token_limit:
            # Keep recent messages but remove oldest ones
            session.history = await self._truncate_history(session.history, self.max_token_limit)
        
        # Strategy 2: Recursive summarization (could be done in background)
        # TODO: Implement recursive summarization as a background task
        # when conversation gets very long

    async def _estimate_tokens(self, messages: List[Message]) -> int:
        """Estimate the number of tokens in a list of messages."""
        # This is a rough estimation - 1 token is roughly 4 characters
        total_chars = sum(len(msg.content) for msg in messages)
        return total_chars // 4

    async def _truncate_history(self, history: List[Message], max_tokens: int) -> List[Message]:
        """Truncate history to fit within token limits."""
        # Always keep system messages and the most recent messages
        system_messages = [msg for msg in history if msg.role == 'system']
        
        # Get non-system messages
        non_system = [msg for msg in history if msg.role != 'system']
        
        if len(non_system) <= 1:  # Only system message and current one
            return history
        
        # Keep the most recent messages that fit within the limit
        # First, estimate tokens for system messages
        system_tokens = await self._estimate_tokens(system_messages)
        remaining_tokens = max_tokens - system_tokens
        
        # Start from the most recent and add backwards until we exceed the limit
        truncated_history = system_messages[:]  # Start with system messages
        current_tokens = system_tokens
        
        # Add messages from the end (most recent) backwards
        for i in range(len(non_system) - 1, -1, -1):
            msg = non_system[i]
            msg_tokens = await self._estimate_tokens([msg])
            
            if current_tokens + msg_tokens <= remaining_tokens:
                truncated_history.append(msg)
                current_tokens += msg_tokens
            else:
                break
        
        # Reverse the non-system messages to maintain chronological order
        non_system_keep = [msg for msg in reversed(truncated_history) if msg.role != 'system']
        system_keep = [msg for msg in truncated_history if msg.role == 'system']
        
        return system_keep + non_system_keep

    async def _store_session(self, session: Session) -> bool:
        """Store session in the configured storage backend."""
        try:
            # In a real implementation, this would store to database or Redis
            # Here we'll implement a simple file-based storage for demonstration
            if self.storage:
                # Store to configured backend
                await self.storage.set(session.id, session.to_dict())
            else:
                # Fallback to file storage for demonstration
                with open(f"sessions/{session.id}.json", "w") as f:
                    json.dump(session.to_dict(), f)
            
            return True
        except Exception as e:
            print(f"Error storing session {session.id}: {str(e)}")
            return False

    async def _fetch_session_from_storage(self, session_id: str) -> Optional[Session]:
        """Fetch session from storage."""
        try:
            # In a real implementation, this would fetch from database or Redis
            if self.storage:
                session_data = await self.storage.get(session_id)
                if session_data:
                    return Session.from_dict(session_data)
            else:
                # Fallback to file storage for demonstration
                try:
                    with open(f"sessions/{session_id}.json", "r") as f:
                        session_data = json.load(f)
                        return Session.from_dict(session_data)
                except FileNotFoundError:
                    return None
            
            return None
        except Exception as e:
            print(f"Error fetching session {session_id}: {str(e)}")
            return None

    async def _find_expired_sessions(self, cutoff_time: datetime) -> List[str]:
        """Find session IDs that have expired."""
        # In a real implementation, this would query the database
        # For now, return an empty list
        return []

    async def _archive_session(self, session_id: str) -> bool:
        """Archive an expired session."""
        # In a real implementation, this would move the session to archive storage
        # For now, just return True
        return True


# PII Detection utility
class PiiDetector:
    """Simple utility for detecting and redacting PII."""
    
    def __init__(self):
        # Common patterns for PII
        self.patterns = [
            # Email addresses
            (r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL]'),
            # Phone numbers
            (r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', '[PHONE]'),
            # Credit card numbers
            (r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b', '[CREDIT_CARD]'),
            # SSN
            (r'\b\d{3}-\d{2}-\d{4}\b', '[SSN]'),
            # IP addresses
            (r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', '[IP_ADDRESS]'),
        ]
    
    def redact(self, text: str) -> str:
        """Redact PII from text."""
        result = text
        for pattern, replacement in self.patterns:
            result = re.sub(pattern, replacement, result)
        return result


# Singleton instance for use in agents
session_manager = SessionManager()