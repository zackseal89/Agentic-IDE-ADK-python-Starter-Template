"""
Basic Agent Template - A minimal ADK agent to get you started.

This is the simplest possible agent. It has no custom tools and uses
only the LLM's built-in capabilities.
"""
from google.adk.agents.llm_agent import Agent

root_agent = Agent(
    name="basic_agent",
    model="gemini-2.0-flash",
    description="A helpful assistant that can answer questions and have conversations.",
    instruction="""You are a friendly and helpful AI assistant.

Your capabilities:
- Answer questions on a wide range of topics
- Help with explanations and summaries
- Engage in natural conversation

Guidelines:
- Be concise but thorough
- Ask for clarification if a question is unclear
- Be honest when you don't know something
""",
)
