# 🤖 AI Assistant Instructions

Welcome! This workspace is set up for developing AI agents using **Google's Agent Development Kit (ADK)**.

## 🎯 Your Mission

Help the developer build amazing AI agents by:
1. Understanding their ideas
2. Guiding them to the right agent architecture
3. Writing clean, well-documented code
4. Following ADK best practices

---

## 📚 Knowledge Base

Before helping with any task, familiarize yourself with these resources:

| Document | Use For |
|----------|---------|
| [adk_reference_guide.md](adk_knowledge_base/adk_reference_guide.md) | Core concepts, agent types, tools, deployment |
| [adk_development_workflow.md](adk_knowledge_base/adk_development_workflow.md) | Step-by-step development phases |
| [copilotkit_agui_integration.md](adk_knowledge_base/copilotkit_agui_integration.md) | Adding a frontend UI |

---

## 🔄 Development Workflow

**Always follow this process when building agents:**

### Phase 1: Ideation 💭
When the user has an idea:
1. Ask clarifying questions about what the agent should do
2. Identify the core capabilities needed
3. List potential tools required
4. Recommend an agent type:
   - **LLM Agent** → For reasoning, conversation, dynamic decisions
   - **Workflow Agent** → For fixed sequences, parallel tasks, loops
   - **Custom Agent** → For specialized logic

### Phase 2: Design 📝
1. Define the agent's instruction (system prompt)
2. Design any custom tools needed
3. Plan the project structure

### Phase 3: Implementation 🛠️
1. Create the agent directory under `agents/`
2. Write `agent.py` with proper structure
3. Implement tools with clear docstrings
4. Set up `.env` from `.env.example`

### Phase 4: Testing 🧪
1. Run `adk run <agent_name>` for CLI testing
2. Run `adk web --port 8000` for visual debugging
3. Iterate based on results

---

## 📁 Project Structure

```
agents/           # User's agent projects go here
templates/        # Starter templates to copy from
adk_knowledge_base/  # Reference documentation
```

---

## ⚡ Quick Commands

| User Says | You Should |
|-----------|------------|
| "I want to build an agent that..." | Start ideation phase, ask questions |
| "Create a new agent" | Use templates or `adk create` |
| "Add a tool for..." | Write a Python function with type hints and docstring |
| "Deploy my agent" | Reference deployment section in knowledge base |
| "It's not working" | Check: API keys, imports, tool docstrings |

---

## ✅ Code Standards

Always follow these rules:

```python
# ✅ Good: Clear type hints and docstring
def get_weather(city: str) -> dict:
    """Get current weather for a city.
    
    Args:
        city: Name of the city to get weather for
        
    Returns:
        Dictionary with temperature and conditions
    """
    return {"temp": 72, "conditions": "sunny"}

# ❌ Bad: No types, no docstring
def get_weather(city):
    return {"temp": 72}
```

---

## 🚫 Never Do

- ❌ Hardcode API keys (use `.env`)
- ❌ Skip tool docstrings (LLM needs them!)
- ❌ Suggest `adk web` for production
- ❌ Ignore error messages - always investigate

---

## 🎉 Ready to Help!

When the user describes an agent idea, start with:

> "That sounds like a great agent idea! Let me ask a few questions to help design it properly..."

Then guide them through the workflow phases above.
