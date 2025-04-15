from browser_use import Agent,  Browser,Controller, ActionResult 
from browser_use.browser.context import BrowserContextConfig ,BrowserContext
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import re
import os
import asyncio
import logging


# iniating custom method controller lol
controller = Controller()


logging.basicConfig(level=logging.INFO)


# Load environment variables
load_dotenv()  
openai_api_key = os.getenv('OPENAI_API_KEY')
llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0.0,
)
# Browser Configuration

config = BrowserContextConfig(
    cookies_file="path/to/cookies.json",
    wait_for_network_idle_page_load_time=1.5,
    browser_window_size={'width': 1280, 'height': 1100},
    highlight_elements=True,
    viewport_expansion=-1,
)

browser = Browser()
context = BrowserContext(browser=browser, config=config)
# Basic logic methods
initial_actions = [
    {'open_tab': {'url': ' https://jobright.ai/jobs/recommend '}},
 
]

class MainMemory:
    def __init__(self):
        self.courses = []
        self.course_count = 0
    def add_course(self, course):
        self.courses.append(course)
        self.course_count += 1
    def retrive_courses(self):
        return self.courses








sensitive_data = {'firstname' : 'Madhvan' , 'lastname' : 'Tyagi' , 'email' : 'madhav.harsh@icloud.com' , 'phone' : '5513592567' , 'address' : '26 charles st, jresey city, NJ 07307' , 'city' : 'jersey city' , 'state' : 'NJ' , 'zip' : '07307' ,'linkedIn':'https://www.linkedin.com/in/madhvan-tyagi-10a44a222/'}







agent = Agent(
    browser_context=context,
    task='''
Navigate to the Website

Open the browser and go to the specified URL.

Sign In

Click on the “Sign in with Google” option.

Proceed with the authentication process.

Complete Human Verification

When the website asks for human verification (e.g., a checkbox), wait a few seconds.

Click the checkbox once it becomes interactable.

Adjust Job Sorting Options

Identify the job sort dropdown menu.

Change the setting from “Recommended” to “Top Matched.”

Select and Start Application on the First Job

Once the jobs are sorted correctly, choose the first job listing.

Begin the application process.

Utilize Sensitive Information

When filling out the application form, retrieve the personal details from the sensitive_data object.

Map each application field (e.g., first name, last name, email, phone, address, city, state, zip code, LinkedIn URL) to its corresponding value from the sensitive_data dictionary.

Ensure all fields are correctly and securely populated.

Upload Resume

When prompted with a file upload button during the application process, initiate the upload of the resume file.

Finalize the Application Process

After completing the application, return to the main website.

Click on the “Yes, I applied” button to confirm and complete the job application.
    
    ''',
    initial_actions=initial_actions,
    llm=llm,
    sensitive_data=sensitive_data,
    use_vision=True,             
    controller=controller 
    # Add delay between actions
)




async def main():
    try:
       async with await browser.new_context() as context:
        history = await agent.run()
        input = input("Press Enter to close the browser...")
        print(history)
         
    except Exception as e:    
        print(f"An error occurred: {e}")
    
    finally:
        # Ensure browser is closed properly
        await browser.close()
        logging.info("Browser closed")

# Run the async function
if __name__ == "__main__":
    asyncio.run(main())




   