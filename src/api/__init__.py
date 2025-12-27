from fastapi import APIRouter, HTTPException
from ..types import ToolCall
from ..tools_registry import get_tool, list_tools
from typing import Dict, Any, List

router = APIRouter()


@router.get("/tools")
def get_available_tools() -> Dict[str, Dict[str, Any]]:
    """List all available tools with their descriptions and schemas."""
    tools = list_tools()
    return {
        name: {
            "description": tool.description,
            "schema": tool.schema
        }
        for name, tool in tools.items()
    }


@router.post("/tools/call")
def call_tool(tool_call: ToolCall) -> Any:
    """Execute a tool call."""
    tool = get_tool(tool_call["tool_name"])
    if not tool:
        raise HTTPException(
            status_code=404, detail=f"Tool '{tool_call['tool_name']}' not found")

    try:
        result = tool.fn(**tool_call["arguments"])
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
