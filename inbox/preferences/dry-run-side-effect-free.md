---
observed: 2026-10-15
source-session: host Claude Code — OYM AI-Coach, Data Bazaar loader (COACH-209), NER redaction cache
candidate-type: preference
confidence: high
status: new
---

AJ holds "dry run touches nothing" as a hard property of a batch job, not a
convenience. When Claude built a GCS cache for NER spans and let dry runs
write it (arguing the objects held only hashes and offsets, so warming the
cache was free), a review flagged the broken promise and AJ chose "writes
only with --execute" over "always" and over an explicit opt-in flag, even
though it means the first production night runs cold and may miss the
60-minute task timeout.

Her reasoning, as Claude put it and she accepted: the promise is what makes
the dry run safe for the next on-call to run anywhere under any credentials;
a warm cache is not worth trading that away.

Apply: any side effect in a dry-run path is a defect to flag, regardless of
how harmless the payload looks. Gate writes on the explicit execute switch;
solve cold-start costs elsewhere (timeouts, one-off warm runs).
