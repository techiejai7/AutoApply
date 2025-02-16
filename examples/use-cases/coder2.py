import os
import sys
import asyncio
from typing import Any, Dict, Optional
from pydantic import BaseModel
from dotenv import load_dotenv
from anthropic import Anthropic
from browser_use import Agent, Browser, Controller

# Load environment variables
load_dotenv()

class StructuredOutputWrapper:
    def __init__(self, claude_chat, output_schema: Optional[BaseModel] = None):
        self.claude_chat = claude_chat
        self.output_schema = output_schema
        
    async def ainvoke(self, messages):
        message_content = "\n".join([msg.content for msg in messages])
        
        if self.output_schema:
            message_content += f"\nPlease format your response according to this schema: {self.output_schema.schema()}"
        
        response = await self.claude_chat.client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=1024,
            temperature=0.7,
            messages=[{
                "role": "user",
                "content": message_content
            }]
        )
        
        return type('AIMessage', (), {'content': response.content[0].text})

class ClaudeChat:
    """Wrapper class to make Claude API compatible with browser_use Agent"""
    def __init__(self):
        self.client = Anthropic(api_key=os.getenv("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"))
        
    def with_structured_output(self, output_schema: Optional[BaseModel] = None, include_raw: bool = False):
        """Implement structured output interface required by browser_use"""
        self.output_schema = output_schema
        self.include_raw = include_raw
        return StructuredOutputWrapper(self, output_schema)
        
    async def ainvoke(self, messages):
        """Async invoke method to match LangChain's ChatModel interface"""
        response = await self.client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=1024,
            temperature=0.7,
            messages=[{
                "role": "user",
                "content": "\n".join([msg.content for msg in messages])
            }]
        )
        
        return type('AIMessage', (), {'content': response.content[0].text})

async def main():
    browser = Browser()
    async with await browser.new_context() as context:
        # Initialize Claude model wrapper
        model = ClaudeChat()
        
        # Define agents with their tasks
        agents = [
            Agent(
                task='Open an online code editor https://www.w3schools.com/tryit/ in browser',
                llm=model,
                browser_context=context,
            ),
            Agent(
                task='try to find a coding problem on the page and solve it',
                llm=model,
                browser_context=context,
            ),
            Agent(
                task='Coder. Your job is to write and complete code. You are an expert coder. '
                     'Code a simple calculator. Write the code on the coding interface after '
                     'agent1 has opened the link.',
                llm=model,
                browser_context=context,
            )
        ]
        
        # Execute agents sequentially with error handling
        for i, agent in enumerate(agents, 1):
            try:
                print(f"\nExecuting Agent {i}...")
                await agent.run()
                print(f"Agent {i} completed successfully")
                
                # Short pause between agents
                await asyncio.sleep(2)
                
            except Exception as e:
                print(f"Error running agent {i}: {str(e)}")
                print(f"Attempting to continue with next agent...")
                continue

if __name__ == "__main__":
    asyncio.run(main())