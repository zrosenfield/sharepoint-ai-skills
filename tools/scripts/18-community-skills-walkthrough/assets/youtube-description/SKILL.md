---
name: youtube-description
description: Generate engaging YouTube video descriptions from video transcripts. Use this skill whenever the user wants to create a YouTube description, write a video description, summarize a video for YouTube, or draft copy for a YouTube upload. Also trigger when the user provides a transcript and mentions YouTube, video publishing, or video SEO. Works with raw transcripts, cleaned transcripts, or transcript files in any format.
---

# YouTube Video Description Generator

Turn a video transcript into an engaging, well-structured YouTube description that hooks viewers, summarizes value, and supports discoverability.

## When to Use

- User provides a video transcript and wants a YouTube description
- User asks for help writing copy for a YouTube upload
- User wants to optimize an existing video description
- User has a transcript file (.txt, .md, .docx, .pdf) and mentions YouTube

## Process

### 1. Analyze the Transcript

Read through the full transcript and identify:

- **Core topic**: What is this video fundamentally about?
- **Key moments**: 3-7 major segments, turning points, or valuable insights
- **Target audience**: Who would watch this? What level of expertise?
- **Tone**: Is the video casual/conversational, educational, professional, entertaining?
- **Unique value**: What makes this video worth watching over alternatives?
- **Any calls to action**: Links, products, services, or follow-ups mentioned

### 2. Draft the Description

Use this structure (adapt based on video type and tone):

```
[Hook — 1-2 sentences that create curiosity or state the value proposition. This is what shows above the "Show more" fold, so it needs to be compelling.]

[Summary — 2-4 sentences expanding on what the viewer will learn, see, or experience. Use natural language, not keyword stuffing.]

⏱ Timestamps
0:00 - [Intro/Opening topic]
X:XX - [Key moment 1]
X:XX - [Key moment 2]
...

[Optional sections as relevant:]

🔗 Links & Resources
- [Any tools, products, articles, or resources mentioned]

📌 Key Takeaways
- [2-4 bullet points summarizing the most valuable insights]

[Closing — brief context about the creator/channel, subscribe CTA]

#hashtag1 #hashtag2 #hashtag3
```

### 3. Guidelines for Quality

**Hook (above the fold)**:
- The first 2-3 lines are critical — they show in search results and above "Show more"
- Lead with a question, bold claim, or clear benefit statement
- Avoid generic openings like "In this video, I talk about..."
- Match the energy and tone of the actual video

**Timestamps**:
- If the transcript includes timing information, generate accurate timestamps
- If no timing info is available, note sections topically and tell the user to fill in timestamps
- Use descriptive labels, not vague ones like "Part 2" or "More info"

**Tone matching**:
- Mirror the creator's voice from the transcript — casual videos get casual descriptions, professional content stays polished
- Don't over-formalize a conversational video or casualize a serious one

**SEO awareness**:
- Naturally incorporate the primary topic keywords in the first 1-2 sentences
- Use 3-5 relevant hashtags at the end
- Don't keyword-stuff — YouTube's algorithm rewards natural language and engagement

**Length**:
- Aim for 150-300 words for the main description body (before timestamps/links)
- Total description can be longer with timestamps and resource links
- Respect YouTube's 5,000 character limit

### 4. Ask the User

If the transcript doesn't make certain things clear, ask about:
- Channel name (for the closing section)
- Any specific links or resources to include
- Whether they want timestamps included (and if they can provide timing)
- Any standard description template they already use

## Example

**Input context**: A 15-minute transcript of someone explaining 5 tips for better landscape photography

**Output**:

```
Most landscape photos fail for the same reason — and it has nothing to do with your camera. Here are 5 techniques that transformed my shots (especially #3).

In this video, I break down the composition tricks, timing strategies, and one simple gear hack that took my landscape photography from "nice snapshots" to images I'm actually proud of. Whether you're shooting on a phone or a full-frame DSLR, these principles apply.

⏱ Timestamps
0:00 - Why most landscape photos look flat
2:15 - Tip 1: The foreground anchor technique
4:30 - Tip 2: Shooting in the "bad" light
7:00 - Tip 3: The exposure bracketing shortcut
9:45 - Tip 4: Finding compositions others miss
12:10 - Tip 5: Post-processing for natural drama

📌 Key Takeaways
- Leading lines + foreground interest = instant depth
- Golden hour is overrated — learn to use overcast and blue hour
- Bracket your exposures even if you don't think you need HDR

🔗 Resources Mentioned
- Photopills app (for sun/moon positioning)
- My editing presets: [link]

If this helped, subscribe for weekly photography tips — I break down both the creative and technical sides of making better images.

#landscapephotography #photographytips #composition #photography #photoediting
```

## Notes

- If the user provides a partial or rough transcript (auto-generated captions, etc.), do your best — note any sections where the transcript was unclear
- For long videos (30+ min), consider suggesting the user break the description into clear sections
- If the video is part of a series, suggest mentioning the series and linking related episodes
