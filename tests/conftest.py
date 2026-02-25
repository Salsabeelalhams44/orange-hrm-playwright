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