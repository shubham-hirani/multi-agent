import os

import requests
from langgraph.prebuilt import create_react_agent

def get_weather_info(city_name:str):
    """Get weather of the given city"""
    url = f"http://api.openweathermap.org/geo/1.0/direct"
    params = {
        "q": city_name,
        "appid": os.getenv('OPENWEATHER_API_KEY')
    }

    # Make the request
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        lat = data[0].get('lat')
        lon = data[0].get('lon')

        url = "https://api.openweathermap.org/data/2.5/weather"
        # Make the request
        params = {
            "lat": lat,
            "lon": lon,
            "appid": os.getenv('OPENWEATHER_API_KEY')
        }
        response = requests.get(url, params=params).json()
        return response
    else:
        return {"error": f"Failed to fetch weather data. Status code: {response.status_code}"}

weather_agent = create_react_agent(
    model="openai:gpt-4.1",
    tools=[get_weather_info],
    prompt=(
        "You are a weather finding agent.\n\n"
        "INSTRUCTIONS:\n"
        "- Assist ONLY with weather-related tasks\n"
        "- After you're done with your tasks, respond to the supervisor directly\n"
        "- Respond ONLY with the results of your work, do NOT include ANY other text."
    ),
    name="weather_agent",
)