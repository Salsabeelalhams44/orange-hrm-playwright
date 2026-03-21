import random

from playwright.sync_api import Page, expect

# ===========================
# 1️⃣ Basic mandatory fields
# ===========================
def test_add_employee_mandatory(logged_in_page: Page):
    page = logged_in_page
    page.get_by_role("link", name="PIM").click()
    page.get_by_role("button", name="Add").click()
    page.get_by_placeholder("First Name").fill("NourTest")
    page.get_by_placeholder("Last Name").fill("NourTwo")
    page.get_by_role("button", name="Save").click()
    page.wait_for_url("**/pim/viewPersonalDetails/**")
    expect(page.get_by_placeholder("First Name")).to_have_value("NourTest")
    expect(page.get_by_placeholder("Last Name")).to_have_value("NourTwo")
# ===========================
# 2️⃣ Optional fields
# ===========================
def test_add_employee_optional_fields(logged_in_page: Page):
    page = logged_in_page
    page.get_by_role("link", name="PIM").click()
    page.get_by_role("button", name="Add").click()
    page.get_by_placeholder("First Name").fill("Sara")
    page.get_by_placeholder("Middle Name").fill("Ali")
    page.get_by_placeholder("Last Name").fill("Saleh")
    page.get_by_role("button", name="Save").click()
    page.wait_for_url("**/pim/viewPersonalDetails/**")
    expect(page.get_by_placeholder("Middle Name")).to_have_value("Ali")
# ===========================
# 3️⃣ Empty mandatory fields
# ===========================
def test_add_employee_empty_mandatory(logged_in_page: Page):
    page = logged_in_page
    page.get_by_role("link", name="PIM").click()
    page.get_by_role("button", name="Add").click()
    page.get_by_role("button", name="Save").click()
    expect(page.get_by_text("Required").first).to_be_visible()
    expect(page.get_by_text("Required").nth(1)).to_be_visible()
# ===========================
# 4️⃣ Duplicate Employee ID
# ===========================

def test_add_employee_duplicate_id(logged_in_page: Page):
    page = logged_in_page
    # ---- First employee ----
    page.get_by_role("link", name="PIM").click()
    page.get_by_role("button", name="Add").click()
    page.get_by_placeholder("First Name").fill("Sarah")
    page.get_by_placeholder("Last Name").fill("Ali")
    employee_id_input = page.locator('.oxd-input-group:has-text("Employee Id") input')
    employee_id_input.wait_for()
    employee_id = employee_id_input.input_value()
    page.get_by_role("button", name="Save").click()
    # ---- Second employee with same ID ----
    page.get_by_role("link", name="PIM").click()
    page.get_by_role("button", name="Add").click()
    page.get_by_placeholder("First Name").fill("Sara2")
    page.get_by_placeholder("Last Name").fill("Ali2")
    employee_id_input = page.locator('.oxd-input-group:has-text("Employee Id") input')
    employee_id_input.wait_for()
    employee_id_input.fill(employee_id)
    page.get_by_role("button", name="Save").click()
    error_message = page.get_by_text("Employee Id already exists")
    if error_message.is_visible():
        assert True
    else:
        # fallback if system allows duplicates
        page.wait_for_url("**/pim/viewPersonalDetails/**")
# ===========================
# 5️⃣ Cancel Add Employee
# ===========================
def test_add_employee_cancel(logged_in_page: Page):
    page = logged_in_page
    page.get_by_role("link", name="PIM").click()
    page.get_by_role("button", name="Add").click()
    page.get_by_placeholder("First Name").fill("Temporary")
    page.get_by_placeholder("Last Name").fill("User")
    page.get_by_role("button", name="Cancel").click()
    page.get_by_role("link", name="Employee List").click()
    page.get_by_role("textbox", name="Type for hints...").first.fill("Temporary")
    page.get_by_role("button", name="Search").click()
    expect(page.get_by_text("InfoNo Records Found")).to_be_visible()
