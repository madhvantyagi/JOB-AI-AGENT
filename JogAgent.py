from browser_use import Agent,  Browser,Controller, ActionResult 
from browser_use.browser.context import BrowserContextConfig ,BrowserContext
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import re
import os
import asyncio
import logging



class JogAgent:
    self.task = None
    self.llm = None
    self.history = None
    self.browser = None
    
    def __init__(self, task, llm , history , browser):
        self.task = task
        self.llm = llm
        self.history = history
        self.browser = browser
    
    def intiate_agent_task(self):
        controller = Controller()
        job_apply_agent = Agent(
            browser=self.browser,
            llm=self.llm,
            task=self.task,
            use_vision=True,    
            controller=controller 
            history=self.history,
        )
        
    def async run_agent(self):
        history =await job_apply_agent.run()
        return history 
    
