from agents import (
    Agent,
    OutputGuardrailTripwireTriggered,
    TResponseInputItem, 
    GuardrailFunctionOutput, 
    InputGuardrailTripwireTriggered, 
    Runner,
    input_guardrail,
    RunContextWrapper,
    output_guardrail, 
    trace
    )

from connection import config
from pydantic import BaseModel
import rich
import asyncio
from dotenv import load_dotenv

load_dotenv()

class advisor_output(BaseModel):
    response : str
    isInvestmentHigh : bool
    reason : str

guardrail_agent = Agent(
    name = "Output Guardrail Agent",
    instructions="""
    you are a Output Guardrail Agent your task is validate if investment is upto 2000 rupees of pkr to block them
    """,
    output_type=advisor_output
)

@output_guardrail
async def financial_output_guardrail(ctx, agent, output) -> GuardrailFunctionOutput:
    result = await Runner.run(
        guardrail_agent, 
        f"Validate this financial advice response: {output}", 
        run_config=config
    )

    rich.print(result.final_output)

    return GuardrailFunctionOutput(
        output_info= result.final_output.reason,
        tripwire_triggered= result.final_output.isInvestmentHigh
    )

earn_advisor_agent = Agent(
    name = "Earn Advisor Agent",
    instructions="""
    you are a advisor agent your job i(s help user how to he earn to his topic
    
    """,
    output_guardrails=[financial_output_guardrail]
)


async def main():
    with trace("Output Guardrail"):
        user_input = input("which Finance i can help you : ")
        try:
          result = await Runner.run(
            earn_advisor_agent,
            input=user_input,
            run_config=config

          )
          print(result.final_output)
        except OutputGuardrailTripwireTriggered as e:
         print('Output guardrail triggered - response did not meet safety standards')


if __name__ == "__main__":
    asyncio.run(main())
