# n8n Trends Tracker - The Winning Formula

## Overview
Automated workflow that scrapes trending content across your 4 pillars and delivers a daily digest of content ideas.

**Output:** Daily report with 30-50 trending topics across F1, Property, Skincare, and Tech.

---

## Workflow Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        SOURCES                                   │
├─────────────┬─────────────┬─────────────┬─────────────┬─────────┤
│   YouTube   │   Reddit    │   Twitter/X │  LinkedIn   │   RSS   │
│  Trending   │  Hot Posts  │  Trending   │   Posts     │  Feeds  │
└──────┬──────┴──────┬──────┴──────┬──────┴──────┬──────┴────┬────┘
       │             │             │             │           │
       └─────────────┴──────┬──────┴─────────────┴───────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │   FILTER BY NICHE   │
                 │  F1 | Property |    │
                 │  Skincare | Tech    │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │   AI ANALYSIS       │
                 │  - Relevance score  │
                 │  - Content angle    │
                 │  - Newsletter fit   │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │  GOOGLE SHEETS      │
                 │  Organized by       │
                 │  pillar + priority  │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │  DAILY DIGEST       │
                 │  Slack / Email      │
                 └─────────────────────┘
```

---

## Sources by Pillar

### F1 & Performance
| Source | What to Monitor |
|--------|-----------------|
| Reddit | r/formula1, r/F1Technical, r/F1Statistics |
| YouTube | F1 official, Chain Bear, Driver61 |
| Twitter/X | @F1, @ChrisMedlandF1, team accounts |
| RSS | motorsport.com, racefans.net, the-race.com |

### Property & Investment
| Source | What to Monitor |
|--------|-----------------|
| Reddit | r/PropertyInvesting, r/southafrica, r/PersonalFinanceZA |
| YouTube | Property channels, market updates |
| Twitter/X | SA property accounts, economists |
| RSS | Property24 news, BusinessTech, Daily Investor |

### Skincare & Beauty
| Source | What to Monitor |
|--------|-----------------|
| Reddit | r/SkincareAddiction, r/AsianBeauty, r/30PlusSkinCare |
| YouTube | Beauty science channels, dermatologists |
| Twitter/X | Skincare influencers, brand accounts |
| RSS | Byrdie, Allure, cosmetics news |

### Tech & Data
| Source | What to Monitor |
|--------|-----------------|
| Reddit | r/datascience, r/MachineLearning, r/analytics |
| YouTube | Tech channels, data tutorials |
| Twitter/X | Data influencers, tech news |
| RSS | Towards Data Science, Analytics Vidhya |

---

## n8n Workflow Nodes

### 1. Schedule Trigger
```
Node: Schedule Trigger
Settings: Every day at 6:00 AM SAST
```

### 2. Reddit Scraper (per subreddit)
```
Node: HTTP Request
URL: https://www.reddit.com/r/{subreddit}/hot.json?limit=25
Method: GET
Headers: User-Agent: "TWF-Bot/1.0"

Subreddits to scrape:
- formula1
- F1Technical
- PropertyInvesting
- SkincareAddiction
- datascience
```

### 3. YouTube Trending (per channel/search)
```
Node: YouTube (or HTTP Request to YouTube API)
Search queries:
- "F1 2026" (last 24 hours)
- "property investment" (last 24 hours)
- "skincare routine" (last 24 hours)
- "data engineering" (last 24 hours)
```

### 4. Twitter/X Search
```
Node: Twitter API
Searches:
- "F1" min_faves:1000
- "property market" min_faves:500
- "skincare" min_faves:1000
- "data science" min_faves:500
```

### 5. RSS Feed Reader
```
Node: RSS Read
Feeds:
- https://www.motorsport.com/rss/f1/news/
- https://www.the-race.com/feed/
- https://businesstech.co.za/news/property/feed/
```

### 6. Merge All Sources
```
Node: Merge
Mode: Append
```

### 7. Filter & Categorize
```
Node: Code (JavaScript)

