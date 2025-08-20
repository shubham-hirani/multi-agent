import os

from langgraph.prebuilt import create_react_agent, InjectedState
from langgraph_supervisor import create_supervisor
from langchain.chat_models import init_chat_model
from typing import Annotated
from langchain_core.tools import tool, InjectedToolCallId
from langgraph.graph import StateGraph, START, MessagesState
from langgraph.types import Command

def create_handoff_tool(*, agent_name: str, description: str | None = None):
    name = f"transfer_to_{agent_name}"
    description = description or f"Ask {agent_name} for help."

    @tool(name, description=description)
    def handoff_tool(
        state: Annotated[MessagesState, InjectedState],
        tool_call_id: Annotated[str, InjectedToolCallId],
    ) -> Command:
        tool_message = {
            "role": "tool",
            "content": f"Successfully transferred to {agent_name}",
            "name": name,
            "tool_call_id": tool_call_id,
        }
        return Command(
            goto=agent_name,
            update={**state, "messages": state["messages"] + [tool_message]},
            graph=Command.PARENT,
        )

    return handoff_tool


# Handoffs
assign_to_weather_agent = create_handoff_tool(
    agent_name="weather_agent",
    description="Assign task to a weather agent.",
)

assign_to_math_agent = create_handoff_tool(
    agent_name="math_agent",
    description="Assign task to a math agent.",
)

supervisor_agent = create_react_agent(
    model="openai:gpt-4.1",
    tools=[assign_to_weather_agent, assign_to_math_agent],
    prompt=(
        "You are a supervisor managing one agents:\n"
        "- a weather agent. Assign weather-related tasks to this agent\n"
        "- a math agent. Assign math-related tasks to this agent\n"
        "Assign work to one agent at a time, do not call agents in parallel.\n"
        "Do not do any work yourself."
        "If you do not find any agent provide answer on your own. "
        "Make sure you do not respond that you do not have any agent for given task"
        "After getting full response summarise the response and make it human readable"
    ),
    name="supervisor",
)