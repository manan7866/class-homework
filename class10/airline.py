import asyncio
from agents import Agent, Runner ,trace , input_guardrail ,InputGuardrailTripwireTriggered , GuardrailFunctionOutput , RunContextWrapper
from connection import config
from dotenv import load_dotenv
from openai.types.responses import ResponseTextDeltaEvent
from pydantic import BaseModel
import rich 
load_dotenv()

class Traveler_info(BaseModel):
    name : str
    seat_preference : str
    travel_experience : str

travler = Traveler_info(name="Abdul Manan", seat_preference="Window",travel_experience="First-time")

def dynamic_instructions(ctx : RunContextWrapper[Traveler_info] , agent : Agent):
    if ctx.context.seat_preference == "Window" and ctx.context.travel_experience == "First-time":
        return """
        Explain window benefits, mention scenic views, reassure about flight experience
        """
    elif ctx.context.seat_preference == "Middle" and ctx.context.travel_experience == "Frequent":
        return """
        Acknowledge the compromise, suggest strategies, offer alternatives
        """
    elif ctx.context.seat_preference == "Any" and ctx.context.travel_experience == "Premium":
        return """
        Highlight luxury options, upgrades, priority boarding
        """



airline_agent = Agent(
    name = 'Airline Agent',
    instructions=dynamic_instructions
)

async def main():
    with trace("Airline DI"):
        user_input = input("Message : ")
        result = await Runner.run(
            airline_agent,
            user_input,
            run_config=config,
            context=travler

        )
        rich.print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())