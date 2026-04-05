import pandas as pd

from rich import print

from ollama import chat

model = 'functiongemma'
# Our mock database
data = {
    "city": ["Tokyo", "Paris", "New York", "Tangier"],
    "temperature_c": [15, 22, 8, 19],
    "condition": ["Sunny", "Cloudy", "Rainy", "Clear"],
    "wind_speed_kmh": [12, 18, 25, 14]
}
weather_db = pd.DataFrame(data)


def get_temperature(city: str) -> str:
    """
    Gets the current temperature and weather condition for a specific city.
    Args:
        city: The name of the city (e.g., "Paris", "Tokyo").
    """
    # Look up the city in our dataset
    result = weather_db[weather_db['city'].str.lower() == city.lower()]
    if result.empty:
        return f"Could not find weather data for {city}."

    temp = result.iloc[0]['temperature_c']
    cond = result.iloc[0]['condition']
    return f"The temperature in {city} is {temp}°C and it is {cond}."


def get_wind_speed(city: str) -> str:
    """
    Gets the current wind speed for a specific city in km/h.
    Args:
        city: The name of the city.
    """
    result = weather_db[weather_db['city'].str.lower() == city.lower()]
    if result.empty:
        return f"Could not find wind data for {city}."

    wind = result.iloc[0]['wind_speed_kmh']
    return f"The wind speed in {city} is {wind} km/h."


# We bundle these so the model knows they exist
available_tools = [get_temperature, get_wind_speed]


messages = [
    {'role': 'user', 'content': 'What is the temperature and wind speed and weather condition in Tangier?'}]
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
        if tool.function.name == 'get_temperature':
            result = get_temperature(**tool.function.arguments)
        elif tool.function.name == 'get_wind_speed':
            result = get_wind_speed(**tool.function.arguments)
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
