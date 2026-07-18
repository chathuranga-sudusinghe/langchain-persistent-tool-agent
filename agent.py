from langchain.agents import create_agent

from llm import model
from tools import (
    get_current_time,
    get_project_information,
    multiply_numbers,
)


agent = create_agent(
    model=model,
    tools=[
        multiply_numbers,
        get_current_time,
        get_project_information,
    ],
    system_prompt=(
        "You are a helpful AI assistant. "
        "Use the available tools when they are useful."
    ),
)