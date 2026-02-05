---
registered_at: 2026-02-03T13:25:10Z
change_id: 2602031624-refactor-tests-add-example
baseline: e2135ec7ac61f883173e218bd641216c55df39a9
archived_at: 2026-02-03T13:26:01Z
---

# Change request: Refactor tests to table-driven approach and add test example

## Why

Test maintainability was poor with many individual test methods duplicating similar patterns. A working example was needed to demonstrate how to use the validation scripts.

## What

Refactored tests and added working example:

1. **Test refactoring to table-driven approach:**
   - Consolidated 25+ individual test methods into single `test_manifest_validation()` with test cases data structure
   - Each test case specifies name, content, and expected errors
   - Used `textwrap.dedent` for cleaner multi-line test content
   - Kept 3 specialized tests for edge cases requiring specific assertions
   - Removed unused imports (`SEVERITY_VALUES`, `MATCHER_TYPES`, `VALID_COUNTRIES`)
   - Renamed `TestMain` class to `TestValidation`

2. **Added test example in `scripts/test_example/`:**
   - `config.yml`: Configuration for 2 apps (pos, backoffice) with 2 environments each
   - 4 manifest files demonstrating various matcher types and version configurations
   - `run.sh`: Bash script to execute validation on the example

3. **Documentation updates:**
   - Updated README.md with instructions for running the test example
