import pytest

from utils.helper import fill_basic_info


@pytest.mark.parametrize(
    "image_path, expected",
    [
        ("data/valid_image.jpg", "success"),
        ("data/invalid_file.pdf", "invalid"),
        ("data/large_image.png", "invalid"),
    ],
)
def test_employee_image_upload(add_employee_page, image_path, expected):
    fill_basic_info(add_employee_page, "Image", "Test")

    add_employee_page.upload_employee_image(image_path)

    if expected == "success":
        add_employee_page.click_save()
        assert add_employee_page.is_success_visible()
    else:
        assert add_employee_page.is_invalid_image_error()
