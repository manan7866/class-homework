from agents import Agent, ModelSettings, Runner, function_tool , trace
import rich
from connection import config
import asyncio
import requests # For Fetching API

@function_tool(name_override="Get_location" , description_override="return user Current Location")
def get_current_location():
    """
    return location
    """
    return "Gulshan-e-Maymar , Karachi"

personal_agent = Agent(
    name = "Agent",
    instructions="you are a helper agent using tools",
    tools=[get_current_location],
    model_settings=ModelSettings(
        temperature="0.1",
        # tool_choice="required"
        # tool_choice="none"
        # tool_choice="auto"
    )
)


async def main():
    with trace("class 11"):
        result = await Runner.run(
            personal_agent,
            "what is my location",
            run_config= config
        )
        rich.print(result.new_items)
        rich.print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
