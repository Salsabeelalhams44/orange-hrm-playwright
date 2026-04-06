import pytest

from utils.helper import generate_unique_vacancy_name

# ===== Add Vacancy Tests =====


@pytest.mark.parametrize(
    ("job_title", "activate"),
    [
        ("Software Engineer", True),  # Active
        ("QA Lead", False),  # Inactive
        ("Chief Executive Officer", True),  # Active different title
    ],
)
def test_add_vacancy(recruitment_page, job_title, activate):
    """Add vacancy with different job titles and statuses."""
    vacancy_name = generate_unique_vacancy_name()

    recruitment_page.navigate_to_add_vacancy()
    recruitment_page.fill_vacancy_name(vacancy_name)
    recruitment_page.select_job_title(job_title)
    recruitment_page.fill_hiring_manager()
    recruitment_page.toggle_status(activate)
    recruitment_page.click_save()

    assert recruitment_page.is_success_visible()

    # CLEANUP
    recruitment_page.delete_vacancy_by_name(vacancy_name)


# ===== Validation Tests =====


@pytest.mark.parametrize(
    ("vacancy_name", "job_title"),
    [
        ("", ""),  # both empty
        ("", "QA Lead"),  # empty vacancy name
        (generate_unique_vacancy_name(), ""),  # empty job title
    ],
)
def test_add_vacancy_validation(
    recruitment_page,
    vacancy_name,
    job_title,
):
    """Validate required fields when adding vacancy."""
    recruitment_page.navigate_to_add_vacancy()

    if vacancy_name:
        recruitment_page.fill_vacancy_name(vacancy_name)
    if job_title:
        recruitment_page.select_job_title(job_title)

    recruitment_page.click_save()

    assert recruitment_page.is_required_error_visible()


# ===== Status Tests =====


def test_add_vacancy_default_status_is_active(recruitment_page):
    """Default status when adding vacancy is Active."""
    recruitment_page.navigate_to_add_vacancy()
    assert recruitment_page.is_status_active()


def test_add_vacancy_toggle_status_to_inactive(recruitment_page):
    """Toggle status from Active to Inactive."""
    recruitment_page.navigate_to_add_vacancy()
    recruitment_page.toggle_status(False)
    assert not recruitment_page.is_status_active()
