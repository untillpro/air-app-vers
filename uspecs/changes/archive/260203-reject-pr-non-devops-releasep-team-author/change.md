---
registered_at: 2026-02-03T13:31:01Z
change_id: 2602031630-reject-pr-non-team-author
baseline: 5ad9a68bd71724cc06b53716fccd9930e69e358f
archived_at: 2026-02-03T16:37:43Z
---

# Change request: Reject PR when author is not in DevOps_releasep team

## Why

Only members of the `DevOps_releasep` team should be allowed to create pull requests for version control changes. Unauthorized PRs need to be automatically rejected to enforce access control.

## What

Add PR author validation:

- Check if PR author is a member of the `DevOps_releasep` team
- Reject the PR with an appropriate message if the author is not a team member
- Allow the PR to proceed if the author is a valid team member
