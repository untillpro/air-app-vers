# Implementation plan: Refactor validate.py into separate modules

## Construction

- [x] create: [scripts/validate_manifest.py](../../scripts/validate_manifest.py)
  - add: Manifest validation functions (`validate_manifest`, `validate_semver`, `parse_semver`, `validate_iso8601`, `validate_location_hash`)
  - add: Constants (`SEVERITY_VALUES`, `MATCHER_TYPES`, `VALID_COUNTRIES`)

- [x] create: [scripts/validate_notes.py](../../scripts/validate_notes.py)
  - add: Notes validation functions (`validate_notes_filename`, `validate_notes_file`)
  - add: Constants (`NOTES_MIN_LENGTH`, `NOTES_MAX_LENGTH`, `REQUIRED_LOCALE`)

- [x] create: [scripts/validate_config.py](../../scripts/validate_config.py)
  - add: Config validation functions (`validate_name`, `load_config`, `validate_config`)
  - add: Constant (`REQUIRED_LOCALE`)

- [x] update: [scripts/validate.py](../../scripts/validate.py)
  - remove: All functions moved to new modules
  - add: Imports from `validate_manifest`, `validate_notes`, `validate_config`
  - keep: `get_versions_from_manifests()`, `main()`, cross-validation logic
  - add: Re-exports for backward compatibility

- [x] review: Run tests and verify refactoring works correctly
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

