"""
Memory Manager Service for ADK Agents

This service handles the storage, retrieval, and consolidation of long-term memories
for production-grade AI agents, following context engineering best practices.
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum

logger = logging.getLogger(__name__)


class MemoryType(Enum):
    """Types of memories to support different use cases."""
    DECLARATIVE = "declarative"  # Factual knowledge ("knowing what")
    PROCEDURAL = "procedural"    # Process knowledge ("knowing how")


@dataclass
class Memory:
    """Represents a single memory entry with metadata."""
    id: str
    user_id: str
    content: str
    memory_type: MemoryType
    importance: float  # 0.0 to 1.0, how important is this memory
    created_at: datetime
    last_accessed: datetime
    provenance: str   # Source of this memory
    tags: List[str] = None
    related_memories: List[str] = None  # IDs of related memories

    def to_dict(self):
        """Convert to dictionary for storage/serialization."""
        result = asdict(self)
        result['memory_type'] = self.memory_type.value
        result['created_at'] = self.created_at.isoformat()
        result['last_accessed'] = self.last_accessed.isoformat()
        return result

    @classmethod
    def from_dict(cls, data: dict):
        """Create Memory instance from dictionary."""
        data['memory_type'] = MemoryType(data['memory_type'])
        data['created_at'] = datetime.fromisoformat(data['created_at'])
        data['last_accessed'] = datetime.fromisoformat(data['last_accessed'])
        return cls(**data)


class MemoryManager:
    """A decoupled memory service for ADK agents."""
    
    def __init__(self, vector_store_client=None, knowledge_graph_client=None):
        """
        Initialize the memory manager.
        
        Args:
            vector_store_client: Client for vector database (e.g., Pinecone, Weaviate)
            knowledge_graph_client: Client for knowledge graph storage
        """
        self.vector_store = vector_store_client
        self.knowledge_graph = knowledge_graph_client
        self._cache = {}  # Simple in-memory cache for hot paths
        
    async def store_memory(self, memory: Memory) -> bool:
        """Store a new memory in the appropriate storage system."""
        try:
            # Add to vector store for semantic search
            if self.vector_store:
                await self._store_in_vector_store(memory)
            
            # Add to knowledge graph for structured queries
            if self.knowledge_graph:
                await self._store_in_knowledge_graph(memory)
                
            # Update cache
            self._update_cache(memory)
            
            logger.info(f"Stored memory {memory.id} for user {memory.user_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to store memory {memory.id}: {str(e)}")
            return False

    async def retrieve_memories(
        self, 
        user_id: str, 
        query: str, 
        top_k: int = 5,
        memory_types: Optional[List[MemoryType]] = None,
        min_importance: float = 0.0,
        max_age_days: Optional[int] = None
    ) -> List[Memory]:
        """
        Retrieve relevant memories based on blended scoring (relevance, recency, importance).
        
        Args:
            user_id: ID of the user whose memories to retrieve
            query: Query to match against memories
            top_k: Number of memories to return
            memory_types: Types of memories to include
            min_importance: Minimum importance threshold
            max_age_days: Maximum age of memories to include
        
        Returns:
            List of relevant memories, scored and ranked
        """
        try:
            # Check cache first
            cache_key = f"{user_id}:{query}"
            if cache_key in self._cache:
                return self._cache[cache_key][:top_k]
            
            # Retrieve from vector store using semantic search
            vector_results = []
            if self.vector_store:
                vector_results = await self._retrieve_from_vector_store(
                    user_id, query, top_k
                )
            
            # Retrieve from knowledge graph for structured queries
            graph_results = []
            if self.knowledge_graph:
                graph_results = await self._retrieve_from_knowledge_graph(
                    user_id, query, top_k
                )
            
            # Combine results and score them using blended approach
            all_memories = vector_results + graph_results
            
            # Filter by criteria
            filtered_memories = [
                mem for mem in all_memories
                if (memory_types is None or mem.memory_type in memory_types)
                and mem.importance >= min_importance
                and (max_age_days is None or 
                     (datetime.now() - mem.created_at).days <= max_age_days)
            ]
            
            # Score using blended approach: relevance (from retrieval), recency, importance
            scored_memories = []
            for memory in filtered_memories:
                recency_score = self._calculate_recency_score(memory)
                # Combine scores (this is a simplified model)
                combined_score = (0.4 * memory.importance + 
                                0.4 * getattr(memory, 'relevance_score', 0.5) + 
                                0.2 * recency_score)
                
                scored_memories.append((memory, combined_score))
            
            # Sort by score and return top_k
            scored_memories.sort(key=lambda x: x[1], reverse=True)
            result = [mem for mem, score in scored_memories[:top_k]]
            
            # Cache the result
            self._cache[cache_key] = result
            
            logger.info(f"Retrieved {len(result)} memories for user {user_id}")
            return result
        except Exception as e:
            logger.error(f"Failed to retrieve memories for user {user_id}: {str(e)}")
            return []

    async def generate_memory(
        self, 
        user_id: str, 
        conversation_context: str, 
        topic_definitions: List[str]
    ) -> Optional[Memory]:
        """
        Generate a memory from conversation context using LLM-driven ETL process.
        
        This runs as an asynchronous background process.
        """
        try:
            # Extract meaningful content based on topic definitions
            extracted_content = await self._extract_meaningful_content(
                conversation_context, topic_definitions
            )
            
            if not extracted_content:
                return None
                
            # Create a new memory
            memory = Memory(
                id=f"mem_{datetime.now().timestamp()}_{user_id}",
                user_id=user_id,
                content=extracted_content,
                memory_type=self._classify_memory_type(extracted_content),
                importance=await self._assess_importance(extracted_content),
                created_at=datetime.now(),
                last_accessed=datetime.now(),
                provenance="conversation_etl"
            )
            
            # Store the memory
            success = await self.store_memory(memory)
            if success:
                logger.info(f"Generated memory {memory.id} for user {memory.user_id}")
                return memory
            else:
                return None
        except Exception as e:
            logger.error(f"Failed to generate memory for user {user_id}: {str(e)}")
            return None

    async def consolidate_memories(self, user_id: str) -> bool:
        """
        Consolidate memories by resolving conflicts, merging duplicates, 
        and pruning stale memories.
        
        This runs as an asynchronous background process.
        """
        try:
            # Retrieve all memories for the user
            all_memories = await self._get_all_memories_for_user(user_id)
            
            # Identify duplicates and conflicts
            duplicates = self._find_duplicates(all_memories)
            conflicts = self._find_conflicts(all_memories)
            
            # Resolve conflicts and merge duplicates
            for duplicate_group in duplicates:
                # Keep the most important/recent
                kept_memory = max(duplicate_group, 
                                key=lambda m: (m.importance, m.created_at))
                
                # Remove others
                for mem in duplicate_group:
                    if mem.id != kept_memory.id:
                        await self._remove_memory(mem.id)
            
            # Prune low-confidence memories
            low_confidence_memories = self._find_low_confidence_memories(all_memories)
            for memory in low_confidence_memories:
                await self._remove_memory(memory.id)
            
            logger.info(f"Consolidated memories for user {user_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to consolidate memories for user {user_id}: {str(e)}")
            return False

    def _calculate_recency_score(self, memory: Memory) -> float:
        """Calculate recency score based on time since creation."""
        age_hours = (datetime.now() - memory.created_at).total_seconds() / 3600
        # Recency score decreases exponentially over time
        # More recent memories get higher scores
        return max(0.0, min(1.0, 1.0 / (1.0 + age_hours / 24)))  # Half-life of 24 hours

    async def _extract_meaningful_content(
        self, 
        conversation_context: str, 
        topic_definitions: List[str]
    ) -> Optional[str]:
        """
        Use LLM to extract meaningful content from conversation.
        
        This is a simplified implementation - in production, you'd use an actual LLM.
        """
        # This would use an LLM in production to filter for meaningful content
        # For now, we'll return the original context if it matches topic definitions
        content_lower = conversation_context.lower()
        for topic in topic_definitions:
            if topic.lower() in content_lower:
                return conversation_context
        
        return None

    def _classify_memory_type(self, content: str) -> MemoryType:
        """Classify memory as declarative or procedural."""
        procedural_indicators = [
            "how to", "steps to", "process", "procedure", "method", 
            "algorithm", "way to", "technique"
        ]
        
        content_lower = content.lower()
        for indicator in procedural_indicators:
            if indicator in content_lower:
                return MemoryType.PROCEDURAL
        
        return MemoryType.DECLARATIVE

    async def _assess_importance(self, content: str) -> float:
        """
        Assess the importance of content using various heuristics.
        
        This is a simplified implementation - in production, you'd use an LLM.
        """
        # Heuristic importance assessment
        importance = 0.5  # Base importance
        
        # Keywords that increase importance
        important_keywords = [
            "important", "critical", "essential", "key", "must", 
            "name", "birthday", "preference", "allergy", "requirement"
        ]
        
        content_lower = content.lower()
        for keyword in important_keywords:
            if keyword in content_lower:
                importance = min(1.0, importance + 0.2)
        
        # Length can also be a factor (not too short, not too long)
        length_factor = min(1.0, len(content) / 500)  # Normalize for content length
        importance = (importance + length_factor) / 2
        
        return importance

    async def _store_in_vector_store(self, memory: Memory):
        """Store memory in vector database for semantic search."""
        # Implementation depends on the specific vector store being used
        # This is a placeholder for Pinecone, Weaviate, etc.
        if self.vector_store:
            # Convert memory to embedding and store
            pass

    async def _store_in_knowledge_graph(self, memory: Memory):
        """Store memory in knowledge graph for structured queries."""
        # Implementation depends on the specific knowledge graph being used
        # This is a placeholder for Neo4j, Amazon Neptune, etc.
        if self.knowledge_graph:
            # Store memory as nodes and relationships
            pass

    async def _retrieve_from_vector_store(self, user_id: str, query: str, top_k: int) -> List[Memory]:
        """Retrieve memories from vector store based on semantic similarity."""
        # Implementation depends on the specific vector store
        # This is a placeholder
        return []

    async def _retrieve_from_knowledge_graph(self, user_id: str, query: str, top_k: int) -> List[Memory]:
        """Retrieve memories from knowledge graph based on structured queries."""
        # Implementation depends on the specific knowledge graph
        # This is a placeholder
        return []

    def _find_duplicates(self, memories: List[Memory]) -> List[List[Memory]]:
        """Find groups of duplicate memories."""
        # Simple heuristic: memories with very similar content
        # In production, you'd use semantic similarity
        return []

    def _find_conflicts(self, memories: List[Memory]) -> List[Tuple[Memory, Memory]]:
        """Find conflicting memories."""
        # In production, you'd identify memories containing contradictory information
        return []

    def _find_low_confidence_memories(self, memories: List[Memory]) -> List[Memory]:
        """Identify low-confidence memories to prune."""
        # Memories with low importance and old age
        threshold_date = datetime.now() - timedelta(days=30)  # 30 days
        return [
            mem for mem in memories 
            if mem.importance < 0.3 and mem.created_at < threshold_date
        ]

    async def _get_all_memories_for_user(self, user_id: str) -> List[Memory]:
        """Retrieve all memories for a specific user."""
        # This would query both vector store and knowledge graph
        return []

    async def _remove_memory(self, memory_id: str) -> bool:
        """Remove a memory from all storage systems."""
        # Remove from vector store, knowledge graph, and cache
        if memory_id in self._cache:
            del self._cache[memory_id]
        return True

    def _update_cache(self, memory: Memory):
        """Update the cache with the latest memory."""
        # Simple cache update
        pass


# Singleton instance for use in agents
memory_manager = MemoryManager()