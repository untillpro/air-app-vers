# Implementation plan: Reject PR when author is not in DevOps_releasep team

## Construction

- [x] update: [.github/workflows/validate-manifest.yml](../../.github/workflows/validate-manifest.yml)
  - Add new job `check-author` that runs before `validate` job
  - Use `actions/github-script` to check if PR author is member of `DevOps_releasep` team
  - If author is not a team member, fail the job with clear error message
  - Make `validate` job depend on `check-author` with `needs: check-author`
