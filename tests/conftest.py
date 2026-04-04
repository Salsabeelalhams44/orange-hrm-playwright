import os
from asyncio.log import logger

import pytest
from playwright.sync_api import Page

from pages.login_page import LoginPage
from pages.PIM.add_employee_page import AddEmployeePage
from pages.pim_page import PimPage


@pytest.fixture
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
    return context.new_page()


@pytest.fixture(autouse=True)
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
def logged_in_page(login_page: LoginPage):
    username = os.getenv("ORANGEHRM_USERNAME", "Admin")
    password = os.getenv("ORANGEHRM_PASSWORD", "admin123")
    login_page.login_with_valid_credentials(username, password)

    yield login_page.page

    # TEARDOWN
    login_page.logout()
    logger.info("Cleanup: logged out successfully")


@pytest.fixture
def pim_page(logged_in_page: Page):
    return PimPage(logged_in_page)


@pytest.fixture
def add_employee_page(pim_page: PimPage):
    pim_page.navigate_to_add_employee("button", "Add")
    emp_page = AddEmployeePage(pim_page.page)

    # Capture display Employee ID before test runs
    emp_id = emp_page.get_employee_id()
    logger.info("Captured employee ID for cleanup: %s", emp_id)

    yield emp_page  # ← test runs here

    # TEARDOWN
    try:
        if emp_id:
            pim_page.delete_employee_by_id(emp_id)
        else:
            logger.info("Cleanup: no employee to delete")
    except Exception as e:
        logger.warning("Cleanup failed for employee %s: %s", emp_id, e)


@pytest.fixture(autouse=True)
def increase_timeout(page: Page):
    page.set_default_timeout(60000)  # 60s for all actions
    page.set_default_navigation_timeout(90000)  # 90s for navigation
