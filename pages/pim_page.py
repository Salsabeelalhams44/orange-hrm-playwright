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
