---
registered_at: 2026-04-02T08:59:58Z
change_id: 2604020859-deny-cyrillic-in-notes
baseline: 4279d0969112740ff0e889a7036c80f388e78a6e
issue_url: https://untill.atlassian.net/browse/AIR-3493
---

# Change request: Deny Cyrillic letters in notes

## Why

When AI translates notes into certain languages, it sometimes produces Cyrillic characters that can be missed during review. To ensure data quality and prevent unintended Cyrillic text from slipping through, Cyrillic letters must be explicitly rejected in notes.

See [issue.md](issue.md) for details.

## What

Deny Cyrillic letters in notes:

- Add validation that rejects notes containing Cyrillic characters
- Implement corresponding tests
