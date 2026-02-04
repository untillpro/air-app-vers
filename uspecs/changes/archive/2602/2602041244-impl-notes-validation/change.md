---
registered_at: 2026-02-04T11:45:28Z
change_id: 2602041445-impl-notes-validation
baseline: 9c1cf0efcd92245dac1cf10ba5acd35a46f7694e
archived_at: 2026-02-04T12:44:49Z
---

# Change request: Implement notes validation

## Why

The system needs to validate notes files to ensure data integrity and consistency. Notes files contain localized release notes for each app version, and validation is required to ensure proper structure, locale coverage, and cross-referencing with manifests.

## What

Implement validation checks for notes files (notes/*.yml):

- YAML syntax is valid
- File name matches pattern {app}--{version}.yml
- App name in filename exists in config.yml
- Version in filename is valid semantic version
- At least one locale entry exists
- All locale names are defined in config.yml
- No duplicate locale entries in same notes file
- en-en locale is present (required for fallback)
- Each locale has non-empty notes field
- Notes text length is within limits (min 1, max 500 characters)

Implement cross-validation checks:

- For each version in any manifest file, a corresponding notes file exists (notes/{app}--{version}.yml)
- For each notes file, the version is referenced in at least one manifest file
- All notes files use only apps defined in config.yml
- All manifest files use only apps and environments defined in config.yml

Repository structure:

```
air-app-vers/
  config.yml           # Defines all app-environment combinations and locales
  manifests/
    pos--live.yml
  notes/
    pos--1.0.0.yml
    pos--1.1.0.yml
    pos--2.0.0.yml
```

Notes file structure example (notes/pos--1.0.0.yml):

```yaml
locales:
  - name: en-en
    notes: Mandatory update due to critical issues
  - name: nl-NL
    notes: Verplichte update vanwege kritieke problemen
  - name: de-DE
    notes: Obligatorisches Update aufgrund kritischer Probleme
```
