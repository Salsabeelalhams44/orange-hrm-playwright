import re
from playwright.sync_api import Page, expect

def test_login_to_orangehrm(page: Page):

    page.get_by_placeholder("Username").fill("Admin")
    page.get_by_placeholder("Password").fill("admin123")

    page.get_by_role("button", name="Login").click()
    expect(page).to_have_title(re.compile("OrangeHRM"))
