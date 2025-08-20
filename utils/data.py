import re
from faker import Faker

_fake = Faker()

_EMAIL_RE = re.compile(
    # very practical email regex (covers common addresses)
    r"^[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@"
    r"(?:[A-Za-z0-9-]+\.)+[A-Za-z]{2,}$"
)

def is_valid_email(value: str) -> bool:
    """Return True if value looks like a valid email address."""
    if not isinstance(value, str) or not value:
        return False
    return _EMAIL_RE.match(value) is not None

def random_email(domain: str = "example.com") -> str:
    """Generate a realistic random email at the given domain."""
    user = _fake.user_name()
    return f"{user}@{domain}"

def full_name(first: str, last: str) -> str:
    """
    Combine first and last names:
    - trims whitespace
    - title-cases each part
    - raises ValueError if either is empty after trimming
    """
    if not isinstance(first, str) or not isinstance(last, str):
        raise ValueError("first and last must be strings")
    f = first.strip()
    l = last.strip()
    if not f or not l:
        raise ValueError("first and last must be non-empty")
    return f.title() + " " + l.title()
