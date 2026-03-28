from utils.helper import fill_basic_info


def test_duplicate_employee_id(pim_page, add_employee_page):
    fill_basic_info(add_employee_page, "Duplicate", "ID")

    emp_id = add_employee_page.get_employee_id()
    add_employee_page.click_save()

    pim_page.navigate_to_add_employee(selector_role="button", selector_name="Add")
    emp2 = add_employee_page.page
    fill_basic_info(emp2, "Duplicate", "ID2")
    emp2.fill_employee_id(emp_id)

    emp2.click_save()

    assert emp2.is_duplicate_id_error()
