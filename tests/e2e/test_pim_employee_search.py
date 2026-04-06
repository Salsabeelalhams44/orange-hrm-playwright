import pytest

from utils.helper import generate_unique_first_name

# ===== Search by ID =====


def test_search_by_valid_employee_id(pim_page, add_employee_page):
    """Search by existing employee ID returns correct result."""
    emp_id = add_employee_page.get_employee_id()  # get ID at runtime
    add_employee_page.fill_first_name("Search")
    add_employee_page.fill_last_name("ByID")
    add_employee_page.click_save()
    add_employee_page.page.wait_for_url("**/pim/viewPersonalDetails/**", timeout=60000)

    pim_page.search_employee_by_id(emp_id)

    assert pim_page.is_employee_in_results_by_id(emp_id)
    assert not pim_page.is_no_records_found()


@pytest.mark.parametrize(
    ("emp_id", "expected"),
    [
        ("000000", "no_results"),  # non-existing ID
        ("@#$%^&", "no_results"),  # special characters
        ("", "has_results"),  # empty returns all
    ],
)
def test_search_by_employee_id_negative(pim_page, emp_id, expected):
    """Search by invalid employee ID."""
    pim_page.search_employee_by_id(emp_id)

    if expected == "no_results":
        assert pim_page.is_no_records_found()
    else:
        assert pim_page.get_search_results_count() > 0


# ===== Search by Name =====


def test_search_by_valid_employee_name(pim_page, add_employee_page):
    """Search by existing employee name returns correct result."""
    add_employee_page.fill_first_name("Findme")
    add_employee_page.fill_last_name("Employee")
    add_employee_page.click_save()
    add_employee_page.page.wait_for_url("**/pim/viewPersonalDetails/**", timeout=60000)

    pim_page.search_employee_by_name("Findme")

    assert pim_page.is_employee_in_results_by_name("Findme")
    assert not pim_page.is_no_records_found()


@pytest.mark.parametrize(
    ("emp_name", "expected"),
    [
        ("ZZZNOBODYHASTHISNAME", "no_results"),  # non-existing name
        ("@#$%^&", "no_results"),  # special characters
        ("123456789", "no_results"),  # numbers only
        ("", "has_results"),  # empty returns all
    ],
)
def test_search_by_employee_name_negative(pim_page, emp_name, expected):
    """Search by invalid employee Name."""
    pim_page.search_employee_by_name(emp_name)

    if expected == "no_results":
        assert pim_page.is_no_records_found()
    else:
        assert pim_page.get_search_results_count() > 0


def test_search_by_partial_name(pim_page, add_employee_page):
    """Search by partial name returns matching results."""
    unique_name = generate_unique_first_name()
    add_employee_page.fill_first_name(unique_name)
    add_employee_page.fill_last_name("Employee")
    add_employee_page.click_save()
    add_employee_page.page.wait_for_url("**/pim/viewPersonalDetails/**", timeout=60000)

    pim_page.search_employee_by_name(unique_name[:6])

    assert pim_page.get_search_results_count() > 0
    assert pim_page.is_employee_in_results_by_name(unique_name)
