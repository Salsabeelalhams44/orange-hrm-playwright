import os
import pytest
from playwright.sync_api import Page
from pages.login_page import LoginPage
from pages.pim_page import PimPage
from pages.PIM.add_employee_page import AddEmployeePage


@pytest.fixture(scope="function")
def context(browser):
    ctx = browser.new_context(
        record_video_dir="videos/",  # saves video for every test
    )
    ctx.tracing.start(screenshots=True, snapshots=True, sources=True)
    yield ctx
    ctx.tracing.stop(path="trace.zip")  # saves trace file
    ctx.close()


@pytest.fixture
def page(context):
    playwright_page = context.new_page()
    yield playwright_page


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
    username = os.getenv("ORANGEHRM_USERNAME", "Admin")
    password = os.getenv("ORANGEHRM_PASSWORD", "admin123")
    login_page.login_with_valid_credentials(username, password)
    return login_page.page


@pytest.fixture
def pim_page(logged_in_page: Page):
    return PimPage(logged_in_page)


@pytest.fixture
def add_employee_page(pim_page: PimPage):
    pim_page.navigate_to_add_employee("button", "Add")
    return AddEmployeePage(pim_page.page)


@pytest.fixture(scope="session", autouse=True)
def set_default_timeout(browser):
    pass


@pytest.fixture(scope="function", autouse=True)
def increase_timeout(page: Page):
    page.set_default_timeout(60000)  # 60s for all actions
    page.set_default_navigation_timeout(90000)  # 90s for navigation
