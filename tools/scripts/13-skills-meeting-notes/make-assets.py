"""
make-assets.py — 13-skills-meeting-notes
Generates demo asset files into assets/ subdirectory.
Run from repo root: python tools/scripts/13-skills-meeting-notes/make-assets.py
Or from this folder: python make-assets.py

Assets:
  Q1 Planning Kickoff - 2025-01-14.txt  — ~600-word Teams-style meeting transcript
    4 speakers: Jordan (PM), Alex (Engineering), Sam (Design), Riley (Marketing)
    25-minute meeting, timestamps every 1-3 minutes in [MM:SS] format
    Topics: Q1 OKRs, Project Atlas launch, design review, marketing plan, wrap-up
    Buried action items and decisions — messy, realistic, not a clean summary
"""
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(SCRIPT_DIR, 'assets')
os.makedirs(ASSETS_DIR, exist_ok=True)

def p(name):
    return os.path.join(ASSETS_DIR, name)

# ---------------------------------------------------------------------------
# Meeting transcript
# ---------------------------------------------------------------------------

TRANSCRIPT = """\
Q1 Planning Kickoff
Zava Internal — January 14, 2025
Attendees: Jordan (PM), Alex (Engineering), Sam (Design), Riley (Marketing)
Duration: ~25 minutes

---

[00:00] Jordan: Okay I think we're all here — Riley, you're on mute, just so you know.

[00:08] Riley: Oh sorry. Can you hear me now?

[00:11] Jordan: Yeah good. Alright, let's get into it. I want to keep this tight. We have three things to cover before EOD and I do not want to run over like we did last week. So, Q1 OKRs first. Alex, do you want to walk us through where Engineering landed?

[00:28] Alex: Sure. So we've got three OKRs on the Engineering side. First is shipping Atlas to internal beta by end of February — we've talked about that. Second is getting API latency under 200ms for 99th percentile, we're currently sitting around 380 so there's work to do. And third is reducing critical bug backlog by 40 percent. That one I'm actually pretty confident on because we've already closed out fourteen of the twenty-two items from last quarter.

[01:12] Jordan: Great. And the Atlas date — February 28, that's firm?

[01:17] Alex: That's the plan. There's a dependency on Sam's design handoff though. Sam, what's the status on the final component specs?

[01:26] Sam: So I have — okay, most of it is done. The navigation patterns and the core card components are finished and in Figma. The thing I'm waiting on is the data visualization module because we had a late requirement come in from Riley's team last week about the reporting dashboard. Riley, that's still in flux right?

[01:48] Riley: Yeah, sorry about that. The exec team wanted to see a summary view before we finalized it, and we're still waiting on their feedback. I know that's not ideal.

[02:01] Alex: That's the thing — if that stays open past January 24th we're going to have to scope it out of the February release and do it as a follow-up. I'm not trying to be difficult, I just need eight business days to implement once the spec is locked.

[02:18] Jordan: Okay. Riley, can you own getting that exec feedback by January 22nd? That gives Alex and Sam the buffer they need.

[02:29] Riley: Yeah, I can make that happen. I'll send a follow-up today.

[02:34] Jordan: Great. So let's call that a decision — Atlas internal beta February 28th, contingent on the reporting dashboard spec being locked by January 22nd. Alex, can you document what gets scoped out if we miss that date?

[02:50] Alex: Yeah I'll write that up this week and post it to the project channel.

[02:55] Jordan: Perfect. Okay, design review. Sam, where are we?

[03:01] Sam: So the main thing I want to flag is the onboarding flow. We had three rounds of user testing in December and there's a pretty consistent problem with step 4 — users are not understanding that they need to complete the profile before they can access the dashboard. We had a 34 percent drop-off at that step in testing.

[03:24] Alex: That's really high.

[03:26] Sam: It is. I have a proposed fix — it's a modal with a progress indicator and clearer copy. I mocked it up last week. But I want to get everyone's eyes on it before I finalize it. Can we do a design review this week? I need Engineering sign-off to make sure the implementation is feasible before I hand it off.

[03:47] Jordan: Alex, is Thursday afternoon doable?

[03:50] Alex: Thursday works. Let's say 2pm. I'll make sure Priya is on that call too since she's owning the onboarding implementation.

[03:58] Sam: Perfect. I'll send the Figma link before the call.

[04:02] Jordan: Okay great. Sam to send Figma link, Thursday 2pm design review, Alex and Priya on the call. Riley, do you want to be on that one?

[04:12] Riley: I can join for the first half. I have a conflict at 2:30 but I'll be there for the main discussion.

[04:19] Jordan: That works. Alright, marketing. Riley, you're up.

[04:23] Riley: Okay so the launch plan for Atlas. We're targeting a public launch in late March, assuming the beta goes well. I have a content calendar drafted — it's in the shared drive, I'll post the link in Slack after this call. The plan is three blog posts, a launch email to our user base, and a short product video. The video is the thing I'm most worried about because our usual vendor is booked through mid-March.

[04:56] Jordan: Can we use someone else for the video?

[05:00] Riley: I've been looking into it. There are a couple of options. Honestly the cheaper option might actually be faster turnaround. I'm going to get two more quotes this week and make a recommendation by Friday.

[05:14] Jordan: Okay, put that in writing — Riley to send video vendor recommendation by end of Friday.

[05:20] Riley: Will do.

[05:22] Alex: Can I just ask — the blog posts. Are those going to include technical content? Because if so I want someone from Engineering to review them. We got burned last time when marketing shipped a post that described the API in a way that was just not accurate.

[05:40] Riley: Yes, fair point. The second post is pretty technical — it's about how we built the data pipeline. I was going to ask you to write a section of it anyway.

[05:50] Alex: I can do that. Let's say I'll have a draft section to you by the 24th?

[05:55] Riley: That works perfectly, thank you.

[06:00] Jordan: Okay. Anything else on launch?

[06:04] Riley: One thing — we still haven't confirmed the launch date publicly. I don't want to start teasing this until we know we're not going to slip the February beta. Can we check in on February 21st and make the go/no-go call then?

[06:20] Jordan: That's a good call. Let's put that on the calendar — February 21st, go/no-go sync for public launch announcement. I'll send the invite.

[06:30] Alex: Works for me.

[06:32] Sam: Same.

[06:34] Jordan: Great. Okay last thing — I want to make sure we're all aligned on the Q1 stack rank. We have four initiatives on the board and I want to be clear about priority order. One: Atlas beta. Two: API latency. Three: onboarding flow fix. Four: the dashboard reporting module. Is anyone going to argue with that?

[06:58] Alex: I think that's right. Though I'd note that if the dashboard spec comes in late it becomes a Q2 item by default, so the stack rank kind of resolves itself.

[07:09] Sam: Agreed.

[07:11] Riley: Fine with me.

[07:13] Jordan: Good. That's the Q1 priority stack. Okay I think we've covered everything. Let me just recap the actions before we drop: Riley is getting exec feedback on the reporting dashboard by January 22nd. Alex is documenting the Atlas scope-out scenario this week. Sam is sending the Figma link before Thursday. Alex and Priya are on the Thursday 2pm design review. Riley is getting video vendor quotes and sending a recommendation by end of Friday. Alex is drafting the technical blog section by January 24th. And I'm sending the February 21st go/no-go invite today. Does that sound right?

[07:58] Riley: Yes.

[08:00] Alex: Yep.

[08:01] Sam: All good.

[08:03] Jordan: Alright, thanks everyone. Good meeting.
"""

with open(p('Q1 Planning Kickoff - 2025-01-14.txt'), 'w', encoding='utf-8') as f:
    f.write(TRANSCRIPT)
print('  ' + p('Q1 Planning Kickoff - 2025-01-14.txt'))

print('Done. Files written to:', ASSETS_DIR)
