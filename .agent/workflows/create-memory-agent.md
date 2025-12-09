---
description: Create a new ADK agent with advanced context engineering capabilities
---

# 🧠 Create Memory-Enhanced Agent Workflow

Use this workflow to create an ADK agent with both session and memory management capabilities.

## Step 1: Determine Memory Requirements

Ask the user:
1. **What information should be remembered across sessions?**
   - Personal preferences?
   - User goals?
   - Interaction history?
   - Domain-specific knowledge?

2. **What is the expected conversation length?**
   - Short interactions (under 10 turns)
   - Medium conversations (10-50 turns)
   - Long-running sessions (50+ turns)

3. **What are the privacy/security requirements?**
   - PII handling needs
   - Data residency requirements
   - Compliance standards

## Step 2: Choose Memory Architecture

Based on requirements, recommend:

### Storage Options:
```
Do you need semantic search across large knowledge bases?
├── YES → Use Vector Database (Pinecone, Weaviate, ChromaDB)
└── NO → Simple key-value storage may suffice

Do you need complex relationship queries?
├── YES → Use Knowledge Graph (Neo4j, Amazon Neptune)
└── NO → Vector Database is sufficient
```

## Step 3: Create Directory Structure

// turbo
```bash
# Create the agent directory
mkdir -p agents/<agent_name>
```

Create these files:

### `agents/<agent_name>/__init__.py`
```python
from .agent import root_agent
from .memory_manager import memory_manager
from .session_manager import session_manager
```

### `agents/<agent_name>/session_manager.py`
```python
# Session management for short-term working memory
# Copied from templates/memory_agent/session_manager.py
```

### `agents/<agent_name>/memory_manager.py`
```python
# Long-term memory management
# Copied from templates/memory_agent/memory_manager.py
```

### `agents/<agent_name>/pii_detection.py`
```python
# PII detection and redaction utilities
# Copied from templates/memory_agent/pii_detection.py
```

## Step 4: Configure the Agent

### `agents/<agent_name>/.env`
Copy from `.env.example`:
```
GOOGLE_API_KEY=your_api_key_here
# Optional: Vector database configuration
# VECTOR_DB_URL=your_vector_db_url
# VECTOR_DB_API_KEY=your_vector_db_api_key
```

## Step 5: Create agent.py

```python
"""
Memory-Enhanced Agent - <One line description>
"""
from google.adk.agents.llm_agent import Agent
import asyncio
from typing import Dict, Any

# Import context engineering components
from .session_manager import session_manager, Message
from .memory_manager import memory_manager
from .pii_detection import pii_detector


async def retrieve_user_memories(user_id: str, query: str) -> Dict[str, Any]:
    """Retrieve relevant memories for the current context."""
    memories = await memory_manager.retrieve_memories(
        user_id=user_id,
        query=query,
        top_k=5,
        min_importance=0.3
    )
    
    return {
        "success": True,
        "memories": [mem.content for mem in memories],
        "count": len(memories)
    }


# Define tools that leverage memory
async def get_user_context(user_id: str, current_query: str) -> Dict[str, Any]:
    """Get relevant user context from long-term memory."""
    context = await retrieve_user_memories(user_id, current_query)
    return context


root_agent = Agent(
    name="<agent_name>",
    model="gemini-2.0-flash",
    description="<Brief description for other agents>",
    instruction="""You are a helpful assistant with access to both short-term session memory 
and long-term user memories.

Available information:
- Current session context
- Relevant long-term user memories

Guidelines:
- Use memory context to provide more personalized responses
- Respect user privacy and security requirements
- Be concise but thorough
- Ask for clarification if needed
""",
    tools=[],  # Add custom tools as needed
)
```

## Step 6: Test the Agent

// turbo
```bash
# Run in CLI mode
adk run agents/<agent_name>
```

For development with context visualization:
```bash
adk web --port 8000
```

## Step 7: Production Considerations

### Performance:
- Implement proper caching for memory retrieval (target <200ms)
- Use background tasks for memory generation
- Monitor token usage and context window management

### Security:
- Verify PII redaction is working properly
- Implement proper session isolation
- Apply access controls to memory data

### Monitoring:
- Track memory retrieval quality
- Monitor session performance metrics
- Log memory generation success rates

## Checklist

- [ ] Agent directory created in `agents/`
- [ ] `agent.py` with `root_agent` defined
- [ ] `session_manager.py` for short-term memory
- [ ] `memory_manager.py` for long-term memory
- [ ] `pii_detection.py` for security
- [ ] `__init__.py` exports all components
- [ ] `.env` configured with API keys
- [ ] Memory storage configured (if needed)
- [ ] Tested with `adk run`