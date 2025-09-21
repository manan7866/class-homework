from agents import Agent , Runner ,RunConfig , AsyncOpenAI , OpenAIChatCompletionsModel , function_tool , ModelSettings
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
import requests # For Fetching API
from connection import config

load_dotenv()  


map_api_key = os.getenv("MAP_API_KEY")



now= datetime.now()


@function_tool
def find_restaurants(city: str, cuisine: str, current_dateTime = now) -> str:
    """
    Finds restaurants of a specific cuisine in a given city using the Geoapify API.
    """
    # Step 1: Get lat/lon from city
    geo_url = f"https://api.geoapify.com/v1/geocode/search?text={city}&apiKey={map_api_key}"
    geo_res = requests.get(geo_url).json()

    try:
        lat = geo_res["features"][0]["properties"]["lat"]
        lon = geo_res["features"][0]["properties"]["lon"]
    except (IndexError, KeyError):
        return f"❌ Could not find location for {city}."

    # Step 2: Get restaurants from Places API
    category = f"catering.restaurant.{cuisine.lower()}"
    radius = 5000  # 5 km radius
    places_url = (
        f"https://api.geoapify.com/v2/places?"
        f"categories={category}&"
        f"filter=circle:{lon},{lat},{radius}&"
        f"limit=5&"
        f"apiKey={map_api_key}"
    )

    places_res = requests.get(places_url).json()
    restaurants = places_res.get("features", [])

    if not restaurants:
        return f"😕 No {cuisine} restaurants found in {city}."

    # Step 3: Format clean response
    result = f"🍽️ Top {cuisine.capitalize()} Restaurants in {city}:\n\n"
    for idx, r in enumerate(restaurants, start=1):
        props = r["properties"]
        name = props.get("name", "Unnamed")
        addr = props.get("formatted", "Address not available")
        result += f"{idx}. 🏮 {name} - {addr}\n"

    return result





myAgent = Agent(
    name = "Map Agent",
    instructions = """
    
    You are a smart restaurant finder agent.

    When the user asks about restaurants or food places:

    1. Extract the city, cuisine (e.g., Chinese, pizza, etc.), and time context (e.g., open now, near me) from the users prompt.
    2. Call the find_restaurants tool with the extracted parameters.
    3. From the Geoapify API response, return only the most relevant results (e.g., top 3–5 restaurants).
    4. For each restaurant, include the name, address, and rating (if available).
    5. If the prompt is missing key information (like the city or cuisine), politely ask the user to clarify.
    always using tools
    """,
    




    tools= [find_restaurants],
    model_settings=ModelSettings(
        temperature=0.9
    )
)

response = Runner.run_sync(
    myAgent,
    input = "Find me some good Chinese restaurants near downtown karachi that are open right now",
    run_config = config
)

print(response.final_output)
