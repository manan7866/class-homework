from agents import Agent , Runner ,RunConfig , AsyncOpenAI , OpenAIChatCompletionsModel , function_tool , ModelSettings
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
import requests # For Fetching API
from connection import config
import smtplib
from email.mime.text import MIMEText



app_password = os.getenv("EMAIL_PASSWORD")
sender_email = os.getenv("EMAIL_ADDRESS") 

@function_tool
def send_email(to: str, subject: str, body: str) -> str:
    """
    Sends an email via Gmail using SMTP.
    """
    message = MIMEText(body)
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = to

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, app_password)
            server.send_message(message)
        return f"Email successfully sent to {to}"
    except Exception as e:
        return f"Failed to send email: {str(e)}"

mail_agent = Agent(
    name = "Mail Agent",
    instructions="""
    You are a mail agent your task is send mail by using tool
    """,
    tools=[send_email]
    
)

response = Runner.run_sync(
    mail_agent,
    input = "Send an email to wighiosultan@gmail.com about the project deadline being moved to next Wednesday",
    run_config = config
)

print(response.final_output)