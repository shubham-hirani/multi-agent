import os
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, MessagesState
from langgraph.graph import END

from dotenv import load_dotenv
load_dotenv()

from utils.utility import pretty_print_messages
from agents import math_agent, weather_agent
from agents.router_agent import supervisor_agent


# Define the multi-agent supervisor graph
supervisor = (
    StateGraph(MessagesState)
    # NOTE: `destinations` is only needed for visualization and doesn't affect runtime behavior
    .add_node(supervisor_agent, destinations=("weather_agent", "math_agent", END))
    .add_node(weather_agent)
    .add_node(math_agent)
    .add_edge(START, "supervisor")
    # always return back to the supervisor
    .add_edge("weather_agent", "supervisor")
    .add_edge("math_agent", "supervisor")
    .compile()
)

if __name__ == "__main__":

    from IPython.display import display, Image

    png_bytes = supervisor.get_graph().draw_mermaid_png()

    # Save to file
    with open("flow.png", "wb") as f:
        f.write(png_bytes)
    print("Flow graph saved as flow.png")
    user_question = input("User question: ")
    user_input = {
            "messages": [
                {
                    "role": "user",
                    "content": user_question,
                }
            ]
        }

    # If you  want to understand the flow of the agent handover uncomment below 2 line and comment last 2 line
    # for chunk in supervisor.stream(user_input):
    #     pretty_print_messages(chunk, last_message=True)

    result = supervisor.invoke(user_input)
    print(result["messages"][-1].content)
