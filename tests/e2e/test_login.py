import os
import pytest


@pytest.mark.parametrize(
    "username, password",
    [
        ("admin", "admin123"),
        (os.getenv("ORANGEHRM_USERNAME"), os.getenv("ORANGEHRM_PASSWORD")),
    ],
)
def test_valid_login_to_orangehrm(login_page, username, password):
    login_page.login_with_valid_credentials(username, password)


@pytest.mark.parametrize(
    "username, password, expected_error",
    [
        ("invalid_user", "invalid_pass", "invalid_credentials"),
        # invalid username and invalid password
        ("", "admin123", "empty_username"),  # empty username, valid password
        ("Admin", "", "empty_password"),  # valid username, empty password
        ("", "", "both_empty"),  # empty username and empty password
        (os.getenv("ORANGEHRM_USERNAME"), "wrong_password", "invalid_credentials"),
        # valid username from env, invalid password
        ("wrong_username", os.getenv("ORANGEHRM_PASSWORD"), "invalid_credentials"),
        # invalid username, valid password from env
        ("null", "null", "invalid_credentials"),  # null values
        ("مستخدم عربي", "admin123", "invalid_credentials"),
        # Arabic username, valid password (tests non-Latin characters)
        ("user_latin", "كلمة مرور عربية", "invalid_credentials"),
        # Latin username, Arabic password (tests mixed characters)
    ],
)
def test_invalid_login_to_orangehrm(login_page, username, password, expected_error):
    login_page.login_with_credentials(username, password)
    if expected_error == "empty_username":
        login_page.empty_username_error()
    elif expected_error == "empty_password":
        login_page.empty_password_error()
    elif expected_error == "both_empty":
        login_page.empty_username_error()
        login_page.empty_password_error()
    elif expected_error == "invalid_credentials":
        login_page.login_fail()
