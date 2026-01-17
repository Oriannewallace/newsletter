# Content Repurposing Automation Strategy

## The Goal
Automatically turn each newsletter issue into multiple social media posts that drive signups.

## The Workflow

```
Newsletter Published
       ↓
AI Extracts Key Insights/Hooks
       ↓
Generates Platform-Specific Content:
  - Twitter/X thread (5-7 tweets)
  - LinkedIn post (thought leadership)
  - Instagram carousel (visual data)
  - Reddit post (discussion starter)
  - Short-form video script (TikTok/Reels)
       ↓
Schedule & Publish
       ↓
CTA: "Full analysis in my newsletter → [link]"
```

## Content Types to Generate

### 1. Twitter/X Thread
- Hook tweet (the surprising insight)
- 4-5 supporting points with data
- Final tweet with CTA to subscribe
- Example: "Verstappen finished P5 but had the fastest race pace. Here's what the data shows 🧵"

### 2. LinkedIn Post
- Professional angle
- Data-driven insight
- Tag relevant topics (#DataAnalysis #F1)
- End with newsletter CTA

### 3. Instagram Carousel
- Slide 1: Bold statement/hook
- Slides 2-5: Key data points as graphics
- Final slide: "Get the full analysis" + link in bio

### 4. Reddit Posts
- r/formula1 - F1 analysis posts
- r/PropertyInvesting - Property insights
- r/SkincareAddiction - Skincare data
- r/dataisbeautiful - Data visualizations
- Value-first, soft CTA in comments

### 5. Short-form Video Script
- 30-60 second script
- "Did you know..." hook
- Quick data reveal
- "Full breakdown in newsletter"

## Tools Needed

### Option A: No-Code (Zapier/Make)
- Trigger: New Beehiiv post published
- Action: Send content to Claude API
- Action: Generate social posts
- Action: Send to Buffer/Hootsuite for scheduling

### Option B: Custom Script (Python)
- Use Beehiiv API to fetch new posts
- Use Claude API to repurpose content
- Use Twitter/LinkedIn APIs to post
- Cron job or webhook trigger

### Option C: Manual + AI
- Copy newsletter to Claude
- Use prompts to generate posts
- Manually schedule in native apps

## Prompts to Use

### Twitter Thread Prompt
```
Take this newsletter content and create a Twitter thread:
- First tweet: surprising hook with emoji
- 4-5 tweets expanding on key points
- Include specific numbers/data
- Final tweet: CTA to subscribe
- Keep each tweet under 280 characters

Newsletter content:
[PASTE CONTENT]
```

### LinkedIn Post Prompt
```
Turn this newsletter into a LinkedIn post:
- Professional tone
- Lead with the insight, not the promotion
- Include 2-3 data points
- End with soft CTA
- Add relevant hashtags
- 150-200 words max

Newsletter content:
[PASTE CONTENT]
```

### Instagram Carousel Prompt
```
Create an Instagram carousel (7 slides) from this newsletter:
- Slide 1: Bold hook statement
- Slides 2-6: One key insight per slide with data
- Slide 7: CTA to subscribe
- Keep text minimal (under 20 words per slide)
- Suggest visual style for each slide

Newsletter content:
[PASTE CONTENT]
```

## Tracking Success

- Track clicks from each platform (UTM parameters)
- Monitor which content types drive most signups
- A/B test hooks and CTAs
- Double down on what works

## Schedule Cadence

After each newsletter:
- Day 0: Twitter thread (immediate)
- Day 1: LinkedIn post
- Day 2: Instagram carousel
- Day 3: Reddit post (if appropriate)
- Day 5: Repurpose as short video

## UTM Links

```
Newsletter signup link with tracking:
https://thewinningformula.beehiiv.com/subscribe?utm_source=twitter&utm_medium=thread&utm_campaign=issue_01
https://thewinningformula.beehiiv.com/subscribe?utm_source=linkedin&utm_medium=post&utm_campaign=issue_01
https://thewinningformula.beehiiv.com/subscribe?utm_source=instagram&utm_medium=carousel&utm_campaign=issue_01
```

---

## Quick Start (Manual Version)

1. Publish newsletter
2. Copy content to Claude
3. Use prompts above to generate posts
4. Schedule posts throughout the week
5. Track signups with UTM links
6. Iterate based on what works
