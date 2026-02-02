# Implementation plan: Validate config.yml structure and manifest file consistency

## Construction

- [x] update: [scripts/validate.py](../../../scripts/validate.py)
  - Add `validate_name()` function to check names are in English alphabet lowercase
  - Add `load_config()` function to parse config.yml and extract expected manifest filenames
  - Add `validate_config()` function to validate config.yml structure:
    - Must have `apps` key with list of apps
    - Each app must have `name` (string) and `environments` (list of strings)
      - Each string is English alphabet lowercase
  - Update `main()` to:
    - Load and validate config.yml first
    - Build set of expected manifest filenames from config (`{app}--{env}.yml`)
    - Build set of actual manifest filenames from `manifests/` directory
    - Error if manifest file not in expected set (orphan file)
    - Error if expected file not in actual set (missing manifest)
    - Continue with existing per-file validation for matching files

- [x] update: [scripts/test_validate.py](../../../scripts/test_validate.py)
  - Add `TestValidateName` class with tests for name validation
  - Add `TestLoadConfig` class with tests for config.yml parsing
  - Add `TestValidateConfig` class with tests for config structure validation
    - Including edge cases: None config, apps not a list, app not a dict, environments not a list
  - Add `TestMain` class with integration tests for config/manifest consistency:
    - Test orphan manifest file detection
    - Test missing manifest file detection
    - Test valid config with matching manifests
    - Test invalid app/environment names
    - Test manifests directory not found
    - Test multiple errors

- [x] create: [scripts/test_validate_manifest.py](../../../scripts/test_validate_manifest.py)
  - Add edge case tests for type validation:
    - Test versions is list instead of dict
    - Test matchers is not a list
    - Test matcher entry is not a dict
    - Test empty file, null versions, duplicate versions

- [x] update: [.github/workflows/validate-manifest.yml](../../../.github/workflows/validate-manifest.yml)
  - Add `config.yml` to the paths that trigger validation workflow (already present)
  - Update test command to use test discovery: `python -m unittest discover scripts -v`
    - Automatically runs both test_validate.py and test_validate_manifest.py

## Testing

Run all tests (60 tests total):

```bash
python -m unittest discover scripts -v
```

## Quick start

Validate manifests against config:

```bash
python scripts/validate.py
```

Example config.yml structure:

```yaml
apps:
  - name: pos
    environments:
      - live
      - staging
  - name: backoffice
    environments:
      - live
```

This generates expected manifest files:

- `manifests/pos--live.yml`
- `manifests/pos--staging.yml`
- `manifests/backoffice--live.yml`

## Edge Cases Covered

The implementation includes robust type checking and edge case handling:

**Config validation:**

- None/missing config
- Invalid YAML syntax
- Missing or empty 'apps' key
- apps is not a list
- app entry is not a dict
- Missing app name or environments
- environments is not a list
- Invalid names (uppercase, numbers, special chars)

**Manifest validation:**

- Invalid YAML syntax
- Missing or null 'versions' key
- versions is a list instead of dict
- Invalid semantic version format
- Versions not in ascending order
- Missing or invalid timestamps
- Missing matchers field
- matchers is not a list
- matcher entry is not a dict
- Invalid matcher types, severity values
- Invalid country codes, location hashes
- Missing default matcher
