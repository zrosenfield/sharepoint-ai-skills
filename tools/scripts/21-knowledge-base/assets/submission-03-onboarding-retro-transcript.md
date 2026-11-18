Meeting Transcript — Onboarding Retrospective: Cascade Corp
Date: April 1, 2025
Attendees: Marcus Chen, Lisa Park, Dev Okafor

Marcus Chen: Let's do the retro on Cascade. They went live last Friday, day 87. Technically within the 90-day window but it was tight. What happened?

Lisa Park: Phase 1 went fine. Standard environment, clean data migration. The issue was Phase 2 — they had five source systems to integrate, not the three they told us during scoping.

Dev Okafor: And two of those were legacy on-prem systems with no modern API. We had to build custom connectors.

Marcus Chen: This is the recurring pattern. Customers understate their integration complexity during sales. By the time we discover the real scope, we're already in Phase 2 with a committed timeline.

Lisa Park: Should we add a technical discovery step before Phase 1 starts? Like a week-long scoping engagement?

Marcus Chen: I've been thinking about this. The problem is sales doesn't want to add time before contract close, and customers don't want to pay for scoping before they've committed. What if we built it into the first week of Phase 1? Call it "Integration Discovery Sprint." Same 90-day timeline, but the first 5 days are dedicated to mapping every system they need to connect, confirming API availability, and flagging anything that needs custom work.

Dev Okafor: That would have caught the Cascade situation on day 5 instead of day 35.

Marcus Chen: Exactly. And then we can adjust the Phase 2 timeline within the overall 90 days instead of scrambling at the end.

Lisa Park: What about the customers where integration discovery reveals they need more than 90 days?

Marcus Chen: Then we have an honest conversation early. A timeline extension on day 5 is a project management conversation. A timeline extension on day 60 is a trust conversation. I'd rather have the first one.

Dev Okafor: The other thing about Cascade — their IT team was unresponsive for two weeks in Phase 2. We couldn't get credentials for the legacy systems. Should we have an escalation path for that?

Marcus Chen: We do, but it's informal. I pinged their VP of Engineering directly. We need to formalize it. Going forward, the kickoff meeting should establish an escalation contact on the customer side — someone with authority to unblock IT resource allocation. Add it to the kickoff template.

Lisa Park: And the training phase — did they feel ready at go-live?

Marcus Chen: Honestly, Phase 3 was compressed because Phase 2 ran long. We did two training sessions instead of the usual four. I'm not thrilled about it. We're going to check in with them at 30 days post-launch and offer supplemental training if needed. But this is exactly why the integration discovery sprint matters — protect Phase 3 by getting accurate scope in Phase 1.

Dev Okafor: One more thing — the custom connectors we built for their legacy systems. Are those reusable?

Marcus Chen: The Oracle connector probably is, it's fairly standard. The AS/400 one is too specific. But let's document both in the integration playbook so the next team doesn't start from zero.
