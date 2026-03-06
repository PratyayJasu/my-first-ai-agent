def get_weather(city):
    # This is a placeholder function. In a real implementation, this would call a weather API.
    return f"The current weather in {city} is sunny with a temperature of 25°C."

def add_numbers(a, b):
    return a + b

TOOLS = {
    "get_weather": get_weather,
    "add_numbers": add_numbers,
}
