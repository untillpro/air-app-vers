---
registered_at: 2026-02-04T12:56:08Z
change_id: 2602041630-refactor-validate-modules
baseline: 677663c1192e71c106b2a6b2e23e95c5fed7f13f
archived_at: 2026-02-04T12:58:51Z
---

# Change request: Refactor validate.py into separate modules

## Why

The monolithic `validate.py` file has grown to contain validation logic for manifests, notes, and config files. Splitting it into focused modules improves code organization, maintainability, and testability.

## What

Split `scripts/validate.py` into separate modules:

- `validate_manifest.py` - Manifest file validation functions and constants
- `validate_notes.py` - Notes file validation functions and constants
- `validate_config.py` - Config file validation functions and constants
- `validate.py` - Cross-validation logic, main() entry point, and re-exports for backward compatibility
