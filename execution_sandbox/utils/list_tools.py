"""
Script to list all available tools from tools.py with their documentation.
"""

import inspect
from typing import Any, Dict, List

import tools


def get_tool_info() -> List[Dict[str, Any]]:
    """
    Get information about all tools in the tools module.

    Returns:
        List[Dict[str, Any]]: List of dictionaries containing tool information
    """
    tool_info = []

    # Get all functions from the tools module
    for name, func in inspect.getmembers(tools, inspect.isfunction):
        # Skip private functions (those starting with _)
        if name.startswith("_"):
            continue

        # Get function signature
        sig = inspect.signature(func)

        # Get docstring
        doc = inspect.getdoc(func) or "No documentation available"

        tool_info.append({"name": name, "signature": str(sig), "docstring": doc})

    return tool_info


def print_tools():
    """Print all tools in a formatted way."""
    tools = get_tool_info()
    print(f"Number of available tools: {len(tools)}")
    print("*" * 80)

    for tool in tools:
        print(f"{tool['name']}{tool['signature']}")


if __name__ == "__main__":
    print_tools()
