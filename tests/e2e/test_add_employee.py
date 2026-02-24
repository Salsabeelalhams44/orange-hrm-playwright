from playwright.sync_api import Page, expect

from tests.conftest import login

# ===========================
# 1️⃣ Basic mandatory fields
# ===========================
def test_add_employee_mandatory(page: login):
    # 1️⃣ Login
    page = login
    page.get_by_role("link", name="PIM").click()
    # 2️⃣ Go to Add Employee
    page.get_by_role("button", name=" Add").click()
    # 3️⃣ Fill mandatory fields
    page.get_by_role("textbox", name="First Name").fill("NourTest")
    page.get_by_role("textbox", name="Last Name").fill("NourTwo")
    # 4️⃣ Save and wait for navigation to profile page
    page.get_by_role("button", name="Save").click()
    page.wait_for_url("**/pim/viewPersonalDetails/**")  
    # 5️⃣ Assertions
    expect(page.get_by_role("textbox", name="First Name")).to_have_value("NourTest")
    expect(page.get_by_role("textbox", name="Last Name")).to_have_value("NourTwo")
# ===========================
# 2️⃣ Optional fields
# ===========================
def test_add_employee_optional_fields(page: login):
    # 1️⃣ Login
    page = login
    page.get_by_role("link", name="PIM").click()
    # 2️⃣ Go to Add Employee
    page.get_by_role("button", name=" Add").click()
    # 3️⃣ Fill optinal fields
    page.get_by_role("textbox", name="First Name").fill("Sara")
    page.get_by_role("textbox", name="Middle Name").fill("Ali")
    page.get_by_role("textbox", name="Last Name").fill("Saleh")
    # 4️⃣ Save and wait for navigation to profile page
    page.get_by_role("button", name="Save").click()
    page.wait_for_url("**/pim/viewPersonalDetails/**")
    # 5️⃣ Assertions
    expect(page.get_by_role("textbox", name="Middle Name")).to_have_value("Ali")
# ===========================
# 3️⃣ Empty mandatory fields
# ===========================
def test_add_employee_empty_mandatory(page: login):
    # 1️⃣ Login
    page = login
    page.get_by_role("link", name="PIM").click()
    # 2️⃣ Go to Add Employee
    page.get_by_role("button", name=" Add").click()
    # 3️⃣ Save and wait for navigation to profile page
    page.get_by_role("button", name="Save").click()
    # 4️⃣ Assertions
    expect(page.get_by_text("Required").first).to_be_visible()
    expect(page.get_by_text("Required").nth(1)).to_be_visible()
# ===========================
# 4️⃣ Duplicate Employee ID
# ===========================
def test_add_employee_duplicate_id(page: login):
    # 1️⃣ Login
    page = login
    page.get_by_role("link", name="PIM").click()
    # 2️⃣ Go to Add Employee
    page.get_by_role("button", name=" Add").click()
    # 3️⃣ Fill  fields
    page.get_by_role("textbox", name="First Name").fill("Sarah")
    page.get_by_role("textbox", name="Last Name").fill("Ali")
    page.get_by_role("textbox").nth(4).fill("0222") 
    # 4️⃣ Save and navigate to profile page
    page.get_by_role("button", name="Save").click()
    # 5️⃣ Assertions
    expect(page.get_by_text("Employee Id already exists")).to_be_visible()
# ===========================
# 5️⃣ Cancel Add Employee
# ===========================
def test_add_employee_cancel(page: login):
    # 1️⃣ Login
    page = login
    page.get_by_role("link", name="PIM").click()
    # 2️⃣ Go to Add Employee
    page.get_by_role("button", name=" Add").click()
    # 3️⃣ Fill mandatory fields
    page.get_by_role("textbox", name="First Name").fill("Temporary")
    page.get_by_role("textbox", name="Last Name").fill("User")
    # 4️⃣Cancel Add Employee
    page.get_by_role("button", name="Cancel").click()
    # 5️⃣ Assertions
    page.get_by_role("link", name="Employee List").click()
    page.get_by_role("textbox", name="Type for hints...").first.fill("Temporary")
    page.get_by_role("button", name="Search").click()
    expect(page.get_by_text("InfoNo Records Found")).to_be_visible()
