from curses import error

from playwright.sync_api import Page, expect


class AddEmployeePage:
    """Page object for OrangeHRM Add Employee page.

    Methods:
        fill_first_name: Fill first name field.
        fill_middle_name: Fill middle name field.
        fill_last_name: Fill last name field.
        fill_employee_id: Fill employee ID field.
        get_employee_id: Retrieve auto-generated employee ID.
        click_save: Click Save button.
        click_cancel: Click Cancel button.
        upload_employee_image: Upload profile image.
        toggle_login_details: Enable/disable login details creation.
        fill_login_details: Fill login credentials and status.
        is_success_visible: Check if success message is visible.
        is_duplicate_id_error: Check if duplicate ID error is visible.
        is_required_error: Check if required field error is visible.
        is_invalid_image_error: Check if invalid image error is visible.
    """

    def __init__(self, page: Page):
        self.page = page

    # =====Fields =======================
    def fill_first_name(self, first_name):
        """Fill the First Name field."""
        self.page.get_by_placeholder("First Name").fill(first_name)

    def fill_middle_name(self, middle_name):
        """Fill the Middle Name field."""
        self.page.get_by_placeholder("Middle Name").fill(middle_name)

    def fill_last_name(self, last_name: str):
        """Fill the Last Name field."""
        self.page.get_by_placeholder("Last Name").fill(last_name)

    def fill_employee_id(self, employee_id):
        """Fill the Employee ID field."""
        employee_id_input = self.page.locator(
            '.oxd-input-group:has-text("Employee Id") input'
        )
        employee_id_input.wait_for(state="visible", timeout=10000)
        employee_id_input.fill(employee_id)

    def get_employee_id(self):
        """Retrieve the auto-generated Employee ID."""
        employee_id_input = self.page.locator(
            '.oxd-input-group:has-text("Employee Id") input'
        )
        employee_id_input.wait_for(state="visible", timeout=10000)
        return employee_id_input.input_value()

    # ===== Actions ====================
    def click_save(self):
        """Click the Save button."""
        self.page.get_by_role("button", name="Save").click()

    def click_cancel(self):
        """Click the Cancel button."""
        self.page.get_by_role("button", name="Cancel").click()

    def upload_employee_image(self, image_path):
        """Upload employee profile image.

        Args:
            image_path: Path to the image file to upload.
        """
        file_input = self.page.locator('input[type="file"]')
        file_input.set_input_files(image_path)
        # Wait for upload to complete (optional, depending on UI feedback)
        self.page.wait_for_timeout(2000)

    def toggle_login_details(self, enable=True):
        switch = self.page.locator(".oxd-switch-input")
        switch.wait_for(state="visible", timeout=10000)
        aria_checked = switch.get_attribute("aria-checked")
        is_enabled = aria_checked == "true"
        if is_enabled != enable:
            switch.click()

    def set_employee_status(self, status):
        """Set employee status in login details.

        Args:
            status: "Enabled" or "Disabled"
        """
        status = status.strip().capitalize()
        if status not in ["Enabled", "Disabled"]:
            raise ValueError("Invalid status")
        self.page.locator(".oxd-radio-wrapper").filter(has_text=status).click()

    def which_status_type_selected(self):
        """Check which status radio button is selected."""
        enabled_radio = self.page.locator(
            '.oxd-radio-wrapper:has-text("Enabled") input'
        )
        if enabled_radio.is_checked():
            return "Enabled"
        return "Disabled"

    def fill_login_details(self, username, password, confirm_password):
        self.page.get_by_role("textbox").nth(5).fill(username)
        self.page.locator('input[type="password"]').first.fill(password)
        self.page.locator('input[type="password"]').nth(1).fill(confirm_password)

    # ===== States ===============

    def is_invalid_image_error(self):
        errors = [
            "File type not allowed",
            "Attachment Size Exceeded",
        ]
        return any(self.page.get_by_text(e).is_visible() for e in errors)

    def is_success_visible(self):
        success_msg = self.page.get_by_text("Successfully Saved")
        expect(success_msg).to_be_visible(timeout=10000)
        return True

    def is_required_error(self):
        return self.page.get_by_text("Required").first.is_visible()

    def is_duplicate_id_error(self):
        error = self.page.get_by_text("Employee Id already exists")
        error.wait_for(state="visible", timeout=10000)
        return error.is_visible()

    def is_username_error_visible(self):
        errors = [
            "Should not exceed 40 characters",
            "Required",
            "Should be at least 5 characters",
            "Username already exists",
        ]
        return any(self.page.get_by_text(e).is_visible() for e in errors)

    def is_password_error_visible(self):
        errors = [
            "Should not exceed 64 characters",
            "Should have at least 7 characters",
            "Your password must contain minimum 1 lower-case letter",
            "Required",
        ]
        return any(self.page.get_by_text(e).is_visible() for e in errors)

    def is_password_mismatch_error(self):
        return self.page.get_by_text("Passwords do not match").is_visible()
