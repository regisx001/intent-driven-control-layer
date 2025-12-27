from typing_extensions import TypedDict
from typing import Dict, Any


class ToolCall(TypedDict):
    tool_name: str
    arguments: Dict[str, Any]
