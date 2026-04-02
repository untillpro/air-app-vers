# Implementation plan: Deny Cyrillic letters in notes

## Provisioning and configuration

**Configuration:**

## Construction

- [x] update: [scripts/validate_notes.py](../../../../scripts/validate_notes.py)
  - add: Regex pattern `_CYRILLIC_RE` matching Cyrillic Unicode block (U+0400–U+04FF)
  - add: `detect_cyrillic_text(text)` — scans text line by line and returns the first line containing Cyrillic characters, or None
  - add: Call `detect_cyrillic_text` in `validate_notes_file` after notes length validation, producing error like "Locale '{locale_name}': notes contain Cyrillic characters: \"{line}\""
- [x] update: [scripts/test_validate_notes.py](../../../../scripts/test_validate_notes.py)
  - add: Test full Cyrillic text is flagged
  - add: Test single Cyrillic word mixed with Latin is flagged
  - add: Test mixed Latin and Cyrillic lines are flagged
  - add: Test Latin-only text passes
  - add: Test non-Cyrillic Unicode characters (äöü, ñ, etc.) pass
