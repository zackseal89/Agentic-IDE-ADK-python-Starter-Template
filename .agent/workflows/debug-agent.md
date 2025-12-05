---
description: Debug common ADK agent issues
---

# 🔧 Debug Agent Workflow

Use this workflow when an agent isn't working correctly.

## Step 1: Identify the Problem

Ask the user:
1. **What's the error message?** (if any)
2. **What did you expect to happen?**
3. **What actually happened?**

---

## Step 2: Common Issues Checklist

### 🔑 API Key Issues

**Symptoms:** "API key not found", "Authentication failed"

**Fix:**
```bash
# Check if .env exists
cat agents/<agent_name>/.env

# Verify the key is set
echo $GOOGLE_API_KEY
```

Ensure `.env` contains:
```
GOOGLE_API_KEY=your_actual_key_here
```

---

### 📦 Import Errors

**Symptoms:** "ModuleNotFoundError", "ImportError"

**Fix:**
```bash
# Ensure virtual environment is active
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Mac/Linux

# Install dependencies
pip install google-adk python-dotenv
```

---

### 🔧 Tool Not Being Called

**Symptoms:** Agent ignores the tool, doesn't use it when expected

**Causes:**
1. **Missing docstring** - LLM doesn't know when to use it
2. **Vague docstring** - LLM doesn't understand the purpose
3. **Tool not in tools list** - Forgot to add it

**Fix:**
```python
# ❌ Bad - No docstring
def my_tool(x):
    return x

# ✅ Good - Clear docstring
def my_tool(query: str) -> dict:
    """Search for products matching the query.
    
    Use this when the user wants to find a product by name or category.
    
    Args:
        query: The search term
        
    Returns:
        Dictionary with matching products
    """
    return {"products": []}
```

Also check the agent instruction mentions the tool!

---

### 🤖 Agent Confused or Wrong Behavior

**Symptoms:** Agent gives wrong answers, acts unpredictably

**Causes:**
1. **Vague instruction** - Not clear enough
2. **Conflicting rules** - Contradictory guidance
3. **Missing context** - Doesn't know the domain

**Fix:** Improve the instruction:
```python
# ❌ Bad
instruction="You are helpful."

# ✅ Good
instruction="""You are a customer support agent for TechShop.

Your role:
- Help customers find products
- Answer questions about orders
- Escalate complex issues to humans

Guidelines:
- Be friendly but professional
- Always verify customer identity before sharing order details
- If unsure, say "Let me check on that for you"

Available tools:
- search_products: Find products in catalog
- get_order: Look up order status
"""
```

---

### 🔄 Agent Loops or Hangs

**Symptoms:** Agent keeps calling the same tool, never finishes

**Causes:**
1. **Tool returns unclear data** - LLM can't interpret result
2. **Instruction doesn't say when to stop**
3. **LoopAgent without exit condition**

**Fix:**
- Ensure tools return clear, structured data
- Add explicit stopping criteria in instruction
- For LoopAgent, define a clear `max_iterations` or exit condition

---

### 🌐 Connection/Network Errors

**Symptoms:** "Connection refused", timeout errors

**Fix:**
```bash
# Check if another process is using the port
netstat -ano | findstr :8000

# Try a different port
adk web --port 8001
```

---

## Step 3: Debug with Logs

Run with verbose output:
```bash
# See what the agent is thinking
adk run agents/<agent_name> --verbose
```

Or use the web UI to inspect:
```bash
adk web --port 8000
# Open http://localhost:8000 and check the "Trace" panel
```

---

## Step 4: Test Tools Individually

Create a test script:
```python
# test_tools.py
from agents.my_agent.agent import my_tool

# Test the tool directly
result = my_tool("test query")
print(result)
```

```bash
python test_tools.py
```

---

## Step 5: Still Stuck?

1. Check the [ADK Reference Guide](../adk_knowledge_base/adk_reference_guide.md)
2. Review [Official ADK Docs](https://google.github.io/adk-docs/)
3. Search for the error message online
4. Ask for help with the full error traceback
