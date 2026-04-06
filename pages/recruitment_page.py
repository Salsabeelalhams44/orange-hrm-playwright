import logging
import re

from playwright.sync_api import Page

from utils.pw_trace import pw_trace_all

logger = logging.getLogger(__name__)


@pw_trace_all
class RecruitmentPage:
    """Page object for OrangeHRM Recruitment Vacancy page.

    Methods:
        navigate_to_recruitment: Navigate to Recruitment page.
        navigate_to_vacancies: Navigate to Vacancies tab.
        navigate_to_add_vacancy: Navigate to Add Vacancy page.
        fill_vacancy_name: Fill vacancy name field.
        select_job_title: Select job title from dropdown.
        toggle_status: Toggle vacancy status switch.
        is_status_active: Check if status switch is active.
        click_save: Click Save button.
        is_success_visible: Check if save was successful.
        is_required_error_visible: Check if required error is visible.
        delete_vacancy_by_name: Delete vacancy by name for cleanup.
    """

    def __init__(self, page: Page):
        self.page = page

    def navigate_to_recruitment(self):
        """Navigate to Recruitment page."""
        self.page.get_by_role("link", name="Recruitment", exact=True).first.click()
        self.page.wait_for_url("**/recruitment/**", timeout=30000)

    def navigate_to_vacancies(self):
        """Navigate to Vacancies tab."""
        self.navigate_to_recruitment()
        self.page.get_by_role("link", name="Vacancies").click()
        self.page.wait_for_load_state("networkidle")

    def navigate_to_add_vacancy(self):
        """Navigate to Add Vacancy page."""
        self.navigate_to_vacancies()
        self.page.get_by_role("button", name="Add").click()
        self.page.wait_for_load_state("networkidle")
        self.page.locator('.oxd-input-group:has-text("Vacancy Name") input').wait_for(
            state="visible", timeout=30000
        )

    def fill_vacancy_name(self, name: str):
        """Fill vacancy name field."""
        vacancy_input = self.page.locator('.oxd-input-group:has-text("Vacancy Name") input')
        vacancy_input.wait_for(state="visible", timeout=30000)
        vacancy_input.clear()
        vacancy_input.fill(name)

    def select_job_title(self, job_title: str):
        """Select job title from dropdown."""
        self.page.locator("div").filter(has_text=re.compile(r"^-- Select --$")).nth(2).click()
        self.page.get_by_role("option", name=job_title, exact=True).click()

    def fill_hiring_manager(self, manager_name: str = "a"):
        """Fill hiring manager field by typing and selecting first result from autocomplete."""
        hiring_manager_input = self.page.get_by_role("textbox", name="Type for hints...")
        hiring_manager_input.wait_for(state="visible", timeout=30000)
        hiring_manager_input.click()
        hiring_manager_input.fill(manager_name)
        self.page.wait_for_timeout(2000)  # wait for options to load
        # Select first available option
        first_option = self.page.get_by_role("option").first
        first_option.wait_for(state="visible", timeout=15000)
        first_option.click()
        self.page.wait_for_timeout(500)

    def toggle_status(self, activate: bool = True):
        """Toggle vacancy Active status switch on or off."""
        switch = self.page.locator(".oxd-switch-input").first
        switch.wait_for(state="visible", timeout=10000)
        classes = switch.get_attribute("class") or ""
        is_active = (
            "oxd-switch-input--active" in classes and "oxd-switch-input--focus" not in classes
        )
        logger.info(
            "Before toggle - classes: %s, is_active: %s, want: %s",
            classes,
            is_active,
            activate,
        )
        if is_active != activate:
            self.page.locator(".oxd-switch-wrapper label").first.click()
            self.page.wait_for_timeout(500)

    def is_status_active(self) -> bool:
        """Check if Active status switch is currently on."""
        switch = self.page.locator(".oxd-switch-input").first
        switch.wait_for(state="visible", timeout=10000)
        classes = switch.get_attribute("class") or ""
        logger.info("Active status switch classes: %s", classes)
        return "oxd-switch-input--active" in classes and "oxd-switch-input--focus" not in classes

    def click_save(self):
        """Click Save button."""
        save_btn = self.page.get_by_role("button", name="Save")
        save_btn.wait_for(state="visible", timeout=10000)
        save_btn.click()

    def is_success_visible(self) -> bool:
        """Check if vacancy was saved successfully."""
        try:
            self.page.wait_for_url("**/recruitment/addJobVacancy/**", timeout=30000)
            self.page.get_by_role("heading", name="Edit Vacancy").wait_for(
                state="visible", timeout=30000
            )
            return True
        except Exception:  # pylint: disable=broad-exception-caught
            return False

    def is_required_error_visible(self):
        """Check if required field error is visible."""
        return self.page.get_by_text("Required").first.is_visible()

    def delete_vacancy_by_name(self, vacancy_name: str):
        """Delete vacancy by name for cleanup."""
        logger.info("Deleting vacancy: %s", vacancy_name)
        self.navigate_to_vacancies()
        row = self.page.locator(f'.oxd-table-body .oxd-table-row:has-text("{vacancy_name}")')
        if row.count() > 0:
            row.locator("button.oxd-icon-button").first.click()
            self.page.get_by_role("button", name="Yes, Delete").click()
            self.page.wait_for_load_state("networkidle")
            logger.info("Vacancy %s deleted successfully", vacancy_name)
        else:
            logger.warning("Vacancy %s not found for deletion", vacancy_name)
