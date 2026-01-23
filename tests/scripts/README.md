# Smoke Tests for OWASP Cornucopia Applications

This directory contains smoke tests for the OWASP Cornucopia project applications.

## Overview

The smoke tests verify basic functionality of both deployed applications:
- **copi.owasp.org** - The Elixir/Phoenix game engine
- **cornucopia.owasp.org** - The SvelteKit card browser website

## What Do Smoke Tests Check?

### For copi.owasp.org (Elixir/Phoenix)
1. Homepage loads successfully (HTTP 200)
2. Cards route is accessible
3. JavaScript assets are being served
4. Server responds with proper HTTP headers

### For cornucopia.owasp.org (SvelteKit)
1. Homepage loads successfully (HTTP 200)
2. Cards browser route (`/cards`) is accessible
3. JavaScript/Svelte bundles are being served
4. Individual card detail pages are accessible (e.g., `/cards/VE2`)
5. Page structure indicates JavaScript execution capability

### Integration Tests
1. Both applications respond within acceptable time limits
2. Both applications are simultaneously accessible

## Running the Tests

### Locally

```bash
# Run all smoke tests
python -m unittest tests.scripts.smoke_tests -v

# Run tests for specific application
python -m unittest tests.scripts.smoke_tests.CopiSmokeTests -v
python -m unittest tests.scripts.smoke_tests.CornucopiaSmokeTests -v

# Run integration tests
python -m unittest tests.scripts.smoke_tests.IntegrationSmokeTests -v
```

### With pipenv

```bash
pipenv run python -m unittest tests.scripts.smoke_tests -v
```

### In CI/CD

Smoke tests run automatically:
- On every push to `master` that affects the applications
- Daily at 6 AM UTC (scheduled)
- Manually via workflow dispatch
- As part of the regular test suite

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

2. **run-tests.yaml** - Main test workflow
   - Includes smoke tests alongside unit and integration tests
   - Runs on pull requests

## Expected Results

All tests should pass when both applications are properly deployed and functioning. If smoke tests fail, it indicates:
- One or both applications are not accessible
- Routes have changed or been removed
- JavaScript is not loading properly
- Server configuration issues
