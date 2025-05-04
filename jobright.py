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
from Controllers.CoverLetter import job_apply_controller
from Agent_i_jobs.subAgents import create_account_agent


logging.basicConfig(level=logging.INFO)

# Load environment variables
load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')

# Browser Configuration
context_config = BrowserContextConfig(
    wait_for_network_idle_page_load_time=1.5,
    browser_window_size={'width': 1280, 'height': 1100},
    highlight_elements=True,
    viewport_expansion=-1,
)
browser_config = BrowserConfig(
    browser_binary_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'  # Replace with your Chrome path
)
browser = Browser(config=browser_config)
context = BrowserContext(browser=browser, config=context_config)

initial_actions = [
    {'open_tab': {'url': 'https://jobright.ai/jobs/recommend'}}
]

# Extract only the important sensitive data from User_Details
sensitive_data = {
    'user_name': User_Details['name'],
    'user_email': User_Details['email'],
    'user_phone': User_Details['phone'],
    'user_address': User_Details['address'],
    'work_authorization': User_Details['work_authorization'],
    'sponsorship': User_Details['sponsorship'],
    'veteran': User_Details['veteran']
}

llm = ChatOpenAI(
    model="gpt-4.1",
    temperature=0.0,
    api_key=openai_api_key
)

task = '''
    Navigate to the Website
    Open the browser and go to the specified URL.

    1.1) Adjust Job Sorting Options
    Identify the job sort dropdown menu on the right top corner of webpage .
    Change the setting from "Recommended" to "Top Matched."
    Select and Start Application on the First Job

    1.2) Once the jobs are sorted correctly, choose the first job listing.
    Begin the application process by clicking on Apply Now.

    1.3) Start Applying Job by Clicking on Apply button

    1.4)After you come to Job application page of company , you have to find Apply now button to start application 
 
 - if button not there :
    1 ) look by scrolling down to bottom of page or try to see if there any other button similar , then just click on it 
    2 ) then start applying application , keep going on you have all the data , use it to fill application
'''



async def main():
    try:
        async with await browser.new_context() as context:
            job_agent = JobAgent(
                task=task,
                llm=llm,
                browser=context,
                controller=job_apply_controller,
                sensitive_data=sensitive_data,
                initial_actions=initial_actions,
               
                )
            job_agent.initiate_agent_task()
            await job_agent.run_agent()
            logging.info("Agent task1 completed")

            # running the login agent if needed
            await create_account_agent(context)

    except Exception as e:
        logging.error(f"An error occurred: {e}")

    finally:
        await browser.close()
        logging.info("Browser closed")

if __name__ == "__main__":
    asyncio.run(main())
