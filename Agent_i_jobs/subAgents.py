from browser_use import Agent, Browser, Controller, ActionResult , BrowserConfig
from browser_use.browser.context import BrowserContextConfig, BrowserContext
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import re
import os
import asyncio
import logging
from Agent.JobAgent import JobAgent
from FIles.resume_details import User_Details

openai_api_key = os.getenv('OPENAI_API_KEY')
''' 
Trying to create an agent here as an hook that only runs if we have to create an account before 
logging in as some companies require you to create account before applying for job
'''


task_2='''  
CHECK BEFORE THAT WE NEED TO CREATE AN ACCOUNT 
 IF WE HAVE TO CREATE AN ACCOUNT THEN :
        1) you have to start Applying application :
        1.0) you have find Apply now button may be from scrolling down to bottom or somewhere in webpge , cick on apply now .
        1.1) you might have to create account before applying , webpage will look like options like , signup or create account or don't have account yet , or etc
        fill the username and some pass word then after filling click on signup or registered or similar buttons like that.
        2 ) if you don't have to create an account or you done creating stop here , 
 ELSE:
  YOU DON'T HAVE ANY TASK FOR NOW  YOUR TASK IS COMPLETED , 
'''



async def create_account_agent(browser_context :BrowserContext):

    logging.info("Running create account hook")
    browser_context = browser_context
    llm = ChatOpenAI(
    model="gpt-4.1",
    temperature=0.0,
    api_key=openai_api_key
    )
    
    job_agent_2 = JobAgent(
                task=task_2,
                llm=llm,
                browser=browser_context,
                controller=None ,
                sensitive_data=None,

            )


    job_agent_2.initiate_agent_task()
    await job_agent_2.run_agent()
    logging.info("Agent task2 completed")



