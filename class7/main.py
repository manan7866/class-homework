import asyncio
from agents import Agent, Runner ,trace , input_guardrail ,InputGuardrailTripwireTriggered , GuardrailFunctionOutput
from connection import config
from dotenv import load_dotenv
from openai.types.responses import ResponseTextDeltaEvent
from pydantic import BaseModel
import rich 

load_dotenv()
class SchoolAdmin_output(BaseModel):
    response: str
    isDistanceLess: bool


admin_guard = Agent(
    name ="Admin Guard",
    instructions="""
    you are a Admin Guard agent your task is check student promt.
    if student home distance is less than 20km to stop them.
     """,
    output_type = SchoolAdmin_output
)

@input_guardrail
async def security_guardrail(ctx, agent, input):
    result = await Runner.run(admin_guard, 
                              input, 
                              run_config=config
                              )
    rich.print(result.final_output)

    return GuardrailFunctionOutput(
        output_info= result.final_output.response,
        tripwire_triggered=result.final_output.isDistanceLess

    )

school_admin_agent = Agent(
    name = "School Admin Agent",
    instructions="""
     you are a school admin agent your task is change student class timing 
     """,
    input_guardrails=[security_guardrail]
    
)


async def main():
    with trace("Learning Guardrails "):
        
        
        try:
            user_input : str = input("what can i help you ? :  ")
            result = await Runner.run(
                school_admin_agent,
                input=user_input,
                run_config=config
            )
            print("Admin Agent is onboarded")
        except InputGuardrailTripwireTriggered :
            print("Admin cannot check in")



if __name__ == "__main__":
    asyncio.run(main())
