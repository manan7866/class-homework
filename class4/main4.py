from agents import Agent , Runner ,RunConfig , AsyncOpenAI , OpenAIChatCompletionsModel , function_tool , ModelSettings
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
import requests # For Fetching API
from connection import config

now= datetime.now()
@function_tool
def meeting_set(
    team: str,
    date: str = None,
    day: str = None,
    time: str = "00:00",
    topic: str = ""
) -> str:
    """
    this is a meeting set tool you handle date and day work from this flow
    if date received you so day ignore
    if day received you so date ignore

    """
    return f"I Scheduled meeting with {team} on {date}/{day} at {time} for {topic} "

personal_Assistant = Agent(
    name = "Personal Assistant",
    instructions="""
    Your are a Personal Assistant your task is handle user personal quries by tools
    
    """,
    tools=[meeting_set]
)

response = Runner.run_sync(
    personal_Assistant,
    input = "Schedule a meeting with the marketing team for this Friday at 2 PM about the new campaign",
    run_config = config
)

print(response.final_output)