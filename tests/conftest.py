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
    """Fixture to navigate to the base URL."""
    base_url = "https://opensource-demo.orangehrmlive.com/"
    page.goto(base_url)
