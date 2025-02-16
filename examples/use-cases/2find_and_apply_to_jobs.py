"""
Find and apply to jobs.

@dev You need to add OPENAI_API_KEY to your environment variables.

Also you have to install PyPDF2 to read pdf files: pip install PyPDF2
"""

import csv
import os
import re
import sys
from pathlib import Path

from PyPDF2 import PdfReader
from dotenv import load_dotenv
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import asyncio
from typing import List, Optional

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from browser_use import ActionResult, Agent, Controller, Browser

from browser_use.browser.context import BrowserContext

load_dotenv()
import logging

# full screen mode
controller = Controller()

# NOTE: This is the path to your cv file
#CV = 'resume.pdf'

#if not CV.exists():
#	raise FileNotFoundError(f'You need to set the path to your cv file in the CV variable. CV file not found at {CV}')

browser = Browser()


@controller.action('Open website')
async def open_website(browser: Browser):
    page = browser.get_current_page()
    await page.goto('www.naukri.com')
    




async def main():
	
	

	

	model="gpt-4o"

	agent = Agent(
		task = '1. navigate to website using "open_website" function and search for "security engineer jobs".',
		llm=model, 
		controller=controller, 
		browser=browser)
	
	await agent.run()


if __name__ == '__main__':
	asyncio.run(main())
