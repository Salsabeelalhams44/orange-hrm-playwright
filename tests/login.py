from playwright.sync_api import Page
import os

def login(page: Page) -> Page:
    """Login to OrangeHRM using environment secrets"""
    username = os.getenv("ORANGEHRM_USERNAME")
    password = os.getenv("ORANGEHRM_PASSWORD")
    base_url = os.getenv("ORANGEHRM_BASE_URL")

    page.goto(f"{BASE_URL}/web/index.php/auth/login")
    page.get_by_role("textbox", name="Username").fill(USERNAME)
    page.get_by_role("textbox", name="Password").fill(PASSWORD)
    page.get_by_role("button", name="Login").click()
    return page