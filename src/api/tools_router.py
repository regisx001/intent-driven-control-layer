from fastapi import APIRouter, HTTPException
from ..types import ToolCall
from src.tools_registry import TOOLS
from typing import Dict, Any, List

router = APIRouter()


@router.get("/tools")
def get_available_tools() -> Dict[str, Dict[str, Any]]:
    """List all available tools with their descriptions and schemas."""
    return {
        name: {
            "description": tool["description"],
            "schema": tool["schema"]
        }
        for name, tool in TOOLS.items()
    }


@router.post("/tools/call")
def call_tool(tool_call: ToolCall) -> Any:
    """Execute a tool call."""
    tool_name = tool_call["tool_name"]
    if tool_name not in TOOLS:
        raise HTTPException(
            status_code=404, detail=f"Tool '{tool_name}' not found")

    try:
        result = TOOLS[tool_name]["function"](**tool_call["arguments"])
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
