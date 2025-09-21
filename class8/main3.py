import asyncio
from connection import config
from agents import Agent, RunContextWrapper, Runner, function_tool
from pydantic import BaseModel
import rich

class LibraryBook(BaseModel):
    book_id: str 
    book_title: str
    author_name: str
    is_available: bool

library_book = LibraryBook(
    book_id="BOOK-123",
    book_title="Python Programming",
    author_name="John Smith",
    is_available=True
)

@function_tool
def getBookInfo(wrapper :RunContextWrapper[LibraryBook]):
    return f'The user info is {wrapper.context}'

personal_agent = Agent(
    name = "Agent",
    instructions="you are a helper agent your task is full help of student and call the tool to get book information",
    tools=[getBookInfo]
)


async def main():
    user_input= input("which can i help you ? : ")
    result = await Runner.run(
        personal_agent,
        user_input,
        run_config=config,
        context = library_book
    )

    rich.print(result.final_output)



if __name__ == "__main__":
    asyncio.run(main())