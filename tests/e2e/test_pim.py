import pytest


@pytest.mark.parametrize(
    "selector_role, selector_name",
    [
        ("button", "Add"),
        ("link", "Add Employee"),
    ],
)
def test_navigate_to_add_employee_page_successfully(
    pim_page, selector_role, selector_name
):
    pim_page.navigate_to_add_employee(selector_role, selector_name)
