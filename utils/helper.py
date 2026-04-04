import uuid

from utils.constants import MAX_USERNAME_LENGTH


def fill_basic_info(page, first="Test", last="User"):
    page.fill_first_name(first)
    page.fill_last_name(last)
    unique_id = str(uuid.uuid4().int)[:6]
    page.fill_employee_id(unique_id)


def generate_valid_unique_username():
    return f"user_{uuid.uuid4().hex[:8]}"  # unique username with 8 chars


def generate_boundary_username():
    unique_part = uuid.uuid4().hex[: MAX_USERNAME_LENGTH - 4]  # 36 chars
    return "user" + unique_part  # exactly 40 chars


def generate_unique_first_name():
    """Generate a unique first name for test employees."""
    return f"Test{uuid.uuid4().hex[:6]}"
