# ADK Reference Guide

A comprehensive reference for developing AI agents using the Google Agent Development Kit (ADK).

---

## Table of Contents

1. [Core Concepts](#core-concepts)
2. [Python Development](#python-development)
3. [Tools & Capabilities](#tools--capabilities)
4. [Advanced Topics](#advanced-topics)

---

## Core Concepts

### Introduction

The Agent Development Kit (ADK) is a flexible and modular framework designed for developing and deploying AI agents. It is optimized for Gemini and the Google ecosystem but remains model-agnostic and deployment-agnostic. ADK aims to make agent development feel like traditional software development, enabling developers to create, deploy, and orchestrate agentic architectures ranging from simple tasks to complex workflows.

### Agent Types

ADK provides three core categories of agents to build sophisticated applications:

#### 1. LLM Agents

**Classes:** `LlmAgent`, `Agent`

- **Description:** These agents utilize Large Language Models (LLMs) as their core engine.
- **Capabilities:** Understand natural language, reason, plan, generate responses, and dynamically decide how to proceed or which tools to use.
- **Use Case:** Ideal for flexible, language-centric tasks where the path to the solution is not strictly defined.

#### 2. Workflow Agents

**Classes:** `SequentialAgent`, `ParallelAgent`, `LoopAgent`

- **Description:** Specialized agents that control the execution flow of other agents in predefined, deterministic patterns without using an LLM for the flow control itself.
- **Types:**
    - **Sequential:** Executes agents one after another.
    - **Parallel:** Executes multiple agents simultaneously.
    - **Loop:** Repeats an agent's execution based on a condition.
- **Use Case:** Perfect for structured processes needing predictable execution pipelines.

#### 3. Custom Agents

**Base Class:** `BaseAgent`

- **Description:** Agents created by extending the `BaseAgent` class directly.
- **Capabilities:** Allow implementation of unique operational logic, specific control flows, or specialized integrations not covered by standard types.
- **Use Case:** Highly tailored application requirements that don't fit into the LLM or Workflow paradigms.

### Multi-Agent Systems

Complex applications often employ multi-agent architectures where different agent types work together:

- **LLM Agents** handle intelligent, language-based task execution.
- **Workflow Agents** manage the overall process flow using standard patterns.
- **Custom Agents** provide specialized capabilities or rules.

This composition allows for modular and scalable applications with complex coordination and delegation.

---

## Python Development

### Installation

To get started with ADK in Python, you need Python 3.10 or higher.

1. **Install the package:**
    ```bash
    pip install google-adk
    ```

2. **Set up a virtual environment (Recommended):**
    ```bash
    python -m venv .venv
    # Windows
    .venv\Scripts\activate
    # Linux/Mac
    source .venv/bin/activate
    ```

### Creating an Agent Project

ADK provides a CLI command to scaffold a new project.

1. **Create project:**
    ```bash
    adk create my_agent
    ```

2. **Project Structure:**
    ```text
    my_agent/
    ├── agent.py       # Main agent code
    ├── .env           # API keys and configuration
    └── __init__.py
    ```

### Developing Your Agent

The `agent.py` file is the entry point. It must define a `root_agent`.

#### Basic Agent Structure

```python
from google.adk.agents.llm_agent import Agent

# Define tools (optional)
def get_current_time(city: str) -> dict:
    """Returns the current time in a specified city."""
    return {"status": "success", "city": city, "time": "10:30 AM"}

# Define the root agent
root_agent = Agent(
    model='gemini-3-pro-preview',
    name='root_agent',
    description="Tells the current time in a specified city.",
    instruction="You are a helpful assistant that tells the current time in cities. Use the 'get_current_time' tool for this purpose.",
    tools=[get_current_time],
)
```

#### Key Components

- **model**: The LLM model to use (e.g., `gemini-3-pro-preview`).
- **name**: Unique identifier for the agent.
- **description**: Brief description of what the agent does.
- **instruction**: System prompt guiding the agent's behavior.
- **tools**: List of python functions or tool objects the agent can use.

### Running Your Agent

You can run your agent using the command-line interface (CLI) or a local web interface.

#### CLI Mode

Interact with your agent directly in the terminal.
```bash
adk run my_agent
```

#### Web Interface

Launch a local web server with a chat interface for testing.
```bash
# Run from the parent directory of your agent folder
adk web --port 8000
```
Access the interface at `http://localhost:8000`.

> [!CAUTION]
> **ADK Web is for development only.** Do not use it for production deployments.

---

## Tools & Capabilities

### Overview

ADK provides a rich ecosystem of tools to equip agents with diverse capabilities. These range from built-in functions to complex integrations with Google Cloud and third-party services.

### Built-in Tools

ADK comes with several pre-built tools that can be immediately used by your agents.

#### Gemini Tools

- **Google Search:** Perform web searches using Google Search with Gemini to retrieve real-time information.
- **Code Execution:** Execute code using Gemini models to perform calculations, data analysis, or logic tasks.

#### Google Cloud Tools

Integrate seamlessly with Google Cloud services:

- **BigQuery:** Connect to BigQuery to retrieve data and perform analysis.
- **Bigtable:** Interact with Bigtable to retrieve data and execute SQL.
- **Spanner:** Interact with Spanner to retrieve data, search, and execute SQL.
- **Vertex AI RAG Engine:** Perform private data retrieval.
- **Vertex AI Search:** Search across private, configured data stores.
- **GKE Code Executor:** Run AI-generated code in a secure and scalable GKE environment.

### Third-Party Tools

ADK supports integration with various third-party services to extend agent functionality:

- **Atlassian:** Manage issues, search pages, and update team content (Jira, Confluence).
- **AgentQL:** Extract resilient, structured web data using natural language.
- **Apify:** Use Actors to scrape websites and automate web workflows.
- **Bright Data:** Connect AI to real web data.
- **Browserbase:** Powers web browsing capabilities for AI agents.
- **Exa:** Search and extract structured content from websites.

### Building Custom Tools

You can define your own tools using standard Python functions.

```python
def my_custom_tool(param: str) -> str:
    """Description of what the tool does."""
    # Tool logic here
    return "result"
```

These functions are then passed to the `tools` list when initializing an agent.

### Memory and Session Management

ADK agents can implement sophisticated memory and session management for production-grade applications.

#### Session Management
- **Short-term memory**: Manage conversation context within a single session
- **Security**: Implement PII redaction and session isolation
- **Performance**: Use token-based truncation and recursive summarization
- **Lifecycle**: Implement TTL policies for session cleanup

#### Long-term Memory
- **Storage**: Use vector databases (Pinecone, Weaviate) for semantic search
- **Retrieval**: Implement blended scoring (relevance, recency, importance)
- **Generation**: Use LLM-driven ETL processes for memory creation
- **Consolidation**: Background processing for memory merging and pruning

#### Context Engineering
A production agent's context payload includes:
- System Instructions and Tool Definitions
- Long-term Memory and External Knowledge (RAG)
- Immediate Conversation History and State

---

## Advanced Topics

### Deployment Options

ADK agents are designed to be deployment-agnostic and can be containerized for various environments.

#### 1. Agent Engine in Vertex AI

- **Description:** A fully managed auto-scaling service on Google Cloud specifically designed for AI agents.
- **Benefits:** Managed scaling, integrated management.

#### 2. Cloud Run

- **Description:** A managed auto-scaling compute platform that runs container-based applications.
- **Benefits:** Serverless, scales to zero, easy deployment of containers.

#### 3. Google Kubernetes Engine (GKE)

- **Description:** Managed Kubernetes service.
- **Benefits:** Full control over the environment, suitable for running Open Models or complex orchestrations.

#### 4. Other Container-friendly Infrastructure

- **Description:** Manually package your agent into a container image (Docker) and run it anywhere (local Docker, Podman, on-prem).
- **Benefits:** Flexibility, offline/disconnected operation.

### Evaluation

ADK includes built-in evaluation capabilities to systematically assess agent performance.

- **Response Quality:** Evaluate the final output of the agent.
- **Execution Trajectory:** Analyze the step-by-step execution path to ensure the agent is reasoning correctly.
- **Test Cases:** Run evaluations against predefined test cases to ensure consistency.

### Safety and Security

Building trustworthy agents requires implementing security patterns.

- **Best Practices:** Follow ADK's safety guidelines to prevent prompt injection and ensure safe tool usage.
- **Human-in-the-loop:** ADK Java (and potentially others) supports human confirmation for sensitive tool executions.
