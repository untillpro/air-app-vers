---
uspecs.registered_at: 2026-02-02T13:35:34Z
uspecs.change_id: 260202-validate-config-and-manifest-consistency
uspecs.baseline: 0888a8ed0ab333bd7436a18e6b14ab313bcdf814
uspecs.archived_at: 2026-02-02T14:21:23Z
---

# Change request: Validate config.yml structure and manifest file consistency

## Why

The current validation does not verify that manifest files in the `manifests/` directory correspond to valid app-environment combinations defined in `config.yml`. This can lead to orphaned manifest files or missing manifests for configured apps, causing deployment issues.

## What

Update config.yml structure and validation logic:

1. **Config.yml structure enforcement:**
   - Structure must be exactly `apps:` containing list of apps with `name` and `environments` list
   - Names must be valid for use in filenames (no spaces, no special characters)

2. **Cross-validation between config.yml and manifests/:**
   - Error if a `.yml` file in `manifests/` doesn't match any app-environment in config.yml
   - Error if an app-environment in config.yml has no corresponding manifest file

3. **Filename format:** `{app}--{environment}.yml` (e.g., `pos--live.yml`)
