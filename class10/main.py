import asyncio
from agents import Agent, Runner ,trace , input_guardrail ,InputGuardrailTripwireTriggered , GuardrailFunctionOutput , RunContextWrapper
from connection import config
from dotenv import load_dotenv
from openai.types.responses import ResponseTextDeltaEvent
from pydantic import BaseModel
import rich 
load_dotenv()

class User_info(BaseModel):
    name : str
    user_type : str

user_info = User_info(name="Abdul Manan", user_type="Patient")
user_info2 = User_info(name="Abdul Manan", user_type="Medical Student")
user_info3 = User_info(name="Abdul Manan", user_type="Doctor")



def dynamic_instructions(ctx : RunContextWrapper[User_info] , agent : Agent):
    if ctx.context.user_type == "Patient":
        return """
        Use simple, non-technical language. Explain medical terms in everyday words. Be empathetic and reassuring
    
        """
    elif ctx.context.user_type == "Medical Student":
        return """
        Use moderate medical terminology with explanations. Include learning opportunities
        """
    elif ctx.context.user_type == "Doctor":
        return """
        Use full medical terminology, abbreviations, and clinical language. Be concise and professional
        """

hospital_agent = Agent(
    name="Hospital Agent",
    instructions=dynamic_instructions,
)






async def main():
    with trace("Dynamic Instruction"):
        user_input = input("how can i help you")
        result = await Runner.run(
            hospital_agent,
            user_input,
            run_config=config,
            context=user_info3

        )
        rich.print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
