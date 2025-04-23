# Test Helper Scripts

This directory contains various testing helper scripts that are not part of the automated test suite but provide tools for development and debugging.

## Available Scripts

### _manual_test.py

An interactive test script for manually testing the Gmail API client implementation. This script provides a simple command-line interface allowing you to:

- View messages in your inbox
- Send test emails (with or without attachments)

#### Usage

```bash
# Run from the project root directory
python -m tests.src.scripts._manual_test
```

**Note**: You need to create a `credentials.json` file before running this script. Please refer to the setup instructions in the project README.

## Difference from Automated Tests

Unlike the tests in `tests/src/tests/` directory, the scripts here:

- Are not automatically discovered and run by pytest
- May require user interaction
- Don't follow standard test naming conventions
- Are not suitable for running in CI/CD environments

These scripts are helper tools for verifying functionality or debugging manually, not components of the test suite. 