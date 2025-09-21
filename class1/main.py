from agents import Agent, ModelSettings, Runner
from connection import config
import asyncio


translater_agent = Agent(
    name="Translater Agent",
    instructions="""
    Your are a translater Agent your job is translate user query English to Roman Urdu
    """
)


async def main():
    result = await Runner.run(
        translater_agent,
        input="translate this 'what is your name'",
        run_config=config
    )
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
