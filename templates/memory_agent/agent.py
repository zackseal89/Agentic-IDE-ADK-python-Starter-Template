"""
Memory-Enhanced Agent Template - An ADK agent with advanced session and memory management.

This template demonstrates how to create an agent that uses both session management
(short-term working memory) and long-term memory with retrieval capabilities.
"""

from google.adk.agents.llm_agent import Agent
import asyncio
from typing import Dict, Any, List
from datetime import datetime

# Import our new context engineering components
from .session_manager import session_manager, Message, Session
from .memory_manager import memory_manager, Memory, MemoryType
from .pii_detection import pii_detector


async def store_conversation_to_memory(session_id: str, user_id: str) -> Dict[str, Any]:
    """
    Store relevant parts of the conversation to long-term memory.
    
    This runs as an asynchronous background process after each conversation turn.
    """
    try:
        # Get the session history
        history = await session_manager.get_session_history(session_id, user_id)
        
        # Combine the conversation for memory extraction
        conversation_text = " ".join([msg.content for msg in history if msg.role in ['user', 'assistant']])
        
        # Define topics that should be remembered
        topic_definitions = [
            "personal preferences",
            "important facts",
            "user goals",
            "contact information",
            "important decisions"
        ]
        
        # Generate memory from conversation
        memory = await memory_manager.generate_memory(
            user_id=user_id,
            conversation_context=conversation_text,
            topic_definitions=topic_definitions
        )
        
        if memory:
            return {
                "success": True,
                "memory_id": memory.id,
                "message": "Conversation stored to long-term memory"
            }
        else:
            return {
                "success": False,
                "message": "No meaningful content found to store in memory"
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Error storing conversation to memory"
        }


async def retrieve_contextual_memories(user_id: str, query: str) -> Dict[str, Any]:
    """
    Retrieve relevant memories for the current context.
    
    Args:
        user_id: ID of the user requesting memories
        query: Current user query to match against memories
    
    Returns:
        Dictionary with retrieved memories and metadata
    """
    try:
        # Retrieve relevant memories using blended scoring (relevance, recency, importance)
        memories = await memory_manager.retrieve_memories(
            user_id=user_id,
            query=query,
            top_k=5,  # Retrieve top 5 relevant memories
            memory_types=[MemoryType.DECLARATIVE, MemoryType.PROCEDURAL],
            min_importance=0.3,  # Only get medium to high importance memories
        )
        
        # Format memories for use in agent prompt
        formatted_memories = [
            {
                "id": mem.id,
                "content": mem.content,
                "importance": mem.importance,
                "created_at": mem.created_at.isoformat(),
                "provenance": mem.provenance
            }
            for mem in memories
        ]
        
        return {
            "success": True,
            "memories": formatted_memories,
            "count": len(memories)
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "memories": [],
            "count": 0
        }


async def handle_user_message(user_id: str, session_id: str, message_content: str) -> str:
    """
    Handle a user message with full context engineering (session + memory).
    
    Args:
        user_id: ID of the user
        session_id: Current session ID
        message_content: User's message content
        
    Returns:
        Formatted response with context
    """
    try:
        # Retrieve relevant long-term memories to enhance context
        memory_response = await retrieve_contextual_memories(user_id, message_content)
        relevant_memories = memory_response.get("memories", [])
        
        # Format memories for inclusion in context
        memory_context = ""
        if relevant_memories:
            memory_context = "Relevant user memories:\n"
            for mem in relevant_memories:
                memory_context += f"- {mem['content']} (importance: {mem['importance']})\n"
        
        # Create a special tool response that includes memory context
        context_info = {
            "relevant_memories": len(relevant_memories),
            "memory_context": memory_context,
            "timestamp": datetime.now().isoformat()
        }
        
        return memory_context or "No relevant memories found."
    except Exception as e:
        return f"Error retrieving memories: {str(e)}"


def create_session_and_context(user_id: str, initial_context: str = "") -> Dict[str, Any]:
    """
    Create a new session with initial context.
    
    Args:
        user_id: ID of the user
        initial_context: Initial system context for the session
    
    Returns:
        Dictionary with session information
    """
    session = asyncio.run(session_manager.create_session(user_id, initial_context))
    return {
        "session_id": session.id,
        "user_id": session.user_id,
        "created_at": session.created_at.isoformat()
    }


# Define the main agent
root_agent = Agent(
    name="memory_enhanced_agent",
    model="gemini-2.0-flash",
    description="An agent with advanced session and memory management capabilities.",
    instruction="""You are a helpful assistant with access to both short-term session memory 
and long-term user memories. Your capabilities include:

1. Understanding the current conversation context (session memory)
2. Accessing relevant information from the user's long-term memories
3. Maintaining privacy and security standards

When appropriate, acknowledge relevant information from the user's memories to provide 
more personalized responses. Be sure to respect user privacy in all interactions.

Available information:
{memory_context}

Guidelines:
- Use memory context to provide more personalized responses
- Respect user privacy and security
- Ask for clarification if needed
- Be concise but thorough
""",
    tools=[],
)

# Add async tool for handling memory retrieval
async def enhanced_respond(user_id: str, session_id: str, message_content: str) -> Dict[str, Any]:
    """
    Enhanced response function that incorporates both session and memory context.
    """
    # Get memory context
    memory_context = await handle_user_message(user_id, session_id, message_content)
    
    # Update the instruction dynamically with memory context
    enhanced_instruction = root_agent.instruction.format(memory_context=memory_context)
    
    # Add user message to session
    user_message = Message(
        id=f"msg_{datetime.now().timestamp()}",
        role="user",
        content=message_content,
        timestamp=datetime.now()
    )
    
    await session_manager.add_message(session_id, user_id, user_message)
    
    # Schedule memory storage as a background task
    asyncio.create_task(store_conversation_to_memory(session_id, user_id))
    
    return {
        "status": "success",
        "memory_context": memory_context,
        "session_id": session_id,
        "user_id": user_id
    }