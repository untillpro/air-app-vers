# Implementation plan: Implement Python tests for validation script

## Construction

- [x] create: [scripts/test_validate.py](../../../scripts/test_validate.py)
  - Implement unit tests using Python's unittest framework
  - Test `validate_semver()` function with valid and invalid version formats
  - Test `parse_semver()` function for correct tuple conversion
  - Test `validate_iso8601()` function with string and datetime inputs
  - Test `validate_location_hash()` function with valid and invalid hashes
  - Test `validate_manifest()` function with various manifest scenarios:
    - Valid manifest (should pass)
    - Invalid YAML syntax
    - Missing 'versions' key
    - Invalid semantic version format
    - Versions not in ascending order (test semantic comparison)
    - Missing 'released_at' field
    - Invalid ISO 8601 timestamp
    - Missing 'matchers' field
    - Invalid matcher types
    - Invalid severity values
    - Invalid country codes
    - Invalid location hash format
    - Missing default matcher
  - Use temporary test files for file-based tests

- [x] update: [.github/workflows/validate-manifest.yml](../../../.github/workflows/validate-manifest.yml)
  - Add test execution step before validation to ensure tests pass in CI

- [x] update: [scripts/test_validate.py](../../../scripts/test_validate.py)
  - Add `TestMain` class with integration tests for `main()` function
  - Test valid manifests (exit code 0)
  - Test invalid manifests (exit code 1, error output)
  - Test multiple errors across multiple files
  - Test missing manifests directory
  - Test empty manifests directory

## Quick start

Run tests locally:

```bash
python -m unittest scripts/test_validate.py
```

Run tests with verbose output:

```bash
python -m unittest scripts/test_validate.py -v
```
