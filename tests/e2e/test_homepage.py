import re
from playwright.sync_api import expect

# Exact title seen in your run; allow optional trailing space
TITLE_PATTERN = re.compile(r"^Innovative Security Automation Solutions for Smart Cities MENAT\s*$")

def test_homepage_loads(page):
    page.goto("https://veertec.com", wait_until="load", timeout=60000)
    expect(page).to_have_title(TITLE_PATTERN)
