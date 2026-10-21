---
observed: 2026-10-16
source-session: host Claude Code — OYM AI-Coach, COACH-209 Data Bazaar loader first deploy
candidate-type: preference
confidence: high
status: new
---

## What I observed

After the first successful deploy and verified run of a nightly Cloud Run
job from an unmerged PR branch (the deploy was the only way to test the
image, IAM and Cloud Run end to end), AJ said: "I should not have deployed
it until the code was approved and merged." The deploy-before-merge order
was in the written plan she had agreed to, but once the schedule was live
she treated unreviewed code writing production data nightly as a line
crossed. Resolution she accepted: keep the deployed job as evidence, pause
the schedule until the PR is approved, redeploy from the merged commit,
then resume.

## How I'd codify it

"Production write paths run only from reviewed, merged code. A deploy from
a PR branch is acceptable as a test, not as the thing that runs unattended:
leave the schedule paused until the merge, then redeploy from the merged
commit." Offer this gate proactively whenever a plan has a scheduled or
automated production write before review.

## Confidence rationale

High: explicit statement in her own words, consistent with her CLAUDE.md
principles (git hygiene, rollback story, small atomic commits) and with
the earlier capture gate-on-harm-report-on-cost. Could be wrong only in
scope: it may apply to data-writing jobs specifically rather than to
every deploy.

## Related captures

[[gate-on-harm-report-on-cost]]
