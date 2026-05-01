Post-Incident Report — Customer Portal Latency Event
Date: March 22, 2025
Author: Dana Torres
Severity: P2
Duration: 3 hours 42 minutes (14:18 - 17:50 UTC)

Summary:
Customer portal response times degraded to 8-12 seconds (normal: 200-400ms) affecting approximately 2,300 active users. No data loss. Root cause was an unindexed database query introduced in the March 20 release.

Timeline:
- 14:18 — Monitoring alerts on p95 latency exceeding 5s threshold
- 14:25 — On-call engineer confirms degradation, begins investigation
- 14:40 — Initial suspicion: increased traffic from new marketing campaign. Traffic analysis disproves this — request volume is normal, response times are slow
- 15:15 — Database team identifies a full table scan on the customer_events table (4.2M rows) triggered by the new activity feed query. This query was added in the March 20 release
- 15:30 — Decision point: roll back the release or add the index? Team debates. Rolling back removes the activity feed feature that marketing has already announced. Adding the index is faster but we've never hot-indexed a table this size in production
- 15:45 — Decision: add the index. Reasoning: the index can be created with CONCURRENTLY flag in Postgres, which doesn't lock the table. Rollback would take ~20 minutes and has its own risk of introducing state inconsistencies with data written since the release
- 16:00 — Index creation begins. Estimated time: 90 minutes for 4.2M rows
- 17:35 — Index creation completes
- 17:50 — Latency returns to normal. Incident resolved

Root Cause:
The activity feed query was tested against the staging database which has 50K rows in customer_events. At that scale, the full table scan completed in 80ms — well within acceptable range. Production has 4.2M rows. The query plan changes at scale — Postgres optimizer chooses a sequential scan when the table fits in memory at small scale but can't at large scale.

What We're Changing:
1. Pre-release query review: Any new query touching tables with >100K rows requires an EXPLAIN ANALYZE against a production-scale dataset. We're building a shadow database with production-volume synthetic data for this purpose.
2. Staging data scale: Staging will be loaded with production-scale data (anonymized) quarterly. This has been requested for two years but was deprioritized. Not anymore.
3. Release-day monitoring: Tightening the latency alert threshold from 5s to 2s for the first 4 hours after any release. Current 5s threshold meant we didn't catch the gradual degradation until it was severe.

Why the Old Process Missed This:
Our code review process checks for SQL injection, N+1 queries, and missing WHERE clauses. It does not check for missing indexes because index requirements are scale-dependent and our reviewers don't have production table sizes memorized. The pre-release query review process above fills this gap.

Decision Log:
- Chose hot-indexing over rollback: correct decision in retrospect. Index creation was uneventful and faster than estimated. Rollback carried migration state risk.
- Chose CONCURRENTLY flag: correct. No table locks, no additional user impact during index creation.
- Did not pursue read replica failover: discussed and rejected. Read replica was already receiving the same unindexed query. Would have moved the problem, not solved it.
