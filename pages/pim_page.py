from venv import logger

from playwright.sync_api import Page, expect


class PimPage:
    """Page object for OrangeHRM PIM page actions and verifications.
    Methods:
        navigate_to_pim: Navigate to PIM page and verify presence.
        navigate_to_add_employee: Navigate to Add Employee page from PIM.
    """

    def __init__(self, page: Page):
        self.page = page

    def navigate_to_pim(self):
        """Check navigation to pim page successful by verifying presence of PIM"""
        pim_link = self.page.get_by_role("link", name="PIM")
        expect(pim_link).to_be_visible(timeout=10000)
        pim_link.click()
        actual_title = self.page.get_by_role("heading", name="PIM")
        expect(actual_title).to_be_visible()

    def navigate_to_add_employee(self, selector_role, selector_name):
        self.navigate_to_pim()
        self.page.get_by_role(selector_role, name=selector_name).click()
        actual_title = self.page.get_by_role("heading", name="Add Employee")
        expect(actual_title).to_be_visible()

    def delete_employee_by_id(self, emp_id: str):
        """Delete employee by searching and deleting from employee list."""
        self.navigate_to_pim()
        # Search for employee
        search_input = self.page.locator('.oxd-input-group:has-text("Employee Id") input')
        search_input.fill(emp_id)
        self.page.get_by_role("button", name="Search").click()
        self.page.wait_for_timeout(2000)

        # Check if employee found
        rows = self.page.locator(".oxd-table-row").count()
        if rows > 1:  # header row + at least one result
            self.page.locator(".oxd-checkbox-input").nth(1).check()
            self.page.get_by_role("button", name="Delete Selected").click()
            self.page.get_by_role("button", name="Yes, Delete").click()
            self.page.wait_for_timeout(2000)
            logger.info("Employee %s deleted successfully", emp_id)
        else:
            logger.warning("Employee %s not found for deletion", emp_id)
