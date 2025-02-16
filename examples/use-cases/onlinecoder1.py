import os
import asyncio
from playwright.async_api import async_playwright
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage
from typing import Optional

class BrowserAgent:
    def __init__(self, model: Optional[ChatOpenAI] = None):
        self.model = model or ChatOpenAI(
            model_name="gpt-4o",
            temperature=0.7
        )
        
    async def execute_task(self, task: str, page) -> str:
        """Execute a task using the language model and browser"""
        messages = [HumanMessage(content=f"Task: {task}\nProvide specific browser actions to accomplish this task.")]
        response = await self.model.ainvoke(messages)
        return response.content

class BrowserController:
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None

    async def setup(self):
        """Initialize browser session"""
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=False)
        self.context = await self.browser.new_context()
        self.page = await self.context.new_page()
        
    async def cleanup(self):
        """Clean up browser resources"""
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()

async def main():
    # Initialize components
    controller = BrowserController()
    agent = BrowserAgent()
    
    try:
        # Setup browser
        await controller.setup()
        
        # Navigate to W3Schools
        await controller.page.goto('https://www.w3schools.com/tryit/')
        #await controller.page.wait_for_load_state('networkidle')
        
        # Execute tasks
        tasks = [
            "Find and click on the HTML tutorial button",
            "Look for a simple example and copy its code",
            "Paste the code into the editor and run it"
        ]
        
        for task in tasks:
            result = await agent.execute_task(task, controller.page)
            print(f"Task: {task}")
            print(f"Agent response: {result}\n")
            
            # Wait between tasks
            await asyncio.sleep(2)
        
        # Keep browser open briefly to see results
        await asyncio.sleep(10)
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    
    finally:
        # Cleanup
        await controller.cleanup()

if __name__ == "__main__":
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    # Run the main async function
    asyncio.run(main())