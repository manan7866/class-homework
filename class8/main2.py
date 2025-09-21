import asyncio
from connection import config
from agents import Agent, RunContextWrapper, Runner, function_tool
from pydantic import BaseModel
import rich

class StudentProfile(BaseModel):
    student_id: str 
    student_name: str
    current_semester: int
    total_courses: int

student = StudentProfile(
    student_id="STU-456",
    student_name="Hassan Ahmed",
    current_semester=4,
    total_courses=5
)

@function_tool
def getStudentInfo(wrapper :RunContextWrapper[StudentProfile]):
    return f'The user info is {wrapper.context}'

personal_agent = Agent(
    name = "Agent",
    instructions="you are a helper agent your task is full help of student and call the tool to get stutent's information",
    tools=[getStudentInfo]
)


async def main():
    user_input= input("which can i help you ? : ")
    result = await Runner.run(
        personal_agent,
        user_input,
        run_config=config,
        context = student
    )

    rich.print(result.final_output)



if __name__ == "__main__":
    asyncio.run(main())