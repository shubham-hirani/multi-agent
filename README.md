# Multi-Agent System with LangGraph
[![Ask DeepWiki](https://devin.ai/assets/askdeepwiki.png)](https://deepwiki.com/shubham-hirani/multi-agent)

This project demonstrates a multi-agent system built with Python using LangChain and LangGraph. It features a supervisor agent that intelligently routes user requests to specialized agents—one for mathematical calculations and another for fetching weather data.

## How It Works

The core of the system is a state graph defined in `main.py` that orchestrates the interactions between different agents in a supervisor-worker pattern.

*   **Supervisor Agent (`router_agent.py`):** Acts as the central coordinator. It analyzes incoming user requests and uses hand-off tools (`assign_to_weather_agent`, `assign_to_math_agent`) to delegate the task to the most appropriate specialized agent. If no agent is suitable for the task, the supervisor is prompted to provide an answer on its own.

*   **Math Agent (`math_agent.py`):** A ReAct agent equipped with tools for basic arithmetic operations: `add`, `multiply`, and `divide`. It is responsible for handling all math-related queries.

*   **Weather Agent (`weather_agent.py`):** A ReAct agent that uses the OpenWeatherMap API to fetch current weather information for a specified city.

*   **Control Flow:** The `StateGraph` in `main.py` defines the interaction flow. All tasks start with the supervisor. After a specialized agent completes its task, control returns to the supervisor, which then finalizes the response. Running the main script also generates a `flow.png` file to visually represent this agent communication graph.

## Installation and Setup

Follow these steps to set up and run the project locally.

1.  **Clone the Repository**
    ```sh
    git clone https://github.com/shubham-hirani/multi-agent.git
    cd multi-agent
    ```

2.  **Install Dependencies**
    Install the required Python packages using the `requirements.txt` file.
    ```sh
    pip install -r requirements.txt
    ```

3.  **Set Up Environment Variables**
    Create a `.env` file from the provided sample and add your API keys.
    ```sh
    cp sample.env .env
    ```
    Now, edit the `.env` file with your credentials:
    ```env
    OPENAI_API_KEY=your_openai_api_key
    OPENWEATHER_API_KEY=your_openweather_api_key
    ```

## Usage

To run the multi-agent system, execute the `main.py` script from your terminal:

```sh
python main.py
```

The script will:
*   Execute a sample query defined within the file.
*   Print the step-by-step interaction between the agents to the console.
*   Generate a `flow.png` image in the root directory, visualizing the agent graph.

You can modify the user query in `main.py` to test different scenarios:
```python
# In main.py
# Example query for the weather agent
content = "What is the weather like in London?"

# Example query for the math agent
content = "What is 12 times 5?"
```

## Project Structure

```
.
├── main.py             # Entry point: defines and runs the agent graph
├── requirements.txt    # Project dependencies
├── sample.env          # Environment variable template
├── agents/             # Contains all agent definitions
│   ├── router_agent.py # Supervisor agent for task routing
│   ├── math_agent.py   # Agent for mathematical tasks
│   └── weather_agent.py# Agent for weather data
└── utils/
    └── utility.py      # Helper functions for pretty-printing output
