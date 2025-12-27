from typing import Callable, Dict, Any


class Tool:
    def __init__(self, name, description, schema, fn: Callable):
        self.name = name
        self.description = description
        self.schema = schema
        self.fn = fn


TOOLS: Dict[str, Tool] = {}


def register_tool(name: str, description: str, schema: Dict[str, Any], fn: Callable):
    tool = Tool(name, description, schema, fn)
    TOOLS[name] = tool


def get_tool(name: str) -> Tool:
    return TOOLS.get(name)


def list_tools() -> Dict[str, Tool]:
    return TOOLS
