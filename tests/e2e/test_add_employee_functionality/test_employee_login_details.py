import pytest
from utils.helper import (
    fill_basic_info,
    generate_boundary_username,
    generate_valid_unique_username,
)
from utils.constants import (
    MAX_PASSWORD_LENGTH,
    MAX_USERNAME_LENGTH,
    MIN_PASSWORD_LENGTH,
    MIN_USERNAME_LENGTH,
)


@pytest.mark.parametrize(
    "username, expected",
    [
        ("valid", "success"),  # valid login details
        ("", "error"),  # empty username
        ("boundary", "success"),  # boundary
        ("a" * (MAX_USERNAME_LENGTH + 1), "error"),  # username too long
        ("a" * (MIN_USERNAME_LENGTH - 1), "error"),  # username too short
    ],
)
def test_username_validation(add_employee_page, username_type, expected):
    fill_basic_info(add_employee_page)
    if username_type == "valid":
        username = generate_valid_unique_username()
    elif username_type == "boundary":
        username = generate_boundary_username()
    else:
        username = username_type

    add_employee_page.toggle_login_details(True)
    add_employee_page.page.get_by_role("textbox").nth(5).wait_for(
        state="visible", timeout=10000
    )
    add_employee_page.fill_login_details(username, "Password123!", "Password123!")

    add_employee_page.click_save()

    if expected == "success":
        assert add_employee_page.is_success_visible()
    else:
        assert add_employee_page.is_username_error_visible()


@pytest.mark.parametrize(
    "password, expected",
    [
        ("Password123!", "success"),  # valid password
        ("1234567", "error"),  # no letters
        ("NOLOWERCASE1!", "error"),  # no lowercase
        ("", "error"),  # empty password
        ("a" * (MIN_PASSWORD_LENGTH - 1), "error"),  # < 7 chars
        ("a" * (MAX_PASSWORD_LENGTH + 1), "error"),  # > 64 chars
    ],
)
def test_password_validation(add_employee_page, password, expected):
    fill_basic_info(add_employee_page)

    add_employee_page.toggle_login_details(True)
    add_employee_page.page.get_by_role("textbox").nth(5).wait_for(
        state="visible", timeout=10000
    )
    add_employee_page.fill_login_details(
        generate_valid_unique_username(), password, password
    )

    add_employee_page.click_save()

    if expected == "success":
        assert add_employee_page.is_success_visible()
    else:
        assert add_employee_page.is_password_error_visible()


def test_password_mismatch(add_employee_page):
    fill_basic_info(add_employee_page)

    add_employee_page.toggle_login_details(True)
    add_employee_page.page.get_by_role("textbox").nth(5).wait_for(
        state="visible", timeout=10000
    )
    add_employee_page.fill_login_details(
        generate_valid_unique_username(), "Password123!", "Password1234!"
    )

    add_employee_page.click_save()

    assert add_employee_page.is_password_mismatch_error()


@pytest.mark.parametrize("status", ["Enabled", "Disabled"])
def test_employee_status(add_employee_page, status):
    fill_basic_info(add_employee_page)

    add_employee_page.toggle_login_details(True)
    add_employee_page.page.get_by_role("textbox").nth(5).wait_for(
        state="visible", timeout=10000
    )

    add_employee_page.fill_login_details(
        generate_valid_unique_username(), "Password123!", "Password123!"
    )
    add_employee_page.set_employee_status(status)

    add_employee_page.click_save()

    assert add_employee_page.is_success_visible()


def test_status_default_enabled(add_employee_page):
    fill_basic_info(add_employee_page)

    # Enable login details
    add_employee_page.toggle_login_details(True)
    add_employee_page.page.get_by_role("textbox").nth(5).wait_for(
        state="visible", timeout=10000
    )

    # Verify default status
    assert add_employee_page.which_status_type_selected() == "Enabled"


def test_status_switch_to_disabled(add_employee_page):
    fill_basic_info(add_employee_page)

    # Enable login details
    add_employee_page.toggle_login_details(True)
    add_employee_page.page.get_by_role("textbox").nth(5).wait_for(
        state="visible", timeout=10000
    )

    # Change status
    add_employee_page.set_employee_status("Disabled")

    assert add_employee_page.which_status_type_selected() == "Disabled"
