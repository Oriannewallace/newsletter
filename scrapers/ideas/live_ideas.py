#!/usr/bin/env python3
"""
Live Newsletter Ideas Generator
Fetches real-time news and events to suggest newsletter topics.

Supports multiple backends:
- Perplexity API (recommended for research-quality results)
- Tavily API (good for news)
- Web scraping fallback

Usage:
    python live_ideas.py --pillar f1
    python live_ideas.py --all
    python live_ideas.py --pillar skincare --query "Rhode skin brand"
"""

import os
import json
import httpx
from datetime import datetime
from typing import Optional
from dataclasses import dataclass, asdict

# Load API keys from environment
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")


@dataclass
class ResearchIdea:
    """A researched newsletter topic with analysis suggestions."""
    pillar: str
    title: str
    summary: str
    key_data_points: list[str]
    analysis_angle: str
    why_now: str
    sources: list[str]
    timestamp: str


PILLAR_PROMPTS = {
    "f1": {
        "name": "F1 & Performance",
        "research_prompt": """Find the most important Formula 1 news from the past week that would make good data analysis content. Focus on:
- Race results and surprising performances
- Team upgrades and technical developments
- Driver comparisons and form changes
- Strategy decisions that affected results

For each topic, explain what data could be analyzed (lap times, pit stops, points trends).""",
        "analysis_frameworks": [
            "Lap time distribution analysis",
            "Pit stop strategy comparison",
            "Points trajectory modeling",
            "Upgrade impact quantification",
        ],
    },
    "property": {
        "name": "Property & Assets",
        "research_prompt": """Find the most relevant South African property market news from the past week. Focus on:
- Interest rate changes and their impact
- Suburb or area performance data
- Rental market trends
- Investment opportunity indicators

For each topic, explain what property data could be analyzed (prices, yields, inventory).""",
        "analysis_frameworks": [
            "Suburb yield comparison",
            "Price-to-rent ratio analysis",
            "Market timing indicators",
            "ROI scenario modeling",
        ],
    },
    "skincare": {
        "name": "Skincare & Consumer Data",
        "research_prompt": """Find the most interesting skincare and beauty industry news from the past week. Focus on:
- Brand launches, acquisitions, or valuations
- Trending ingredients backed by data
- Consumer behavior shifts
- Scientific studies on skincare efficacy

For each topic, explain what consumer/market data could be analyzed.""",
        "analysis_frameworks": [
            "Ingredient trend analysis",
            "Brand valuation breakdown",
            "Consumer sentiment analysis",
            "Clinical efficacy review",
        ],
    },
    "tech": {
        "name": "Tech, Data & Modeling",
        "research_prompt": """Find interesting data science and machine learning news from the past week that could be explained to a general audience. Focus on:
- New model releases or techniques
- Real-world ML applications and case studies
- Tools that make data analysis easier
- Interesting datasets or analyses

For each topic, explain how it demonstrates data-driven thinking.""",
        "analysis_frameworks": [
            "Model comparison study",
            "Tool/technique evaluation",
            "Case study breakdown",
            "Assumption testing demo",
        ],
    },
}


async def search_perplexity(query: str, pillar_context: str) -> dict:
    """
    Search using Perplexity API for research-quality results.

    Requires PERPLEXITY_API_KEY environment variable.
    """
    if not PERPLEXITY_API_KEY:
        return {"error": "PERPLEXITY_API_KEY not set"}

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.perplexity.ai/chat/completions",
            headers={
                "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": "llama-3.1-sonar-small-128k-online",
                "messages": [
                    {
                        "role": "system",
                        "content": f"You are a research assistant for a data-driven newsletter. {pillar_context}"
                    },
                    {
                        "role": "user",
                        "content": query
                    }
                ],
                "temperature": 0.2,
                "return_citations": True,
            },
            timeout=30.0,
        )
        return response.json()


