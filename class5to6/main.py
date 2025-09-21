from agents import Agent, Runner ,trace
from connection import config
from dotenv import load_dotenv
from openai.types.responses import ResponseTextDeltaEvent

from pydantic import ValidationError





load_dotenv()




import asyncio

# 🧠 Sub-agents
poet_writer_agent = Agent(
    name="Poet Writer Agent",
    instructions="You are a poet. Write a short 2-stanza poem based on the user's theme."
)

lyric_analyst = Agent(
    name="Lyric Analyst Agent",
    instructions="""
        You are a Lyric Poetry Analyst. Your job is to analyze the poem focusing on the poet's feelings and emotions.
        Identify the emotions expressed in the poem and explain how the poem conveys these feelings.
    """
)

narrative_analyst = Agent(
    name="Narrative Analyst Agent",
    instructions=f"""
        You are a Narrative Poetry Analyst. Analyze the poem as a story: characters and events or sequence.
        Comment on the storytelling aspects and poetic structure.
    """
)

dramatic_analyst = Agent(
    name="Dramatic Analyst Agent",
    instructions="""
        You are a Dramatic Poetry Analyst. Evaluate how the poem would sound or feel if performed aloud.
        Focus on performance voice tone and dramatic elements.
    """
)

# 🧠 Parent agent
parent_agent = Agent(
    name="Parent Agent",
    instructions="""
          You are the Parent Agent. Your work is delegate Agents user query 
    """
,
    handoffs=[
        poet_writer_agent,
        lyric_analyst,
        narrative_analyst,
        dramatic_analyst
    ],
    
)



async def main():
  with trace("Peot Agent"):
    user_input : str = input("📝 Please enter a theme or full poem: ")
    
    
    result = Runner.run_streamed(
        parent_agent,
        input=user_input,
        run_config=config
    )
    print("🛠️ Debug: Parent Agent returned. Last Agent was →", result.last_agent.name)
    print("\n📋 Final Output to User:\n")
    
    
    try:
     async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            print(event.data.delta, end="", flush=True)
    except ValidationError as validation_error:
     print("Validation error:", validation_error)
    except Exception as e:
     print("An unhandled error occurred:", e)       

if __name__ == "__main__":
    asyncio.run(main())