// Categorize by pillar based on keywords
const f1Keywords = ['f1', 'formula 1', 'verstappen', 'hamilton', 'mclaren', 'ferrari', 'red bull', 'lap time', 'qualifying'];
const propertyKeywords = ['property', 'real estate', 'rental', 'yield', 'investment', 'suburb', 'mortgage'];
const skincareKeywords = ['skincare', 'retinol', 'serum', 'moisturizer', 'spf', 'ingredient', 'routine'];
const techKeywords = ['data', 'python', 'machine learning', 'analytics', 'dashboard', 'sql', 'ai'];

// Assign pillar and filter relevance
```

### 8. AI Analysis (Claude/GPT)
```
Node: HTTP Request (Anthropic API)
Prompt:
"Analyze this content for newsletter potential:
Title: {{title}}
Source: {{source}}

Rate 1-10 on:
- Relevance to data-driven analysis
- Newsletter content potential
- Audience interest

Suggest a unique angle for The Winning Formula newsletter.
Return JSON: {score, angle, pillar}"
```

### 9. Filter High-Scoring Items
```
Node: IF
Condition: score >= 7
```

### 10. Google Sheets
```
Node: Google Sheets
Operation: Append
Spreadsheet: TWF Content Ideas
Columns:
- Date
- Pillar
- Title
- Source URL
- AI Score
- Suggested Angle
- Status (New/Used/Rejected)
```

### 11. Daily Digest
```
Node: Slack (or Email)
Message:
"🎯 Daily Content Ideas - {{date}}

**F1** ({{f1Count}} ideas)
{{f1TopIdeas}}

**Property** ({{propertyCount}} ideas)
{{propertyTopIdeas}}

**Skincare** ({{skincareCount}} ideas)
{{skincareTopIdeas}}

**Tech** ({{techCount}} ideas)
{{techTopIdeas}}

📊 Full list: [Google Sheet Link]"
```

---

## Google Sheet Structure

### Sheet: Content Ideas
| Date | Pillar | Title | Source | URL | AI Score | Angle | Status |
|------|--------|-------|--------|-----|----------|-------|--------|
| 2026-01-17 | F1 | Verstappen's new contract | Reddit | url | 8 | Analyze salary vs performance data | New |

### Sheet: Used Content
Track which ideas became newsletters

### Sheet: Analytics
- Ideas per pillar per week
- Conversion rate (idea → newsletter)
- Best performing sources

---

## Setup Checklist

- [ ] Create n8n account (self-hosted or cloud)
- [ ] Get API keys:
  - [ ] Reddit API (free)
  - [ ] YouTube Data API (free tier)
  - [ ] Twitter/X API (basic tier)
  - [ ] Anthropic/OpenAI API
  - [ ] Google Sheets API
  - [ ] Slack webhook (or email SMTP)
- [ ] Create Google Sheet with structure above
- [ ] Build workflow node by node
- [ ] Test each source individually
- [ ] Connect AI analysis
- [ ] Set up daily schedule
- [ ] Test full workflow

---

## Cost Estimate

| Service | Cost |
|---------|------|
| n8n Cloud | Free tier (limited) or $20/mo |
| Reddit API | Free |
| YouTube API | Free (10k requests/day) |
| Twitter/X | $100/mo (Basic) or scrape alternatives |
| Claude API | ~$5-10/mo (depending on volume) |
| Google Sheets | Free |
| **Total** | ~$25-130/mo |

### Budget Alternative
Skip Twitter API, use RSS feeds and Reddit only = ~$25/mo

---

## Quick Start (MVP Version)

Start simple, expand later:

**Phase 1: Reddit + RSS only**
1. Scrape 5 subreddits
2. Read 5 RSS feeds
3. Basic keyword filtering
4. Dump to Google Sheet
5. No AI (manual review)

**Phase 2: Add AI scoring**
1. Add Claude analysis
2. Auto-categorize by pillar
3. Daily Slack digest

**Phase 3: Full automation**
1. Add YouTube
2. Add Twitter/X
3. Add LinkedIn
4. Trend velocity detection

---

## Sample n8n JSON Export

Save this to import into n8n as a starting template:
(Create after building the workflow)

---

*Estimated setup time: 2-4 hours for MVP, 1 day for full version*