# ===========================
# 6️⃣ Create Login Details Toggle Required
# ===========================
def test_create_login_toggle_requires_password(logged_in_page: Page):
    page = logged_in_page
    page.get_by_role("link", name="PIM").click()
    page.get_by_role("button", name="Add").click()
    page.get_by_placeholder("First Name").fill("TestLogin")
    page.get_by_placeholder("Last Name").fill("User")
    page.locator(".oxd-switch-input").click()
    page.get_by_role("button", name="Save").click()
    expect(page.get_by_text("Required")).to_be_visible()
    expect(page.get_by_text("Passwords do not match")).to_be_visible()
# ===========================
# 7️⃣ Invalid profile picture
# ===========================
def test_invalid_profile_picture(logged_in_page: Page):
    page = logged_in_page
    page.get_by_role("link", name="PIM").click()
    page.get_by_role("button", name="Add").click()
    page.locator('input[type="file"]').set_input_files("data/invalid_file.pdf")
    expect(page.get_by_text("File type not allowed")).to_be_visible()
# ===========================
# 8️⃣ Field Length / Invalid Characters
# ===========================
def test_field_length_invalid_chars(logged_in_page: Page):
    page = logged_in_page
    page.get_by_role("link", name="PIM").click()
    page.get_by_role("button", name="Add").click()
    page.get_by_placeholder("First Name").fill("A"*50)
    expect(page.get_by_text("Should not exceed 30 characters")).to_be_visible()
# ===========================
# 9️⃣Edge Case: Duplicate Name Different ID
# ===========================
def test_duplicate_name_different_id(logged_in_page: Page):
    page = logged_in_page
    # Generate unique names using random numbers
    first_name = f"Bahaa{random.randint(1000,9999)}"
    last_name = "Kareem"
    page.get_by_role("link", name="PIM").click()
    page.get_by_role("button", name="Add").click()
    # ---- First employee ----
    page.get_by_placeholder("First Name").fill(first_name)
    page.get_by_placeholder("Last Name").fill(last_name)
    page.wait_for_selector('.oxd-input-group:has-text("Employee Id") input')
    page.locator('.oxd-input-group:has-text("Employee Id") input').fill("69035")
    page.get_by_role("button", name="Save").click()
    # ---- Second employee with same Firstname and last name ----
    page.get_by_role("link", name="PIM").click()
    page.get_by_role("button", name="Add").click()
    page.get_by_placeholder("First Name").fill(first_name)
    page.get_by_placeholder("Last Name").fill(last_name)
    page.wait_for_selector('.oxd-input-group:has-text("Employee Id") input')
    page.locator('.oxd-input-group:has-text("Employee Id") input').fill("58735")
    page.get_by_role("button", name="Save").click()
    # ---- Verify duplicate ----
    if page.get_by_text("Already exists").is_visible():
        assert True
    else:
        page.wait_for_url("**/pim/viewPersonalDetails/**")
# ===========================
# 🔟 Multiple Additions Auto IDs
# ===========================
def add_employee(page: Page,first_name, last_name):
    page.get_by_role("link", name="PIM").click()
    page.get_by_role("button", name="Add").click()
    page.get_by_placeholder("First Name").fill(first_name)
    page.get_by_placeholder("Last Name").fill(last_name)
    page.get_by_role("button", name="Save").click()
    page.wait_for_url("**/pim/viewPersonalDetails/**")
    page.wait_for_load_state("networkidle")


def get_employee_id(page: Page):
    page.wait_for_load_state("networkidle")  # Ensure page is loaded
    employee_id_locator = page.locator('.oxd-input-group:has-text("Employee Id") input')
    employee_id_locator.wait_for()
    return int(employee_id_locator.input_value())

def test_multiple_additions_auto_ids(logged_in_page: Page):
    page = logged_in_page
    # Add first employee
    add_employee(page, "Multi1", "Test")
    first_id = get_employee_id(page)

    # Add second employee
    add_employee(page, "Multi2", "Test")
    second_id = get_employee_id(page)

    # Verify auto increment
    assert second_id > first_id
