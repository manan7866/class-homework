import asyncio
from connection import config
from agents import Agent, RunContextWrapper, Runner, function_tool
from pydantic import BaseModel
import rich

class BankAccount(BaseModel):
    account_number: str 
    customer_name: str
    account_balance: float
    account_type: str

bank_account = BankAccount(
    account_number="ACC-789456",
    customer_name="Fatima Khan",
    account_balance=75500.50,
    account_type="savings"
)

@function_tool
def getUserInfo(wrapper :RunContextWrapper[BankAccount]):
    return f'The user info is {wrapper.context}'

personal_agent = Agent(
    name = "Agent",
    instructions="you are a helper agent your task is full help of user and call the tool to get user's information",
    tools=[getUserInfo]
)


async def main():
    user_input= input("which can i help you ? : ")
    result = await Runner.run(
        personal_agent,
        user_input,
        run_config=config,
        context = bank_account
    )

    rich.print(result.final_output)



if __name__ == "__main__":
    asyncio.run(main())

