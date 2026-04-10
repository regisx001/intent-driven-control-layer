import json
from typing import Any, Callable

from rich import print

try:
    from .tools import available_tools
except ImportError:
    # Allows running as a script: python src/main.py
    from tools import available_tools

from ollama import chat

model = 'functiongemma'
tool_registry: dict[str, Callable[..., str]] = {
    tool.__name__: tool for tool in available_tools
}


def _parse_tool_arguments(raw_arguments: Any) -> dict[str, Any]:
    if raw_arguments is None:
        return {}
    if isinstance(raw_arguments, dict):
        return raw_arguments
    if isinstance(raw_arguments, str):
        stripped = raw_arguments.strip()
        if not stripped:
            return {}
        parsed = json.loads(stripped)
        if not isinstance(parsed, dict):
            raise ValueError('Tool arguments must decode to a JSON object.')
        return parsed
    raise ValueError(
        f'Unsupported tool argument type: {type(raw_arguments).__name__}')


messages = [
    {'role': 'user', 'content': 'give me the 1 last row in energy dataset '}]

print('Prompt:', messages[0]['content'])
print(f"Available tools: {', '.join(sorted(tool_registry.keys()))}")

# The Agent Loop: Keep running until the model gives a final text answer
while True:
    # 1. Call the model (Only call it here, inside the loop)
    response = chat(model, messages=messages, tools=available_tools)

    # 2. Break condition: If there are no tool calls, it's the final answer
    if not response.message.tool_calls:
        print('\nFinal Response:', response.message.content)
        break

    print(f"\nTools Requested: {response.message.tool_calls}")

    # 3. Append the model's tool request to the history
    messages.append(response.message)

    # 4. Execute the requested tools
    for tool in response.message.tool_calls:
        tool_name = tool.function.name
        print(f"[Executing: {tool_name}({tool.function.arguments})]")

        function_to_call = tool_registry.get(tool_name)
        if function_to_call is None:
            result = f"Error: Tool {tool_name} not found."
        else:
            try:
                arguments = _parse_tool_arguments(tool.function.arguments)
                result = function_to_call(**arguments)
            except Exception as error:
                result = f"Error executing {tool_name}: {error}"

        print(f"[Tool Result length: {len(str(result))} characters]")

        # 5. Send the stringified data back to the LLM
        messages.append({
            'role': 'tool',
            'name': tool_name,
            'content': str(result)
        })
