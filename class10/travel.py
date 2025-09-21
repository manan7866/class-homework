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
    trip_type : str
    traveler_profile : str 

travler = Traveler_info(name="Abdul Manan" , trip_type="Adventure" , traveler_profile="Solo")
traveler2 = Traveler_info(name="Abdul Manan" , trip_type="Cultural" , traveler_profile="Family")

def dynamic_instruction(ctx : RunContextWrapper[Traveler_info] , agent : Agent):
    if ctx.context.trip_type == "Adventure" and ctx.context.traveler_profile == "Solo":
        return """
        Suggest exciting activities, focus on safety tips,
        recommend social hostels and group tours for meeting people
        """
    elif ctx.context.trip_type == "Cultural" and ctx.context.traveler_profile == "Family":
        return """
        Focus on educational attractions, kid-friendly museums, interactive experiences, family accommodations
        """
    elif ctx.context.trip_type == "Business" and ctx.context.traveler_profile == "Executive" :
        return """
        Emphasize efficiency, airport proximity,
        business centers, reliable wifi, premium lounges.
        medical_student/doctor)
        """

transport_agent = Agent(
    name = "Transport Agent",
    instructions=dynamic_instruction
)

async def main():
    with trace("Transport Agent"):
        user_input = input("Your Message : ")
        result = await Runner.run(
            transport_agent,
            user_input,
            run_config=config,
            context=traveler2
        )
        rich.print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())