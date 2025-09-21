import asyncio
from agents import Agent, Runner ,trace , input_guardrail ,InputGuardrailTripwireTriggered , GuardrailFunctionOutput
from connection import config
from dotenv import load_dotenv
from openai.types.responses import ResponseTextDeltaEvent
from pydantic import BaseModel
import rich 

load_dotenv()

class gate_kepeer_output(BaseModel):
    response : str
    isStutentFromOtherSchool : bool

gate_kepeer_guard = Agent(
    name ="Gate Kepeer Guard",
    instructions="""
    you are a Gate Kepeer Guard of Spectrum Schooling System your task is if students are from other school to stop them
    """,
    output_type=gate_kepeer_output
)

@input_guardrail
async def school_guard(ctx , agent , input):
    result = await Runner.run(
        gate_kepeer_guard,
        input,
        run_config=config
    )
    rich.print(result.final_output)

    return GuardrailFunctionOutput(
        output_info= result.final_output.response,
        tripwire_triggered= result.final_output.isStutentFromOtherSchool
    )

gate_kepeer_agent = Agent(
    name = "Gate Kepeer Agent",
    instructions="""
    you are a Gate Kepeer Agent your task is wellcome to student in School
    """,
    input_guardrails=[school_guard]
)


async def main():
   with trace("Gate Kepeer"):
    try :
      user_input = input("Your School name PLZ : ")
      result = await Runner.run(
         gate_kepeer_agent,
         input=user_input,
         run_config=config
      )
      print("Gate Kepeer OnBoarded")

    except InputGuardrailTripwireTriggered:
       print("Gate Kepeer cannot check-in")

if __name__ == "__main__" : 
   asyncio.run(main())