from agents import Agent , Runner ,RunConfig , AsyncOpenAI , OpenAIChatCompletionsModel , function_tool , ModelSettings
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
import requests # For Fetching API
from connection import config

load_dotenv()  


api_key = os.getenv("WEATHER_API_KEY")

"jsum ohqm kwvo qgpf"
"ok7y 4hpi iyh7 e7mm dzff kgxr qfm6 r2xb"
now= datetime.now()

@function_tool
def weather_update(city , current_date = now ) -> str:
    """
    Returns weather update for the given city using OpenWeather API.
     
    
    """
    
    
    
    url =  requests.get(f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric")

    data = url.json()
    

    return f"The weather in {city} is {data}." 




myAgent = Agent(
    name = None,
    instructions = """
    You are a smart weather assistant. Whenever the user asks a weather-related question:

    1. Extract the city, date, and time (or general time of day like 'morning', 'afternoon', 'evening') from the user's prompt.
    2. Call the weather tool using those parameters.
    3. Identify and return the forecast that best matches the user's intent — whether it's for a specific hour, part of the day, or a general time like 'tonight', 'next Monday', or 'weekend'.
    4. Be concise and only return the relevant weather information. Avoid showing unnecessary data.
    """,

    tools= [weather_update],
    model_settings=ModelSettings(
        temperature=2.0
    )
)

response = Runner.run_sync(
    myAgent,
    input = "What's the weather going to be like in Dubai tomorrow afternoon?",
    run_config = config
)

print(response.final_output)
#document (https://insight.adsrvr.org/track/cei?advertiser_id=igcouad&cookie_sync=1&up…m/signup?return_url=https%3A%2F%2Fwww.yelp.com%2Fdevelopers%3Fcountry%3DUS)