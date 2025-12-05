# 🚀 ADK Agent Template

**Build AI agents the easy way.** This template gives you everything you need to create powerful AI agents using [Google's Agent Development Kit (ADK)](https://google.github.io/adk-docs/).

> 💡 **AI-Powered Development:** This repo includes special instructions for AI assistants. Just describe what you want to build, and your AI will guide you through the entire process!

---

## ✨ What's Inside

| Folder | What it does |
|--------|--------------|
| `adk_knowledge_base/` | Complete ADK documentation at your fingertips |
| `templates/` | Ready-to-use agent starter code |
| `.agent/workflows/` | Step-by-step guides for your AI assistant |

---

## 🏁 Quick Start

### 1️⃣ Clone This Template

```bash
# Using GitHub's "Use this template" button is easiest!
# Or clone it:
git clone https://github.com/YOUR_USERNAME/adk-agent-template.git my-agent-project
cd my-agent-project
```

### 2️⃣ Set Up Your Environment

```bash
# Create a virtual environment
python -m venv .venv

# Activate it
# Windows:
.venv\Scripts\activate
# Mac/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3️⃣ Add Your API Key

```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your Gemini API key
# Get one free at: https://aistudio.google.com/apikey
```

### 4️⃣ Start Building! 🎉

Tell your AI assistant:

> *"I want to build an agent that helps users track their fitness goals"*

Your AI will:
1. Ask you clarifying questions
2. Help you choose the right agent type
3. Write the code following ADK best practices
4. Test it with you

---

## 🤖 AI-Assisted Development

This template is designed to work seamlessly with AI coding assistants (Cursor, GitHub Copilot, etc.).

### Magic Commands

Just say these to your AI assistant:

| Say This | What Happens |
|----------|--------------|
| *"I have an idea for an agent..."* | 💭 AI helps you brainstorm and design |
| *"Create a new agent called X"* | 🛠️ AI scaffolds the project structure |
| *"My agent isn't working"* | 🔧 AI helps debug common issues |
| *"How do I add a tool?"* | 📚 AI references the knowledge base |

### How It Works

Your AI assistant automatically reads:
- `GEMINI.md` - Project context and rules
- `.cursorrules` - Development standards
- `adk_knowledge_base/` - Complete ADK reference

No setup needed. It just works! ✨

---

## 📁 Project Structure

```
my-agent-project/
│
├── 📚 adk_knowledge_base/          # ADK documentation
│   ├── adk_reference_guide.md      # Core concepts, tools, deployment
│   ├── adk_development_workflow.md # Step-by-step dev process
│   └── copilotkit_agui_integration.md  # Frontend integration
│
├── 🧩 templates/                   # Starter templates
│   ├── basic_agent/                # Simple agent to get started
│   └── tool_agent/                 # Agent with custom tools
│
├── 🤖 agents/                      # Your agents go here!
│   └── (your agents)
│
├── ⚙️ .agent/workflows/            # AI assistant workflows
├── 📋 .cursorrules                 # AI coding rules
├── 📋 GEMINI.md                    # AI project context
└── 📦 requirements.txt             # Python dependencies
```

---

## 🎯 Creating Your First Agent

### Option A: Use an AI Assistant (Recommended)

Just describe your idea:

> *"Create an agent that can search for recipes based on ingredients I have"*

### Option B: Use the ADK CLI

```bash
# Create a new agent
adk create my_first_agent

# Test it in the terminal
adk run my_first_agent

# Or test with a web UI
adk web --port 8000
```

### Option C: Copy a Template

```bash
# Copy the basic template
cp -r templates/basic_agent agents/my_agent

# Edit agents/my_agent/agent.py with your logic
```

---

## 📖 Learning Resources

| Resource | Description |
|----------|-------------|
| [ADK Reference Guide](adk_knowledge_base/adk_reference_guide.md) | Everything about agents, tools, and deployment |
| [Development Workflow](adk_knowledge_base/adk_development_workflow.md) | Step-by-step development process |
| [CopilotKit Integration](adk_knowledge_base/copilotkit_agui_integration.md) | Add a chat UI to your agent |
| [Official ADK Docs](https://google.github.io/adk-docs/) | Google's official documentation |

---

## 🛠️ Common Tasks

### Add a Custom Tool

```python
def search_products(query: str) -> dict:
    """Search for products matching the query.
    
    Args:
        query: The search term to look for
        
    Returns:
        A dictionary with matching products
    """
    # Your logic here
    return {"results": [...]}

# Add to your agent
root_agent = Agent(
    name="shopping_assistant",
    tools=[search_products],  # 👈 Add your tool here!
    ...
)
```

### Deploy to Cloud Run

```bash
gcloud run deploy my-agent --source .
```

See [Advanced Topics](adk_knowledge_base/adk_reference_guide.md#advanced-topics) for more deployment options.

---

## ❓ Troubleshooting

| Problem | Solution |
|---------|----------|
| `API key not found` | Make sure `.env` has your `GOOGLE_API_KEY` |
| `Module not found` | Run `pip install -r requirements.txt` |
| `Agent not responding` | Check your tool docstrings - the AI needs them! |

---

## 🤝 Contributing

Found a way to make this template better? PRs welcome!

---

## 📜 License

MIT License - Use this however you want!

---

<p align="center">
  <b>Happy Building! 🎉</b><br>
  <sub>Made with ❤️ for the ADK community</sub>
</p>
