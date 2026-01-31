# Smoke Tests for copi.owasp.org

This directory contains smoke tests for the copi.owasp.org application.

## Overview

The smoke tests verify basic functionality of the copi.owasp.org Elixir/Phoenix game engine by running against a Dockerized application and database in the CI pipeline (localhost).

**Note:** We do not need smoke tests for cornucopia.owasp.org because Vite comes with built-in smoke tests that fire up the server and check that all internal links on the website go to live pages.

## What Do Smoke Tests Check?

### For copi.owasp.org (Elixir/Phoenix)
1. Homepage loads successfully (HTTP 200)
2. Cards route is accessible
3. JavaScript assets are being served
4. Server responds with proper HTTP headers

## Running the Tests

### Locally

To run the smoke tests locally, you need to have the copi.owasp.org application running on `http://127.0.0.1:4000` (or set the `COPI_BASE_URL` environment variable to a different URL).

```bash
# Run all smoke tests
python -m unittest tests.scripts.smoke_tests -v

# Run tests for copi.owasp.org
python -m unittest tests.scripts.smoke_tests.CopiSmokeTests -v
```

### With pipenv

```bash
pipenv run python -m unittest tests.scripts.smoke_tests -v
```

### In CI/CD

The smoke tests run automatically in the CI pipeline:
- On every push to `master` that affects the copi.owasp.org application
- Daily at 6 AM UTC (scheduled)
- Manually via workflow dispatch
- As part of the regular test suite on pull requests

**Important:** In the CI pipeline, the smoke tests run against a Dockerized copi.owasp.org application and PostgreSQL database provisioned specifically for the test job on localhost (port 4000).

## Test Structure

```
tests/
└── scripts/
    └── smoke_tests.py  # Main smoke test file
```

## Dependencies

The smoke tests require:
- Python 3.11+
- `requests` library (for HTTP requests)

These are already included in the project's `Pipfile`.

## Related Issue

These smoke tests were created to address [Issue #1265](https://github.com/OWASP/cornucopia/issues/1265).

## CI/CD Integration

Two workflows handle smoke tests:

1. **smoke-tests.yaml** - Dedicated smoke test workflow
   - Runs on schedule (daily)
   - Runs on manual trigger
   - Runs when application code changes
   - Provisions Docker containers (PostgreSQL database + copi.owasp.org application) on localhost
   - Runs smoke tests against the Dockerized application on localhost:4000

2. **run-tests.yaml** - Main test workflow
   - Includes smoke tests along with other tests (unit/integration)
   - Runs on pull requests
   - Note: Currently runs smoke tests without Docker provisioning - may need to be updated

## Expected Results

All tests should pass when the copi.owasp.org application is properly running. If smoke tests fail, it indicates:
- The application is not accessible on the expected URL
- Routes have changed or been removed
- JavaScript is not loading properly
- Server configuration issues
- Database connectivity issues
