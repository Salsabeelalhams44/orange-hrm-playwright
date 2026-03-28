import uuid
from constants import MAX_USERNAME_LENGTH


def fill_basic_info(page, first="Test", last="User"):
    page.fill_first_name(first)
    page.fill_last_name(last)


def generate_valid_unique_username():
    unique_part = uuid.uuid4().hex[:8]  # Generate a unique 8-character string
    return "user" + unique_part


def generate_boundary_username():
    unique_part = uuid.uuid4().hex[: MAX_USERNAME_LENGTH - 4]  # 36 chars
    return "user" + unique_part  # exactly 40 chars
