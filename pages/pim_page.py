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

    def search_employee_by_id(self, employee_id):
        """Search employee by ID in employee list."""
        self.navigate_to_pim()
        search_input = self.page.locator('.oxd-input-group:has-text("Employee Id") input')
        search_input.wait_for(state="visible", timeout=30000)
        search_input.clear()
        search_input.fill(employee_id)
        self.page.get_by_role("button", name="Search").click()
        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_timeout(2000)  # wait for table to update

    def search_employee_by_name(self, name):
        """Search employee by name in employee list."""
        self.navigate_to_pim()
        name_input = self.page.locator('.oxd-input-group:has-text("Employee Name") input')
        name_input.wait_for(state="visible", timeout=30000)
        name_input.clear()
        name_input.fill(name)
        self.page.wait_for_timeout(1000)  # wait for autocomplete
        self.page.get_by_role("button", name="Search").click()
        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_timeout(2000)  # wait for table to update

    def get_search_results_count(self):
        """Get number of results in employee list table."""
        self.page.wait_for_timeout(2000)  # wait for results to load

        return self.page.locator(".orangehrm-container").get_by_role("row").count()

    def is_no_records_found(self):
        """Check if no records found message is visible."""
        return self.page.locator("#oxd-toaster_1").get_by_text("No Records Found").is_visible()

    def is_employee_in_results_by_name(self, name):
        """Check if specific employee name appears in search results."""
        return self.page.locator(".orangehrm-container").get_by_role("row", name=name).is_visible()

    def is_employee_in_results_by_id(self, employee_id):
        """Check if specific employee ID appears in search results."""
        return self.page.locator(".orangehrm-container").get_by_role("row", name=employee_id).is_visible()
