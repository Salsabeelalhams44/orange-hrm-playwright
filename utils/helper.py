import time
import uuid
from utils.constants import MAX_USERNAME_LENGTH


def fill_basic_info(page, first="Test", last="User"):
    page.fill_first_name(first)
    page.fill_last_name(last)


def generate_valid_unique_username():
    return f"user_{uuid.uuid4().hex[:8]}"  # unique username with 8 chars


def generate_boundary_username():
    unique_part = uuid.uuid4().hex[: MAX_USERNAME_LENGTH - 4]  # 36 chars
    return "user" + unique_part  # exactly 40 chars
