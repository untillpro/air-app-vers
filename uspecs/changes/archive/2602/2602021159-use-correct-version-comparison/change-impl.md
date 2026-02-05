# Implementation plan: Use correct semantic version comparison

## Construction

- [x] update: [scripts/validate.py](../../../scripts/validate.py)
  - Add `parse_semver()` function to convert version string to numeric tuple (major, minor, patch)
  - Replace string comparison at line 80 with semantic version comparison using parsed tuples
  - Fix `validate_iso8601()` to handle datetime objects (YAML parser auto-converts ISO 8601 strings)
