from datetime import datetime

from langchain_core.tools import tool


@tool
def multiply_numbers(first_number: float, second_number: float) -> float:
    """Multiply two numbers and return the result."""
    return first_number * second_number


@tool
def get_current_time() -> str:
    """Return the current local date and time."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


@tool
def get_project_information() -> str:
    """Return information about the current learning project."""
    return (
        "This is a simple LangChain agent project that demonstrates "
        "model integration, automatic tool selection, and agent execution."
    )