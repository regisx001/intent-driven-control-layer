import pandas as pd

from rich import print
from .tools import available_tools, get_last_rows

from ollama import chat

model = 'functiongemma'


messages = [
    {'role': 'user', 'content': 'Print the last rows of the energy dataset !!'}]

print('Prompt:', messages[0]['content'])

response = chat(model, messages=messages, tools=available_tools)

# The Agent Loop: Keep running until the model gives a final text answer
while True:
    response = chat(model, messages=messages, tools=available_tools)

    # 1. Break condition: If there are no tool calls, the model is giving the final answer!
    if not response.message.tool_calls:
        print('\nFinal Response:', response.message.content)
        break

    print(f"Tools : {response.message.tool_calls}")

    # 2. The model wants to use a tool. Add its request to the chat history.
    messages.append(response.message)

    # 3. Process every tool the model asked for in this specific turn
    for tool in response.message.tool_calls:
        print(
            f"\n[Model is calling: {tool.function.name}({tool.function.arguments})]")

        # Execute the appropriate Python function dynamically
        if tool.function.name == 'get_last_rows':
            result = get_last_rows(**tool.function.arguments)
        # elif tool.function.name == 'get_wind_speed':
        #     result = get_wind_speed(**tool.function.arguments)
        else:
            result = f"Error: Tool {tool.function.name} not found."

        print(f"[Tool Result: {result}]")

        # 4. Append the tool's result back into the chat history
        messages.append({
            'role': 'tool',
            'content': str(result)
        })

    # The loop repeats. The model reads the new history (with the tool result)
    # and decides whether to call another tool or formulate the final answer.
