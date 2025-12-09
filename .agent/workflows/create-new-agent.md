---
description: Create a new ADK agent from scratch or template
---

# 🛠️ Create New Agent Workflow

Use this workflow to scaffold a new agent project.

## Step 1: Get Agent Details

Ask the user:
1. **Agent name:** (lowercase with underscores, e.g., `recipe_finder`)
2. **Use template?** Basic (minimal), Tool Agent (with custom tools), or Memory Agent (with session and memory management)

---

## Step 2: Create Directory Structure

// turbo
```bash
# Create the agent directory
mkdir -p agents/<agent_name>
```

Create these files:

### `agents/<agent_name>/__init__.py`
```python
from .agent import root_agent
```

### `agents/<agent_name>/.env`
Copy from `.env.example`:
```
GOOGLE_API_KEY=your_api_key_here
GOOGLE_CLOUD_PROJECT=your_project_id
```

---

## Step 3: Create agent.py

### Option A: Basic Agent (no custom tools)

```python
"""
<Agent Name> - <One line description>
"""
from google.adk.agents.llm_agent import Agent

root_agent = Agent(
    name="<agent_name>",
    model="gemini-2.0-flash",
    description="<Brief description for other agents>",
    instruction="""You are a helpful assistant that <purpose>.

Your capabilities:
- <Capability 1>
- <Capability 2>

Guidelines:
- Be concise and friendly
- Ask for clarification if needed
""",
)
```

### Option B: Agent with Custom Tools

```python
"""
<Agent Name> - <One line description>
"""
from google.adk.agents.llm_agent import Agent


def example_tool(query: str) -> dict:
    """Search for something based on the query.
    
    Use this when the user wants to find information about X.
    
    Args:
        query: The search term
        
    Returns:
        Dictionary with search results
    """
    # TODO: Implement actual logic
    return {"results": [], "query": query}


root_agent = Agent(
    name="<agent_name>",
    model="gemini-2.0-flash",
    description="<Brief description>",
    instruction="""You are a helpful assistant that <purpose>.

Available tools:
- example_tool: Use to search for information

Guidelines:
- Be concise and friendly
- Use tools when appropriate
""",
    tools=[example_tool],
)
```

---

## Step 4: Test the Agent

// turbo
```bash
# Run in CLI mode
adk run agents/<agent_name>
```

Or for visual debugging:
```bash
adk web --port 8000
```

---

## Step 5: Iterate

Common improvements:
1. **Refine the instruction** if agent is confused
2. **Improve tool docstrings** if tools are misused
3. **Add more tools** as needed
4. **Add error handling** in tools

---

## Checklist

- [ ] Agent directory created in `agents/`
- [ ] `agent.py` with `root_agent` defined
- [ ] `__init__.py` exports `root_agent`
- [ ] `.env` configured with API key
- [ ] Tested with `adk run`
