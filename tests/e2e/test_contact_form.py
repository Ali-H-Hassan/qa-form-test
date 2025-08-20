from playwright.sync_api import expect
from faker import Faker

fake = Faker()

def goto_with_retry(page, url: str, attempts: int = 3, base_timeout_ms: int = 60000):
    """
    Navigate with retries. Uses 'domcontentloaded' (faster) instead of 'load' (waits for all assets).
    Exponential backoff between attempts.
    """
    for i in range(1, attempts + 1):
        try:
            # shorter wait condition; bump timeout each attempt
            page.set_default_navigation_timeout(base_timeout_ms * i)
            page.goto(url, wait_until="domcontentloaded")
            return
        except Exception:
            if i == attempts:
                raise
            # small backoff then try again
            page.wait_for_timeout(1000 * i)

def test_contact_form_requires_company_email(page, iteration):
    # Robust navigation
    goto_with_retry(page, "https://veertec.com", attempts=3, base_timeout_ms=60000)

    # Ensure form fields are present before interacting
    first_name = page.get_by_label("First name")
    last_name = page.get_by_label("Last name")
    submit_btn = page.get_by_role("button", name="Submit")
    email_input = page.get_by_label("Company email")

    # Bring form into view
    first_name.scroll_into_view_if_needed()
    first_name.wait_for(state="visible", timeout=30000)
    last_name.wait_for(state="visible", timeout=30000)
    submit_btn.wait_for(state="visible", timeout=30000)

    # Fill ONLY first & last name (leave Company email empty)
    first_name.fill(fake.first_name())
    last_name.fill(fake.last_name())

    # Submit
    submit_btn.click()

    # Assert Company email is required/invalid (HTML5 validity)
    is_required = email_input.evaluate("el => el.required === true")
    assert is_required, "Company email input is not marked required."

    is_missing = email_input.evaluate("el => el.validity.valueMissing === true")
    assert is_missing, "Expected Company email to be missing (valueMissing)."

    is_invalid = email_input.evaluate("el => el.matches(':invalid')")
    assert is_invalid, "Expected Company email to be :invalid after submit."
