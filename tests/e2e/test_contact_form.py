# Enhanced version with additional improvements

from playwright.sync_api import expect
from faker import Faker
import logging

fake = Faker()
logger = logging.getLogger(__name__)

def goto_with_retry(page, url: str, attempts: int = 3, base_timeout_ms: int = 60000):
    """
    Navigate with retries. Uses 'domcontentloaded' (faster) instead of 'load' (waits for all assets).
    Exponential backoff between attempts.
    """
    for i in range(1, attempts + 1):
        try:
            page.set_default_navigation_timeout(base_timeout_ms * i)
            page.goto(url, wait_until="domcontentloaded")
            logger.info(f"Successfully navigated to {url} on attempt {i}")
            return
        except Exception as e:
            logger.warning(f"Navigation attempt {i} failed: {e}")
            if i == attempts:
                logger.error(f"All {attempts} navigation attempts failed")
                raise
            # small backoff then try again
            page.wait_for_timeout(1000 * i)

def test_contact_form_requires_company_email(page, iteration):
    """
    Test that the contact form properly validates required Company Email field.
    
    This test:
    1. Navigates to the homepage
    2. Locates the contact form
    3. Fills only first/last name (leaving email empty)
    4. Submits the form
    5. Verifies proper HTML5 validation occurs
    """
    logger.info(f"Starting contact form test iteration {iteration}")
    
    # Robust navigation
    goto_with_retry(page, "https://veertec.com", attempts=3, base_timeout_ms=60000)

    # Locate form elements with better error messages
    try:
        first_name = page.get_by_label("First name")
        last_name = page.get_by_label("Last name") 
        submit_btn = page.get_by_role("button", name="Submit")
        email_input = page.get_by_label("Company email")
    except Exception as e:
        logger.error(f"Failed to locate form elements: {e}")
        raise AssertionError("Contact form elements not found - page structure may have changed")

    # Bring form into view and ensure visibility
    first_name.scroll_into_view_if_needed()
    
    # Wait for all elements to be ready
    elements_to_wait = [first_name, last_name, submit_btn, email_input]
    for element in elements_to_wait:
        element.wait_for(state="visible", timeout=30000)

    # Generate test data
    test_first_name = fake.first_name()
    test_last_name = fake.last_name()
    logger.info(f"Using test data: {test_first_name} {test_last_name}")

    # Fill ONLY first & last name (leave Company email empty intentionally)
    first_name.fill(test_first_name)
    last_name.fill(test_last_name)
    
    # Verify the email field is indeed empty before submitting
    email_value = email_input.input_value()
    assert email_value == "", f"Expected email field to be empty, but got: '{email_value}'"

    # Submit the form
    submit_btn.click()
    
    # Give the browser a moment to process validation
    page.wait_for_timeout(500)

    # Assert Company email validation occurs (HTML5 validity)
    is_required = email_input.evaluate("el => el.required === true")
    assert is_required, "Company email input should be marked as required"

    is_missing = email_input.evaluate("el => el.validity.valueMissing === true") 
    assert is_missing, "Company email should trigger valueMissing validation"

    is_invalid = email_input.evaluate("el => el.matches(':invalid')")
    assert is_invalid, "Company email should be in :invalid state after submission"
    
    # Optional: Check if browser shows validation message
    validation_message = email_input.evaluate("el => el.validationMessage")
    assert validation_message, f"Expected validation message, got: '{validation_message}'"
    
    logger.info(f"Contact form validation test iteration {iteration} completed successfully")