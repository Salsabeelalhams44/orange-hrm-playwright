import os
import pytest
from playwright.sync_api import Page
from pages.login_page import LoginPage
from pages.pim_page import PimPage


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
    page.wait_for_selector('input[placeholder="Username"]', timeout=60000)
    return page


@pytest.fixture
def login_page(page: Page):
    return LoginPage(page)


@pytest.fixture
def logged_in_page(login_page: LoginPage) -> Page:
    username = os.getenv("ORANGEHRM_USERNAME", "admin")
    password = os.getenv("ORANGEHRM_PASSWORD", "admin123")
    login_page.login_with_valid_credentials(username, password)
    return login_page.page


@pytest.fixture
def pim_page(logged_in_page: Page):
    return PimPage(logged_in_page)
