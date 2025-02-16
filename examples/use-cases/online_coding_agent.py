import os
import sys
from openai import OpenAI

from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio

from browser_use import Agent, Browser, Controller

import os


from dotenv import load_dotenv
load_dotenv()


async def main():
    browser = Browser()
    async with await browser.new_context() as context:
        
        model = ChatOpenAI(
    model_name="gpt-4o",  # Note: it's model_name, not model
    #temperature=0.7,     # Optional: controls randomness (0-1)
  #  max_tokens=None,     # Optional: max tokens in response
   # request_timeout=60   # Optional: seconds before timeout
)
        
        #model = ChatOpenAI(model='gpt-4')

        # Initialize browser agent
        agent1 = Agent(
            task='Open an online code editor https://www.w3schools.com/tryit/ in browser',
            llm=model,
            browser_context=context,
        )
        executor = Agent(
            task='try to find a coding problem on the page and solve it',
            llm=model,
            browser_context=context,
        )

        coder = Agent(
            task='Coder. Your job is to write and complete code. You are an expert coder. Code a simple calculator. Write the code on the coding interface after agent1 has opened the link.',
            llm=model,
            browser_context=context,
        )
        await agent1.run()
        await executor.run()
        await coder.run()

asyncio.run(main())
