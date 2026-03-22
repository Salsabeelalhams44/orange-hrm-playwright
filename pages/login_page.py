from playwright.sync_api import Page, expect


class LoginPage:
    """Page object for OrangeHRM login page actions and verifications.
    Methods:
        login_with_credentials: fill username/password + click login.
        login_with_valid_credentials: login + verify dashboard.
        login_fail: verify invalid credentials message.
        empty_username_error: verify required-username message.
        empty_password_error: verify required-password message.
    """

    def __init__(self, page: Page):
        self.page = page

    def login_with_credentials(self, username, password):
        """Login to OrangeHRM using provided credentials"""
        user_input = self.page.get_by_placeholder("Username")
        pass_input = self.page.get_by_placeholder("Password")
        user_input.wait_for(state="visible", timeout=30000)
        pass_input.wait_for(state="visible", timeout=30000)
        user_input.fill(username)
        pass_input.fill(password)
        self.page.get_by_role("button", name="Login").click()

    def login_successful(self):
        """Check if login was successful by verifying presence of Dashboard"""
        # self.page.wait_for_selector("h6:has-text('Dashboard')", timeout=30000)
        actual_title = self.page.get_by_role("heading", name="Dashboard")
        expect(actual_title).to_be_visible()

    def login_with_valid_credentials(self, username, password):
        self.login_with_credentials(username, password)
        self.login_successful()

    def login_fail(self):
        """Check for invalid login error message"""
        error_message = self.page.get_by_text("Invalid credentials")
        expect(error_message).to_be_visible()

    def empty_username_error(self):
        """Check for empty username error message"""
        error_message = self.page.get_by_text("Required").first
        expect(error_message).to_be_visible()

    def empty_password_error(self):
        """Check for empty password error message"""
        error_message = self.page.get_by_text("Required").last
        expect(error_message).to_be_visible()
