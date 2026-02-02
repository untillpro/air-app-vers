---
uspecs.registered_at: 2026-02-02T11:53:57Z
uspecs.change_id: 260202-use-correct-version-comparison
uspecs.baseline: 1a3077aba114cad5ff9e273de2932ae2f7e9a3a2
uspecs.archived_at: 2026-02-02T11:59:49Z
---

# Change request: Use correct semantic version comparison

## Why

The validation script currently uses string comparison to check if versions are in ascending order (line 81: `if version <= prev_version`). This is incorrect for semantic versioning because string comparison is lexicographic, not numeric. For example, "9.0.0" > "10.0.0" would incorrectly pass validation because "9" > "1" in string comparison, even though 10.0.0 should come after 9.0.0.

## What

Replace string-based version comparison with proper semantic version comparison that parses version strings into numeric tuples (major, minor, patch) for accurate ordering validation.
