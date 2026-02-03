---
uspecs.registered_at: 2026-02-02T11:46:13Z
uspecs.change_id: 260202-add-github-job-url-to-pr-comments
uspecs.baseline: 1a3077aba114cad5ff9e273de2932ae2f7e9a3a2
uspecs.archived_at: 2026-02-02T11:50:53Z
---

# Change request: Add GitHub job URL to PR validation failure comments

## Why

When validation fails on a PR, the current comment only says "Please check the workflow logs for details" without providing a direct link. This requires Release Engineers to manually navigate to the Actions tab and find the correct workflow run, which is inefficient and adds friction to the release process.

## What

Enhanced the PR comment functionality in the validation workflow to include a direct URL to the failed GitHub Actions job when validation fails. The comment now displays:
- Clear visual indicators (✅/❌ emojis) for success/failure status
- Direct clickable link to the workflow run when validation fails
- Improved formatting with bold headers for better readability