async def search_tavily(query: str) -> dict:
    """
    Search using Tavily API for news results.

    Requires TAVILY_API_KEY environment variable.
    """
    if not TAVILY_API_KEY:
        return {"error": "TAVILY_API_KEY not set"}

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.tavily.com/search",
            json={
                "api_key": TAVILY_API_KEY,
                "query": query,
                "search_depth": "advanced",
                "include_answer": True,
                "include_raw_content": False,
                "max_results": 5,
            },
            timeout=30.0,
        )
        return response.json()


def parse_perplexity_response(response: dict, pillar: str) -> list[ResearchIdea]:
    """Parse Perplexity API response into structured ideas."""
    ideas = []

    if "error" in response:
        return ideas

    try:
        content = response["choices"][0]["message"]["content"]
        citations = response.get("citations", [])

        # Create a single comprehensive idea from the response
        pillar_config = PILLAR_PROMPTS.get(pillar, {})

        ideas.append(ResearchIdea(
            pillar=pillar_config.get("name", pillar),
            title=f"Weekly {pillar_config.get('name', pillar)} Research",
            summary=content[:500] + "..." if len(content) > 500 else content,
            key_data_points=[
                "See full response for detailed data points"
            ],
            analysis_angle=pillar_config.get("analysis_frameworks", ["General analysis"])[0],
            why_now="Current week's developments",
            sources=citations[:5] if citations else ["Perplexity research"],
            timestamp=datetime.now().isoformat(),
        ))
    except (KeyError, IndexError) as e:
        print(f"Error parsing response: {e}")

    return ideas


def get_manual_ideas(pillar: str) -> list[ResearchIdea]:
    """
    Get manually curated ideas when APIs are not available.
    These serve as templates and examples.
    """
    pillar_config = PILLAR_PROMPTS.get(pillar, {})

    manual_ideas = {
        "f1": [
            ResearchIdea(
                pillar="F1 & Performance",
                title="Race Weekend Analysis Template",
                summary="After each race, analyze: qualifying vs race performance gaps, tire strategy effectiveness, and points implications for the championship.",
                key_data_points=[
                    "Lap time data from FastF1",
                    "Pit stop timing and tire compounds",
                    "Position changes lap by lap",
                    "Championship points before/after",
                ],
                analysis_angle="Performance delta analysis",
                why_now="Run after each race weekend",
                sources=["FastF1 API", "Official F1 results"],
                timestamp=datetime.now().isoformat(),
            ),
            ResearchIdea(
                pillar="F1 & Performance",
                title="Team Upgrade Impact Study",
                summary="When teams announce upgrades, track performance changes in subsequent races to quantify impact.",
                key_data_points=[
                    "Lap times before upgrade (3-race average)",
                    "Lap times after upgrade (3-race average)",
                    "Qualifying position changes",
                    "Race pace relative to leader",
                ],
                analysis_angle="Before/after comparative analysis",
                why_now="Track after team announcements",
                sources=["FastF1 API", "Team technical briefings"],
                timestamp=datetime.now().isoformat(),
            ),
        ],
        "property": [
            ResearchIdea(
                pillar="Property & Assets",
                title="Monthly Suburb Comparison",
                summary="Compare rental yields and price growth across Cape Town suburbs using Property24 data.",
                key_data_points=[
                    "Median asking prices by suburb",
                    "Median rental prices by suburb",
                    "Calculated gross yields",
                    "Inventory levels (supply indicator)",
                ],
                analysis_angle="Yield vs growth quadrant analysis",
                why_now="Monthly market snapshot",
                sources=["Property24 scraper", "Your ROI model"],
                timestamp=datetime.now().isoformat(),
            ),
        ],
        "skincare": [
            ResearchIdea(
                pillar="Skincare & Consumer Data",
                title="Ingredient Trend Tracker",
                summary="Monitor Google Trends for skincare ingredients, correlate with product launches and influencer mentions.",
                key_data_points=[
                    "Search volume trends (12-month)",
                    "Product launch dates",
                    "Social mention counts",
                    "Clinical study publication dates",
                ],
                analysis_angle="Hype cycle position analysis",
                why_now="Monthly or when ingredient goes viral",
                sources=["Google Trends", "PubMed", "Social listening"],
                timestamp=datetime.now().isoformat(),
            ),
        ],
        "tech": [
            ResearchIdea(
                pillar="Tech, Data & Modeling",
                title="Simple vs Complex Model Showdown",
                summary="Take a real problem, solve it with linear regression AND a neural network, compare results and explain when simple wins.",
                key_data_points=[
                    "Dataset characteristics",
                    "Model accuracy metrics",
                    "Training time comparison",
                    "Interpretability scores",
                ],
                analysis_angle="Complexity vs performance tradeoff",
                why_now="Evergreen educational content",
                sources=["Your own experiments", "ML papers"],
                timestamp=datetime.now().isoformat(),
            ),
        ],
    }

    return manual_ideas.get(pillar, [])


