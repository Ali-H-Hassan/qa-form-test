import pytest
from utils import is_valid_email, random_email, full_name

def test_full_name_happy_path():
    assert full_name("john", "doe") == "John Doe"

def test_full_name_trims_and_titles():
    assert full_name("  aLi  ", "  hASsAn ") == "Ali Hassan"

def test_full_name_raises_on_empty():
    with pytest.raises(ValueError):
        full_name(" ", "doe")
    with pytest.raises(ValueError):
        full_name("john", " ")

def test_is_valid_email_true_cases():
    good = [
        "user@example.com",
        "first.last@sub.domain.org",
        "a+b_c-d@company.co",
    ]
    for e in good:
        assert is_valid_email(e), f"should be valid: {e}"

def test_is_valid_email_false_cases():
    bad = [
        "",
        "no-at-symbol.com",
        "user@",
        "@domain.com",
        "user@domain",
        "user@domain..com",
        "user@.com",
    ]
    for e in bad:
        assert not is_valid_email(e), f"should be invalid: {e}"

def test_random_email_uses_domain_and_is_valid():
    email = random_email(domain="test.local")
    assert email.endswith("@test.local")
    assert is_valid_email(email.replace("@test.local", "@example.com"))
