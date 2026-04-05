from utils.helper import fill_basic_info


def test_add_employee_mandatory(add_employee_page):
    fill_basic_info(add_employee_page, "Mandatory", "Fields")
    add_employee_page.click_save()

    assert add_employee_page.is_success_visible()


def test_add_employee_empty_fields(add_employee_page):
    add_employee_page.click_save()
    assert add_employee_page.is_required_error()


def test_add_employee_cancel(add_employee_page):
    """Test canceling add employee operation returns to employee list."""
    fill_basic_info(add_employee_page, "Temporary", "User")
    add_employee_page.click_cancel()
    # Verify we're back on the employee list page

    assert "viewEmployeeList" in add_employee_page.page.url
