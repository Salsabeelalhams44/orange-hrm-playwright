from playwright.sync_api import Page, expect

def test_add_employee_mandatory(page: Page):
    # 1️⃣ Login
    page.goto("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    page.get_by_role("textbox", name="Username").fill("Admin")
    page.get_by_role("textbox", name="Password").fill("admin123")
    page.get_by_role("button", name="Login").click()

    # 2️⃣ Go to Add Employee
    page.get_by_role("link", name="PIM").click()
    page.get_by_role("button", name=" Add").click()

    # 3️⃣ Fill mandatory fields
    page.get_by_role("textbox", name="First Name").fill("NourTest")
    page.get_by_role("textbox", name="Last Name").fill("NourTwo")
    page.get_by_role("textbox").nth(4).fill("05214")

    # 4️⃣ Save and wait for navigation to profile page
    page.get_by_role("button", name="Save").click()
    page.wait_for_url("**/pim/viewPersonalDetails/**")  

    # 5️⃣ Assertions
    expect(page.get_by_role("textbox", name="First Name")).to_have_value("NourTest")
    expect(page.get_by_role("textbox", name="Last Name")).to_have_value("NourTwo")
    expect(page.get_by_role("textbox").nth(4)).to_have_value("05214")

def test_add_employee_optional_fields(page: Page):
    page.goto("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    page.get_by_role("textbox", name="Username").fill("Admin")
    page.get_by_role("textbox", name="Password").fill("admin123")
    page.get_by_role("button", name="Login").click()

    page.get_by_role("link", name="PIM").click()
    page.get_by_role("button", name=" Add").click()

    page.get_by_role("textbox", name="First Name").fill("Sara")
    page.get_by_role("textbox", name="Middle Name").fill("Ali")
    page.get_by_role("textbox", name="Last Name").fill("Saleh")
    page.get_by_role("textbox").nth(4).fill("0222")

    page.get_by_role("button", name="Save").click()
    page.wait_for_url("**/pim/viewPersonalDetails/**")

    expect(page.get_by_role("textbox", name="Middle Name")).to_have_value("Ali")


def test_add_employee_empty_mandatory(page: Page):
    page.goto("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    page.get_by_role("textbox", name="Username").fill("Admin")
    page.get_by_role("textbox", name="Password").fill("admin123")
    page.get_by_role("button", name="Login").click()

    page.get_by_role("link", name="PIM").click()
    page.get_by_role("button", name=" Add").click()

    page.get_by_role("button", name="Save").click()

    # التحقق من ظهور رسائل الخطأ
    expect(page.get_by_text("Required").first).to_be_visible()
    expect(page.get_by_text("Required").nth(1)).to_be_visible()

def test_add_employee_duplicate_id(page: Page):
    page.goto("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    page.get_by_role("textbox", name="Username").fill("Admin")
    page.get_by_role("textbox", name="Password").fill("admin123")
    page.get_by_role("button", name="Login").click()

    page.get_by_role("link", name="PIM").click()
    page.get_by_role("button", name=" Add").click()

    page.get_by_role("textbox", name="First Name").fill("John")
    page.get_by_role("textbox", name="Last Name").fill("Doe")
    page.get_by_role("textbox").nth(4).fill("0222") 

    page.get_by_role("button", name="Save").click()

    # التحقق من رسالة الخطأ للـ duplicate ID
    expect(page.get_by_text("Employee Id already exists")).to_be_visible()



def test_add_employee_cancel(page: Page):
    page.goto("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    page.get_by_role("textbox", name="Username").fill("Admin")
    page.get_by_role("textbox", name="Password").fill("admin123")
    page.get_by_role("button", name="Login").click()

    page.get_by_role("link", name="PIM").click()
    page.get_by_role("button", name=" Add").click()

    page.get_by_role("textbox", name="First Name").fill("Temporary")
    page.get_by_role("textbox", name="Last Name").fill("User")
    page.get_by_role("button", name="Cancel").click()

    # التأكد أن الموظف لم يُضاف
    page.get_by_role("link", name="Employee List").click()
    page.get_by_role("textbox", name="Type for hints...").first.fill("Temporary")
    page.get_by_role("button", name="Search").click()
    expect(page.get_by_text("InfoNo Records Found")).to_be_visible()
