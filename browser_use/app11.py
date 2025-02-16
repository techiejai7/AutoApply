import os
import sys
import logging

from langchain_openai import ChatOpenAI

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio

from browser_use import Agent, Browser, Controller

from typing import List, Optional

from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI, ChatOpenAI
from pydantic import BaseModel, SecretStr
from langchain_google_genai import ChatGoogleGenerativeAI

from browser_use import Browser, ActionResult, Agent, Controller
from browser_use.browser.context import BrowserContext
# Configure logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UploadInfo(BaseModel):
    index: int


browser = Browser()
controller = Controller()
@controller.action('Open website')
async def open_naukri(url: str):
    #brower=Browser()
    page = browser.get_current_page()
    await page.goto('www.naukri.com')
    return ActionResult(extracted_content='Website opened')

@controller.action('Upload CV', param_model=UploadInfo)
async def handle_cv_upload(upload_info: UploadInfo, browser: BrowserContext):
    return await upload_cv(upload_info.index, browser)


@controller.action(
	'Upload cv to element - call this function to upload if element is not found, try with different index of the same upload element',
	requires_browser=True,
)
async def upload_cv(index: int, browser: BrowserContext):
    # Define the CV path
    CV = os.path.join(os.path.dirname(__file__), 'resume.pdf')
    path = str(CV)
    dom_el = await browser.get_dom_element_by_index(index)

    if dom_el is None:
        return ActionResult(error=f'No element found at index {index}')

    file_upload_dom_el = dom_el.get_file_upload_element()

    if file_upload_dom_el is None:
        logger.info(f'No file upload element found at index {index}')
        return ActionResult(error=f'No file upload element found at index {index}')

    file_upload_el = await browser.get_locate_element(file_upload_dom_el)

    if file_upload_el is None:
        logger.info(f'No file upload element found at index {index}')
        return ActionResult(error=f'No file upload element found at index {index}')

    try:
        await file_upload_el.set_input_files(path)
        msg = f'Successfully uploaded file to index {index}'
        logger.info(msg)
        return ActionResult(extracted_content=msg)
    except Exception as e:
        logger.debug(f'Error in set_input_files: {str(e)}')
        return ActionResult(error=f'Failed to upload file to index {index}')


@controller.action('Read my cv for context to fill forms')
def read_cv():
    CV = os.path.join(os.path.dirname(__file__), 'resume.pdf')
    with open(CV, 'r') as f:
        return f.read()
    



async def main():
    
    async with await browser.new_context() as context:
        #model = model='gpt-4o'

        llm=ChatOpenAI(
            model='gpt-4o',
            api_key=SecretStr(os.getenv('OPENAI_API_KEY', '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'))
        )

        



        # Initialize browser agent
        login = Agent(
           # task='Open an online code editor programiz.',
            task='use the open_naukri function to open the website and login using email (jaykrishnamishra23@gmail.com) and password (Gr@3691215) mentiond above.',

            llm=llm,
            browser_context=context,
            controller=controller,
        )
        jobsearch = Agent(
            task='Look for Job Search bar and Search for "Security Engineer" jobs. From the search results and open a job',
            llm=llm,
            browser_context=context,
            controller=controller,
        )

        jobapply = Agent(
            task='Analyse the job page, scross through the results to find a job and then open it new tab. Then find the "Apply" button, and answer any questions asked on right hand side tab.',
            llm=llm,
            browser_context=context,
        )

        uploadresume = Agent(
            task='Upload the resume from the path "\resume.pdf"',
            llm=llm,
            browser_context=context,
            controller=controller,
        )

        questions=Agent(
            task='Else is question is asked, it comes up on right hand side bar. enter the answer and submit the answer',
            llm=llm,
            browser_context=context,
            controller=controller,)
        
        await login.run()
        await jobsearch.run()
        await jobapply.run()
        await uploadresume.run()
       # await questions.run()

asyncio.run(main())
