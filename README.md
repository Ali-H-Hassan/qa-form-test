# VEER Form Test - Automated Contact Form Validation

Comprehensive test automation solution for validating form functionality on veertec.com

## Project Overview

This project implements automated testing for the "Get in Touch with VEER" contact form on the veertec.com website. The test suite validates form field requirements, specifically ensuring that the Company Email field is properly validated when left empty.

### Test Scenarios
1. Navigate to veertec.com homepage
2. Locate and scroll to the "Get in Touch with VEER" form
3. Fill only First Name and Last Name fields
4. Submit the form with Company Email field empty
5. Verify proper validation error for missing Company Email

## Technology Stack

- **Language:** Python 3.8+
- **Test Framework:** Playwright
- **Test Runner:** pytest
- **Test Data:** Faker library

## Project Structure

```
veer-form-test/
├── tests/
│   ├── e2e/
│   │   ├── test_contact_form.py    # Main form validation test
│   │   └── test_homepage.py        # Homepage loading test
│   └── unit/
│       └── test_data.py            # Unit tests for utility functions
├── utils/
│   ├── __init__.py
│   └── data.py                     # Data generation utilities
├── conftest.py                     # pytest configuration
├── pytest.ini                     # pytest settings
└── README.md
```

## Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation
```bash
# Clone and navigate to project
git clone <your-repository-url>
cd veer-form-test

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install playwright pytest faker
playwright install --with-deps chromium firefox webkit
```

## Running Tests

### Basic Commands
```bash
# Run all tests
pytest

# Run e2e tests only
pytest tests/e2e/

# Run specific test
pytest tests/e2e/test_contact_form.py

# Run with specific browser
pytest --browser chromium tests/e2e/test_contact_form.py

# Run multiple iterations
pytest --iterations 5 tests/e2e/test_contact_form.py
```

### Advanced Options
```bash
# Verbose output
pytest -v

# Generate HTML report
pytest --html=reports/test_report.html

# Run tests in parallel across browsers
pytest -n auto --browser chromium --browser firefox --browser webkit

# Debug mode (visible browser)
pytest --headed tests/e2e/test_contact_form.py
```

## Key Features

### Robust Error Handling
- Automatic retry with exponential backoff for network issues
- Progressive timeout increases for unreliable connections
- Graceful degradation strategies

### Advanced Form Validation
- HTML5 validation API usage instead of text-based assertions
- Multiple validation checks: `required`, `valueMissing`, `:invalid`
- Validation message content verification

### Test Implementation
```python
# Core validation approach
is_required = email_input.evaluate("el => el.required === true")
is_missing = email_input.evaluate("el => el.validity.valueMissing === true") 
is_invalid = email_input.evaluate("el => el.matches(':invalid')")
```

### Utility Functions
- Random test data generation with Faker
- Email validation with regex patterns
- Name formatting and validation helpers

## Cross-Browser Support
Built-in support for Chromium, Firefox, and WebKit browsers.

## Troubleshooting

### Common Issues
**Network Timeouts:** Handled automatically by retry mechanism
**Element Not Found:** Check if form structure changed on website
**Browser Issues:** Reinstall with `playwright install --with-deps chromium`

### Debug Mode
```bash
# Run with debug output
pytest -s --log-cli-level=INFO tests/e2e/test_contact_form.py
```

## CI/CD Integration

```yaml
# Example GitHub Actions
- name: Run Tests
  run: pytest --browser chromium --html=reports/test_report.html
```

## Contributing

- Follow PEP 8 guidelines
- Maintain test coverage for utilities
- Use conventional commit messages
