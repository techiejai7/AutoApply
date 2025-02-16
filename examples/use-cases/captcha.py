"""
Simple try of the agent.

@dev You need to add OPENAI_API_KEY to your environment variables.
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio


from dotenv import load_dotenv
load_dotenv()
#from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI

from browser_use import Agent
#from anthropic import AsyncAnthropic
from langchain_anthropic import ChatAnthropic


# NOTE: captchas are hard. For this example it works. But e.g. for iframes it does not.
# for this example it helps to zoom in.
#llm = ChatOpenAI(model='gpt-3.5')

#llm = AsyncAnthropic(api_key="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")

import getpass
import os



llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2
    # other params...
)

agent = Agent(
	task='go to https://captcha.com/demos/features/captcha-demo.aspx and solve the captcha',
	llm=llm,
)


async def main():
	await agent.run()
	input('Press Enter to exit')


asyncio.run(main())
