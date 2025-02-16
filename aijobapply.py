import os
import sys

from langchain_openai import ChatOpenAI

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
from langchain_google_genai import ChatGoogleGenerativeAI

from browser_use import Agent, Browser, Controller



async def main():
    browser = Browser()
    async with await browser.new_context() as context:
        #model = 'gpt-4o'

        llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2
    # other params...
)


        # Initialize browser agent
        login = Agent(
           # task='Open an online code editor programiz.',
            task='Open naukri.com ',

            llm=llm,
            browser_context=context,
        )
        jobsearch = Agent(
            task='Look for Job Search bar and Search for "Security Engineer" jobs. From the search results and open a job',
            llm=llm,
            browser_context=context,
        )

        jobapply = Agent(
            task='Analyse the job page, scross through the results to find a job with "Easy Apply", fillnaly click on easy apply button',
            llm=llm,
            browser_context=context,
        )

        #questions=Agent(
         #   task='Else is question is asked, it comes up on right hand side bar. enter the answer and submit the answer',
          #  llm=model,
           # browser_context=context,

        #)
        await login.run()
        await jobsearch.run()
        await jobapply.run()
       # await questions.run()

asyncio.run(main())
