from pages.PIM.add_employee_page import AddEmployeePage
from utils.helper import fill_basic_info


def test_duplicate_employee_id(pim_page, add_employee_page):
    duplicate_id = "99999"

    fill_basic_info(add_employee_page, "Duplicate", "ID")

    add_employee_page.fill_employee_id(duplicate_id)
    add_employee_page.click_save()

    add_employee_page.page.wait_for_url("**/pim/viewPersonalDetails/**", timeout=15000)

    pim_page.navigate_to_add_employee(selector_role="button", selector_name="Add")
    add_employee_page2 = AddEmployeePage(
        pim_page.page
    )  # create new AddEmployeePage instance

    fill_basic_info(add_employee_page2, "Duplicate", "ID2")
    add_employee_page2.fill_employee_id(duplicate_id)

    add_employee_page2.click_save()

    assert add_employee_page2.is_duplicate_id_error()
