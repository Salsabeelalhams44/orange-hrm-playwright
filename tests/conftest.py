import os
import pytest
from playwright.sync_api import Page
from tests.login import login

@pytest.fixture
def page(playwright) -> Page:
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    page = login(page)

    yield page
    context.close()
    browser.close()


@pytest.fixture(scope="function", autouse=True)
def goto(page: Page):
    """Navigate to the base URL before each test."""
    base_url = os.getenv("ORANGEHRM_BASE_URL")
    if not base_url:
        raise ValueError("ORANGEHRM_BASE_URL is not set")
    page.goto(f"{base_url}/web/index.php/auth/login")
    return page

@pytest.fixture
def logged_in_page(page: Page) -> Page:
    return login(page)