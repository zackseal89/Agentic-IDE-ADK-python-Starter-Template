# ADK Agent Development Workflow

This document outlines the standard workflow for developing AI agents using the Agent Development Kit (ADK). Follow these steps to ensure a structured and efficient development process.

## Phase 1: Setup & Initialization

1.  **Prerequisites Check**
    *   Ensure Python 3.10+ is installed.
    *   Obtain a Google Cloud Project ID and Gemini API Key.

2.  **Environment Setup**
    ```bash
    # Create and activate virtual environment
    python -m venv .venv
    source .venv/bin/activate  # or .venv\Scripts\activate on Windows
    
    # Install ADK
    pip install google-adk
    ```

3.  **Project Initialization**
    ```bash
    # Scaffold new agent project
    adk create <agent_name>
    cd <agent_name>
    ```
    *   *Action:* Configure `.env` with your `GOOGLE_API_KEY` and `GOOGLE_CLOUD_PROJECT`.

## Phase 2: Design & Architecture

1.  **Determine Agent Type**
    *   **Use `LlmAgent` if:** The task requires reasoning, natural language understanding, or dynamic decision making.
    *   **Use `Workflow Agent` if:** The process is a fixed sequence (`SequentialAgent`), requires parallel processing (`ParallelAgent`), or needs repetition (`LoopAgent`).
    *   **Use `Custom Agent` if:** You need highly specialized logic not covered by the above.

2.  **Define Capabilities (Tools)**
    *   Identify what external actions the agent needs (e.g., Search, Database access).
    *   Select built-in tools (Google Search, Code Execution) or plan custom Python functions.

3.  **Plan Memory & Session Management**
    *   **Session Memory:** For short-term working memory during a conversation
        * Plan for PII redaction and security measures
        * Consider token limits and conversation history management
        * Implement session isolation and access controls
    *   **Long-term Memory:** For persistent user information across sessions
        * Plan for vector database integration (Pinecone, Weaviate, etc.)
        * Design memory retrieval strategies with relevance scoring
        * Plan for background memory generation and consolidation

## Phase 3: Implementation

1.  **Implement Tools (`agent.py`)**
    *   Write custom Python functions with clear type hints and docstrings.
    *   *Tip:* The docstring is critical; it tells the LLM *when* and *how* to use the tool.

2.  **Configure the Agent (`agent.py`)**
    *   Instantiate your chosen Agent class.
    *   **Instruction Tuning:** Write a clear, concise system instruction.
    *   **Model Selection:** Choose the appropriate Gemini model (e.g., `gemini-3-pro-preview`).
    *   **Tool Registration:** Pass your list of tools to the agent constructor.

    ```python
    root_agent = Agent(
        name="my_agent",
        instruction="You are a helpful assistant...",
        tools=[my_tool, google_search],
        model="gemini-3-pro-preview"
    )
    ```

## Phase 4: Testing & Iteration

1.  **Interactive Testing (CLI)**
    *   Run `adk run <agent_name>` to test the conversation flow in the terminal.
    *   *Check:* Does the agent call tools correctly? Does it handle errors gracefully?

2.  **Visual Debugging (Web UI)**
    *   Run `adk web --port 8000` to use the chat interface.
    *   *Inspect:* Review the execution trajectory to understand the agent's reasoning steps.

3.  **Refinement**
    *   Refine the `instruction` if the agent is confused.
    *   Improve tool docstrings if tools are misused.

## Phase 5: Deployment

1.  **Containerization**
    *   ADK projects are container-ready. Use the generated `Dockerfile` (or create one).

2.  **Deploy to Cloud**
    *   **Option A (Vertex AI Agent Engine):** For managed scaling and enterprise features.
    *   **Option B (Cloud Run):** For serverless, container-based deployment.
    *   **Option C (GKE):** For full control and complex orchestrations.

    ```bash
    # Example Cloud Run deploy
    gcloud run deploy <service-name> --source .
    ```

## Phase 6: Evaluation & Monitoring

1.  **Systematic Evaluation**
    *   Create a test dataset of inputs and expected outputs.
    *   Run ADK's evaluation tools to measure response quality and tool usage accuracy.

2.  **Monitoring**
    *   Use BigQuery Agent Analytics (if configured) to track agent performance in production.
