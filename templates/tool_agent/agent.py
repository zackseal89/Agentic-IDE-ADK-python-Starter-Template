"""
Tool Agent Template - An ADK agent with custom tools.

This template demonstrates how to create an agent with custom Python
functions as tools. The agent can call these tools based on user requests.
"""
from google.adk.agents.llm_agent import Agent
from .tools import get_current_time, search_items


root_agent = Agent(
    name="tool_agent",
    model="gemini-2.0-flash",
    description="An assistant that can tell time and search for items.",
    instruction="""You are a helpful assistant with special capabilities.

Available tools:
- get_current_time: Get the current time in any city
- search_items: Search for items in our catalog

Guidelines:
- Use tools when the user's request matches their purpose
- Always explain the results in a friendly way
- If a tool returns an error, apologize and explain the issue
""",
    tools=[get_current_time, search_items],
)
