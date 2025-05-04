import os
import logging
from browser_use import Controller, ActionResult, Browser

# Configure logging
logging.basicConfig(level=logging.INFO)
# Define the path to the resume file
RESUME_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'FIles', 'APPLY_RESUME.pdf')
print(RESUME_PATH)
# controller for applying job
job_apply_controller = Controller()

@job_apply_controller.action('upload the cover letter')
async def upload_cover_letter(browser: Browser, cover_letter_path:str):
    try:
        # Use the provided path or default to the resume in Files directory
        if not cover_letter_path:
            cover_letter_path = RESUME_PATH

        # Get the current page
        page = await browser.get_current_page()

        # First verify the file input exists
        if await page.is_visible('input[type="file"]'):
            await page.set_input_files('input[type="file"]', cover_letter_path)
            return ActionResult(success=True, message=f"Uploaded cover letter successfully from {cover_letter_path}")

        elif await page.is_visible('button.upload-button'):
            # If button is visible but input is hidden
            await page.click('button.upload-button')
            await page.set_input_files('input[type="file"]', cover_letter_path, force=True)
            return ActionResult(success=True, message=f"Uploaded cover letter successfully from {cover_letter_path}")

        else:
            # Try common alternative patterns
            for selector in ['input[accept=".pdf,.docx"]', 'input[name="resume"]', 'input[name="cv"]', 'input[name="coverLetter"]']:
                if await page.is_visible(selector):
                    await page.set_input_files(selector, cover_letter_path)
                    return ActionResult(success=True, message=f"Uploaded cover letter successfully from {cover_letter_path} using selector {selector}")

            # If we get here, none of the selectors worked
            return ActionResult(success=False, message=f"Error uploading cover letter: No suitable file input found")

    except Exception as e:
        logging.error(f"Cover letter upload failed: {str(e)}")
        return ActionResult(success=False, message=f"Error uploading the cover letter: {e}")


@job_apply_controller.action('upload the resume')
async def upload_resume(browser: Browser, resume_path :str =RESUME_PATH):
    try:
        # Use the provided path or default to the resume in Files directory
        if not resume_path:
            resume_path = RESUME_PATH

        # Get the current page
        page = await browser.get_current_page()

        logging.info(f"Attempting to upload resume from: {resume_path}")

        # First verify the file input exists
        if await page.is_visible('input[type="file"]'):
            await page.set_input_files('input[type="file"]', resume_path)
            return ActionResult(success=True, message=f"Uploaded resume successfully from {resume_path}")

        elif await page.is_visible('button.upload-button'):
            # If button is visible but input is hidden
            await page.click('button.upload-button')
            await page.set_input_files('input[type="file"]', resume_path, force=True)
            return ActionResult(success=True, message=f"Uploaded resume successfully from {resume_path}")

        else:
            # Try common alternative patterns
            for selector in ['input[accept=".pdf,.docx"]', 'input[name="resume"]', 'input[name="cv"]']:
                if await page.is_visible(selector):
                    await page.set_input_files(selector, resume_path)
                    return ActionResult(success=True, message=f"Uploaded resume successfully from {resume_path} using selector {selector}")

            # If we get here, none of the selectors worked
            return ActionResult(success=False, message=f"Error uploading resume: No suitable file input found")

    except Exception as e:
        logging.error(f"Resume upload failed: {str(e)}")
        return ActionResult(success=False, message=f"Error uploading the resume: {e}")