async def get_live_ideas(pillar: str, custom_query: Optional[str] = None) -> list[ResearchIdea]:
    """
    Get live ideas using available APIs, falling back to manual ideas.
    """
    pillar_config = PILLAR_PROMPTS.get(pillar)
    if not pillar_config:
        return []

    query = custom_query or pillar_config["research_prompt"]

    # Try Perplexity first
    if PERPLEXITY_API_KEY:
        print(f"🔍 Searching Perplexity for {pillar_config['name']} ideas...")
        response = await search_perplexity(query, pillar_config["research_prompt"])
        if "error" not in response:
            return parse_perplexity_response(response, pillar)

    # Try Tavily next
    if TAVILY_API_KEY:
        print(f"🔍 Searching Tavily for {pillar_config['name']} news...")
        response = await search_tavily(f"{pillar_config['name']} news this week")
        # Parse Tavily response...

    # Fall back to manual ideas
    print(f"📋 Using template ideas for {pillar_config['name']} (set API keys for live results)")
    return get_manual_ideas(pillar)


def format_ideas(ideas: list[ResearchIdea], format: str = "markdown") -> str:
    """Format ideas for output."""
    if format == "json":
        return json.dumps([asdict(idea) for idea in ideas], indent=2)

    # Markdown format
    output = [f"# Newsletter Ideas - {datetime.now().strftime('%B %d, %Y')}\n"]

    current_pillar = None
    for idea in ideas:
        if idea.pillar != current_pillar:
            current_pillar = idea.pillar
            output.append(f"\n## 📊 {current_pillar}\n")

        output.append(f"### {idea.title}\n")
        output.append(f"{idea.summary}\n")
        output.append(f"\n**Why Now:** {idea.why_now}\n")
        output.append(f"**Analysis Angle:** {idea.analysis_angle}\n")
        output.append(f"\n**Key Data Points:**")
        for point in idea.key_data_points:
            output.append(f"- {point}")
        output.append(f"\n**Sources:** {', '.join(idea.sources)}\n")
        output.append("---\n")

    return "\n".join(output)


async def main():
    """CLI entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Generate live newsletter topic ideas")
    parser.add_argument(
        "--pillar", "-p",
        choices=list(PILLAR_PROMPTS.keys()) + ["all"],
        default="all",
        help="Which pillar to research"
    )
    parser.add_argument(
        "--query", "-q",
        type=str,
        help="Custom search query"
    )
    parser.add_argument(
        "--format", "-f",
        choices=["markdown", "json"],
        default="markdown",
        help="Output format"
    )
    parser.add_argument(
        "--output", "-o",
        type=str,
        help="Output file path"
    )

    args = parser.parse_args()

    pillars = list(PILLAR_PROMPTS.keys()) if args.pillar == "all" else [args.pillar]

    all_ideas = []
    for pillar in pillars:
        ideas = await get_live_ideas(pillar, args.query)
        all_ideas.extend(ideas)

    output = format_ideas(all_ideas, args.format)

    if args.output:
        with open(args.output, "w") as f:
            f.write(output)
        print(f"✅ Ideas saved to {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
