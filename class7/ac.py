import asyncio
from agents import Agent, Runner ,trace , input_guardrail ,InputGuardrailTripwireTriggered , GuardrailFunctionOutput
from connection import config
from dotenv import load_dotenv
from openai.types.responses import ResponseTextDeltaEvent
from pydantic import BaseModel
import rich 

load_dotenv()

class ac_output(BaseModel):
    response : str
    isTemperatureBelow : bool


ac_guard = Agent(
    name = "AC Guard",
    instructions="""
    you are a AC Guard your task is if promt below 26C to stop them
    """,
    output_type=ac_output
)

@input_guardrail
async def security_guardrail(ctx ,agent , input):
    result = await Runner.run(
        ac_guard,
        input, 
        run_config=config
    )
    rich.print(result.final_output)

    return GuardrailFunctionOutput(
        output_info= result.final_output.response,
        tripwire_triggered= result.final_output.isTemperatureBelow 
    )


ac_control_agent = Agent(
    name = "AC Control Agent",
    instructions="""
    you are a AC Control Agent your task is adjust AC temperature to user input default temperature is 30C
    """,
    input_guardrails= [security_guardrail]
)

async def main():
    with trace("AC Agent "):
        
        
        try:
            user_input : str = input("what can i help you ? :  ")
            result = await Runner.run(
                ac_control_agent,
                input=user_input,
                run_config=config
            )
            print("AC Agent is onboarded")
        except InputGuardrailTripwireTriggered :
            print("AC Agent cannot check in")



if __name__ == "__main__":
    asyncio.run(main())