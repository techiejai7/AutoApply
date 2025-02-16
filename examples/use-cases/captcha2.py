import os
import sys
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Agent
import asyncio
from langchain_core.tools import BaseTool

import langchain_google_genai


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv()

# Initialize Gemini with proper configuration
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
   # temperature=0.1,
  #  max_tokens=2048,
  #  timeout=120,
   # max_retries=3,
  #  convert_system_message_to_human=True,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

# Remove the verbose parameter from Agent initialization
agent = Agent(
    task='go to https://captcha.com/demos/features/captcha-demo.aspx and solve the captcha',
    llm=llm
)

async def main():
    try:
        await agent.run()
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        input('Press Enter to exit')

if __name__ == "__main__":
    asyncio.run(main())