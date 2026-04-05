import json

from rich import print

from ollama import chat

model = 'functiongemma'


def get_weather(city: str) -> str:
    """
    Get the current weather for a city.

    Args:
      city: The name of the city

    Returns:
      A string describing the weather
    """
    return json.dumps({'city': city, 'temperature': 22, 'unit': 'celsius', 'condition': 'sunny'})


messages = [{'role': 'user', 'content': 'What is the weather in Tangier?'}]
print('Prompt:', messages[0]['content'])

response = chat(model, messages=messages, tools=[get_weather])

if response.message.tool_calls:
    tool = response.message.tool_calls[0]
    print(f'Calling: {tool.function.name}({tool.function.arguments})')

    result = get_weather(**tool.function.arguments)
    print(f'Result: {result}')

    messages.append(response.message)
    messages.append({'role': 'tool', 'content': result})

    final = chat(model, messages=messages)
    print('Response:', final.message.content)
else:
    print('Response:', response.message.content)