# ===========================
# 6️⃣ Create Login Details Toggle Required
# ===========================
def test_create_login_toggle_requires_password(page: login):
    # 1️⃣ Login
    page = login
    page.get_by_role("link", name="PIM").click()
    # 2️⃣ Go to Add Employee
    page.get_by_role("button", name=" Add").click()
    # 3️⃣ Fill first and last names
    page.get_by_role("textbox", name="First Name").fill("TestLogin")
    page.get_by_role("textbox", name="Last Name").fill("User")
    # 4️⃣ Toggle create login details
    page.locator(".oxd-switch-input").click()
    page.get_by_role("button", name="Save").click()
    # 5️⃣ Assertions: Should show error for missing password
    expect(page.get_by_text("Required").nth(2)).to_be_visible()
    expect(page.get_by_text("Required").nth(3)).to_be_visible()
    expect(page.get_by_text("Passwords do not match")).to_be_visible()
# ===========================
# 7️⃣ Invalid profile picture
# ===========================
def test_invalid_profile_picture(page: login):
    # 1️⃣ Login
    page = login
    page.get_by_role("link", name="PIM").click()
    # 2️⃣ Go to Add Employee
    page.get_by_role("button", name=" Add").click()
    # 3️⃣ Attach invalid file
    page.get_by_role("button", name="Choose File").set_input_files("names.pdf")
    # 4️⃣ Assertion
    expect(page.get_by_text("Invalid file type")).to_be_visible()
# ===========================
# 8️⃣ Field Length / Invalid Characters
# ===========================
def test_field_length_invalid_chars(page: login):
    # 1️⃣ Login
    page = login
    # 2️⃣ Go to Add Employee
    page.get_by_role("link", name="PIM").click()
    page.get_by_role("button", name=" Add").click()
    # 3️⃣ Fill invalid character(too long) in First Name field
    page.get_by_role("textbox", name="First Name").fill("A"*50)  
    # 4️⃣ Assertions
    expect(page.get_by_text("Should not exceed 30")).to_be_visible()
# ===========================
# 9️⃣Edge Case: Duplicate Name Different ID
# ===========================
def test_duplicate_name_different_id(page: Page):
    # 1️⃣ Login
    page = login
    # 2️⃣ Go to Add Employee
    page.get_by_role("link", name="PIM").click()
    page.get_by_role("button", name=" Add").click()
    # 3️⃣ Fill First Name, Last Name and ID(new value)
    page.get_by_role("textbox", name="First Name").fill("Bahaa")
    page.get_by_role("textbox", name="Last Name").fill("Kareem")
    page.get_by_role("textbox").nth(4).fill("9999")  # New ID
    # 4️⃣ Save and navigate to profile page
    page.get_by_role("button", name="Save").click()
    page.wait_for_url("**/pim/viewPersonalDetails/**")
    # 5️⃣ Assertion
    expect(page.get_by_role("textbox", name="First Name")).to_have_value("Bahaa")
    expect(page.get_by_role("textbox", name="Last Name")).to_have_value("Kareem")

# ===========================
# 🔟 Multiple Additions Auto IDs
# ===========================
def test_multiple_additions_auto_ids(page: Page):
    # 1️⃣ Login
    page = login
    page.get_by_role("link", name="PIM").click()
    # Add first employee
    page.get_by_role("button", name=" Add").click()
    page.get_by_role("textbox", name="First Name").fill("Multi1")
    page.get_by_role("textbox", name="Last Name").fill("Test")
    page.get_by_role("button", name="Save").click()
    page.wait_for_url("**/pim/viewPersonalDetails/**")
    first_id = page.get_by_role("textbox").nth(4).input_value()
    # Add second employee
    page.get_by_role("button", name=" Add").click()
    page.get_by_role("textbox", name="First Name").fill("Multi2")
    page.get_by_role("textbox", name="Last Name").fill("Test")
    page.get_by_role("button", name="Save").click()
    page.wait_for_url("**/pim/viewPersonalDetails/**")
    second_id = page.get_by_role("textbox").nth(4).input_value()
    # Assertion
    assert first_id != second_id, "Employee Id already exists"