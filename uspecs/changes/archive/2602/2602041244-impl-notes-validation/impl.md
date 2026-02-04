# Implementation plan: Implement notes validation

## Construction

- [x] update: [config.yml](../../config.yml)
  - add: `locales` list with supported locale codes (en-en, nl-NL, de-DE, fr-FR, es-ES)

- [x] update: [notes/pos--1.0.0.yml](../../notes/pos--1.0.0.yml), [notes/pos--1.1.0.yml](../../notes/pos--1.1.0.yml), [notes/pos--2.0.0.yml](../../notes/pos--2.0.0.yml)
  - update: Convert from dict format to list format with `name` and `notes` fields

- [x] update: [scripts/validate.py](../../scripts/validate.py)
  - add: `validate_notes_filename()`, `validate_notes_file()` - notes validation functions
  - add: `get_versions_from_manifests()` - helper for cross-validation
  - update: `validate_config()` - parse locales, return 4 values (expected_files, app_names, locales, errors)
  - update: `main()` - integrate notes validation and cross-validation

- [x] update: [scripts/test_validate.py](../../scripts/test_validate.py)
  - update: All existing tests to include locales in config
  - add: Config locales validation tests (2 tests)
  - add: Cross-validation integration tests (6 tests)

- [x] create: [scripts/test_validate_notes.py](../../scripts/test_validate_notes.py)
  - add: `TestValidateNotesFilename` - filename pattern validation (2 tests)
  - add: `TestValidateNotesFile` - notes file structure validation (16 tests)

- [x] review: Run tests and verify all validations work correctly
  - `python -m unittest discover scripts -v` - 64 tests passing

## Quick start

Validate all manifests and notes:

```bash
python scripts/validate.py
```

Run tests:

```bash
python -m unittest discover scripts -v
```
