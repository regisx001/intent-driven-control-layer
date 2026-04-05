import pandas as pd

from rich import print
from .tools import available_tools, get_last_rows

from ollama import chat

model = 'functiongemma'


messages = [
    {'role': 'user', 'content': 'Print the last 6 rows of the energy dataset !!'}]

print('Prompt:', messages[0]['content'])

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
        print(f"[Executing: {tool.function.name}({tool.function.arguments})]")

        if tool.function.name == 'get_last_rows':
            # This will now hold the actual markdown string of the dataframe!
            result = get_last_rows(**tool.function.arguments)
        else:
            result = f"Error: Tool {tool.function.name} not found."

        print(f"[Tool Result length: {len(str(result))} characters]")

        # 5. Send the stringified data back to the LLM
        messages.append({
            'role': 'tool',
            'content': str(result)
        })
