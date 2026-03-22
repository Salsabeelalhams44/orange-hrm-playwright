import os
import pytest
from playwright.sync_api import Page
from pages.login_page import LoginPage


@pytest.fixture
def page(browser):
    context = browser.new_context()
    playwright_page = context.new_page()
    yield playwright_page
    context.close()


@pytest.fixture(scope="function", autouse=True)
def goto(page: Page):
    """Navigate to the base URL before each test."""
    base_url = os.getenv("ORANGEHRM_BASE_URL")
    if not base_url:
        raise ValueError("ORANGEHRM_BASE_URL is not set")
    page.goto(
        f"{base_url}/web/index.php/auth/login",
        wait_until="networkidle",
        timeout=300000,
    )
    page.wait_for_selector('input[placeholder="Username"]', timeout=30000)
    return page


@pytest.fixture
def login_page(page: Page):
    return LoginPage(page)


@pytest.fixture
def login_success(page: Page):
    page_obj = LoginPage(page)
    page_obj.login_with_valid_credentials("Admin", "admin123")
    return page_obj
