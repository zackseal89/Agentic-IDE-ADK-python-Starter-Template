---
description: Brainstorm and design a new AI agent from an idea
---

# 🧠 Agent Brainstorming Workflow

Use this workflow when the user has an idea for an agent but needs help designing it.

## Step 1: Understand the Idea

Ask these clarifying questions:

1. **What problem does this agent solve?**
   - What task will it automate or assist with?

2. **Who will use it?**
   - End users, developers, internal team?

3. **What should the agent be able to DO?**
   - List specific actions (search, create, analyze, etc.)

4. **Does it need external data?**
   - APIs, databases, web scraping?

5. **Should it remember past conversations?**
   - Session-based or persistent memory?

---

## Step 2: Identify Required Tools

Based on the answers, list the tools needed:

```markdown
| Tool Name | Purpose | Type |
|-----------|---------|------|
| search_X | Find items in database | Custom |
| google_search | Get real-time info | Built-in |
| send_email | Notify users | Custom |
```

---

## Step 3: Recommend Agent Type

Use this decision tree:

```
Does the agent need to REASON and make dynamic decisions?
├── YES → Use LlmAgent
└── NO → Is it a fixed sequence of steps?
    ├── YES → Use SequentialAgent
    └── NO → Do steps run in parallel?
        ├── YES → Use ParallelAgent
        └── NO → Does it loop until done?
            ├── YES → Use LoopAgent
            └── NO → Use Custom Agent (BaseAgent)
```

---

## Step 4: Create Design Summary

Output a summary like this:

```markdown
## Agent Design: [Name]

**Type:** LlmAgent
**Purpose:** [One sentence description]

### Tools Required:
1. `tool_name` - Description
2. `tool_name` - Description

### Instruction Draft:
> You are a helpful assistant that [purpose].
> When the user asks about X, use tool Y.
> Always [behavior guideline].

### Next Steps:
1. Create agent directory: `agents/[name]/`
2. Implement tools
3. Test with `adk run`
```

---

## Step 5: Proceed to Implementation

Ask: "Ready to create this agent? I'll set up the project structure for you."

Then use the `/create-new-agent` workflow.
