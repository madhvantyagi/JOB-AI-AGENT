from playwright.sync_api import sync_playwright
import os
from browser_use import Controller  , ActionResult 

@controller.action('upload the resume')
def upload_cv(page, cv_file_path):
    try:
        # First verify the file input exists
        if page.is_visible('input[type="file"]'):
            page.set_input_files('input[type="file"]', cv_file_path)
        elif page.is_visible('button.upload-button'):
            # If button is visible but input is hidden
            page.click('button.upload-button')
            page.set_input_files('input[type="file"]', cv_file_path, force=True)
        else:
            # Try common alternative patterns
            for selector in ['input[accept=".pdf,.docx"]', 'input[name="resume"]', 'input[name="cv"]']:
                if page.is_visible(selector):
                    page.set_input_files(selector, cv_file_path)
                    return True
            return False
        return True
    except Exception as e:
        print(f"Upload failed: {str(e)}")
        return False