"""
Sprint 1 - Contact Form Tests
TC-S1-010: Contact form is accessible via navigation
TC-S1-011: All required fields are present
TC-S1-012: Subject dropdown contains all required options
TC-S1-013: Message under 50 characters shows a validation error
TC-S1-014: Successful form submission shows a confirmation message
"""

import pytest
from playwright.sync_api import Page, expect
from conftest import BASE_URL

SUBJECT_OPTIONS = [
    "Customer service",
    "Webmaster",
    "Return",
    "Payments",
    "Warranty",
    "Status of my order",
]

VALID_MESSAGE = (
    "This is a test message that is definitely longer than fifty characters."
)


@pytest.fixture(autouse=True)
def go_to_contact(page: Page):
    page.goto(f"{BASE_URL}/#/contact")
    page.wait_for_load_state("networkidle")


def test_tc_s1_010_contact_form_accessible_via_nav(page: Page):
    """TC-S1-010: Navigating to the contact page via the nav link shows the contact form."""
    # Start from home, click the nav link
    page.goto(BASE_URL)
    page.wait_for_load_state("networkidle")
    page.locator("[data-test='nav-contact']").click()
    page.wait_for_load_state("networkidle")

    expect(page.locator("[data-test='first-name']")).to_be_visible()


def test_tc_s1_011_all_required_fields_are_present(page: Page):
    """TC-S1-011: The contact form contains first name, last name, email,
    subject dropdown, message textarea, and a submit button."""
    expect(page.locator("[data-test='first-name']")).to_be_visible()
    expect(page.locator("[data-test='last-name']")).to_be_visible()
    expect(page.locator("[data-test='email']")).to_be_visible()
    expect(page.locator("[data-test='subject']")).to_be_visible()
    expect(page.locator("[data-test='message']")).to_be_visible()
    expect(page.locator("[data-test='contact-submit']")).to_be_visible()


def test_tc_s1_012_subject_dropdown_contains_required_options(page: Page):
    """TC-S1-012: The subject dropdown includes all six required option values."""
    subject_select = page.locator("[data-test='subject']")
    expect(subject_select).to_be_visible()

    option_texts = subject_select.locator("option").all_inner_texts()
    # Strip and normalise whitespace for comparison
    option_texts = [t.strip() for t in option_texts]

    for expected in SUBJECT_OPTIONS:
        assert any(expected.lower() in opt.lower() for opt in option_texts), (
            f"Expected subject option '{expected}' not found. "
            f"Available options: {option_texts}"
        )


def test_tc_s1_013_short_message_shows_validation_error(page: Page):
    """TC-S1-013: Submitting a message shorter than 50 characters shows a validation error."""
    page.locator("[data-test='first-name']").fill("John")
    page.locator("[data-test='last-name']").fill("Doe")
    page.locator("[data-test='email']").fill("john@example.com")
    page.locator("[data-test='subject']").select_option("Customer service")
    page.locator("[data-test='message']").fill("Too short")
    page.locator("[data-test='contact-submit']").click()

    error = page.locator("[data-test='message-error']")
    expect(error).to_be_visible()
    expect(error).to_contain_text("50")


def test_tc_s1_014_successful_submission_shows_confirmation(page: Page):
    """TC-S1-014: Submitting a valid form shows a confirmation message and hides the form."""
    page.locator("[data-test='first-name']").fill("John")
    page.locator("[data-test='last-name']").fill("Doe")
    page.locator("[data-test='email']").fill("john@example.com")
    page.locator("[data-test='subject']").select_option("Customer service")
    page.locator("[data-test='message']").fill(VALID_MESSAGE)
    page.locator("[data-test='contact-submit']").click()

    # Confirmation message should appear
    success_alert = page.locator(".alert.alert-success")
    expect(success_alert).to_be_visible()
    expect(success_alert).to_contain_text("Thanks for your message")

    # Form fields should no longer be visible
    expect(page.locator("[data-test='contact-submit']")).not_to_be_visible()
