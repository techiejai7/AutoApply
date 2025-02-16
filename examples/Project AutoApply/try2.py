import os
import asyncio
import csv
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel
from playwright.async_api import async_playwright
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage

class JobDetails(BaseModel):
    title: str
    company: str
    link: str
    location: Optional[str] = None
    experience: Optional[str] = None
    description: Optional[str] = None

class JobSearchController:
    def __init__(self):
        self.jobs: List[JobDetails] = []
    
    async def save_jobs_to_csv(self):
        filename = f'devops_jobs_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Title', 'Company', 'Location', 'Experience', 'Link', 'Description'])
            for job in self.jobs:
                writer.writerow([
                    job.title, job.company, job.location,
                    job.experience, job.link, job.description
                ])
        return f"Jobs saved to {filename}"

class BrowserAgent:
    def __init__(self, controller: JobSearchController):
        self.controller = controller
        self.model = ChatOpenAI(
            model_name="gpt-3.5-turbo",
            temperature=0.7
        )
    
    async def process_page_content(self, content: str) -> List[JobDetails]:
        """Process page content using LLM to extract job details"""
        messages = [HumanMessage(content=f"""
        Extract job details from the following content. Format as JSON list of jobs with fields:
        title, company, location, experience, link, description.
        Content: {content}
        """)]
        response = await self.model.ainvoke(messages)
        # Process response to create JobDetails objects
        # This is a placeholder - actual implementation would parse LLM response
        return []

async def main():
    controller = JobSearchController()
    agent = BrowserAgent(controller)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        
        try:
            # Navigate to Naukri.com
            await page.goto('https://www.naukri.com')
            await page.wait_for_load_state('networkidle')
            
            # Search for DevOps Engineer
            await page.fill('input[placeholder="Enter skills / designations / companies"]', 'DevOps Engineer')
            await page.click('button.qsbSubmit')
            await page.wait_for_load_state('networkidle')
            
            # Wait for job listings to load
            await page.wait_for_selector('.list')
            
            # Get first 5 job cards
            job_cards = await page.query_selector_all('.jobTuple')
            for i, card in enumerate(job_cards[:5]):
                try:
                    # Click to open job details
                    await card.click()
                    await page.wait_for_timeout(2000)  # Wait for details to load
                    
                    # Extract job information
                    title = await card.query_selector('.title')
                    company = await card.query_selector('.subTitle')
                    location = await card.query_selector('.location')
                    
                    job = JobDetails(
                        title=await title.inner_text() if title else "Unknown",
                        company=await company.inner_text() if company else "Unknown",
                        location=await location.inner_text() if location else "Unknown",
                        link=await page.url(),
                    )
                    controller.jobs.append(job)
                    
                except Exception as e:
                    print(f"Error processing job {i+1}: {str(e)}")
            
            # Save extracted jobs
            save_result = await controller.save_jobs_to_csv()
            print(save_result)
            
            # Keep browser open briefly to see results
            await page.wait_for_timeout(5000)
            
        except Exception as e:
            print(f"An error occurred: {str(e)}")
        
        finally:
            await browser.close()

if __name__ == "__main__":
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    # Run the main async function
    asyncio.run(main())