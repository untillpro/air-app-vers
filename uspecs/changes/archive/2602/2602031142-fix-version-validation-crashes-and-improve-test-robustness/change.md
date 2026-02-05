---
registered_at: 2026-02-03T07:59:00Z
change_id: 2602030758-fix-version-validation-crashes-and-improve-test-robustness
baseline: 6f5c7ec9872469ff120a0b0a8ed8fd0d355299c4
archived_at: 2026-02-03T11:42:16Z
---

# Change request: Fix version validation crashes and improve test robustness

## Why

Two critical crashes in validation logic could cause the script to fail instead of reporting errors gracefully when processing malformed manifest files. Additionally, test cleanup was fragile and could leak resources if setUp failed partway through.

## What

Fix validation crashes and improve test reliability:

1. **Version format validation crash fix:**
   - Invalid version formats (e.g., "a.b.c") now skip comparison instead of crashing
   - Only valid versions are compared for ordering
   - Added 5 tests for invalid version format edge cases

2. **Version details type validation crash fix:**
   - Type check added before accessing version details fields
   - Graceful error messages when details is not a dict (e.g., number, string, list, null)
   - Added 1 consolidated test covering multiple invalid types

3. **Test robustness improvements:**
   - Refactored 3 test classes to use `addCleanup` instead of `tearDown`
   - Cleanup now guaranteed even if setUp fails
   - Resources (temp directories, working directory) properly cleaned up in all scenarios
