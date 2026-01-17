#!/usr/bin/env python3
"""
Newsletter Ideas Generator
Surfaces timely topics for "The Winning Formula" newsletter across 4 pillars:
- F1 & Performance
- Property & Assets
- Skincare & Consumer Data
- Tech, Data & Modeling

Uses web search to find current events and suggests analysis angles.
"""

import json
import os
from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import Optional
import httpx

# Pillar configurations with search queries and analysis frameworks
PILLARS = {
    "f1": {
        "name": "F1 & Performance",
        "color": "#FF8000",
        "search_queries": [
            "Formula 1 news this week",
            "F1 race results analysis",
            "F1 team upgrades technical",
            "F1 driver performance data",
        ],
        "analysis_frameworks": [
            "Lap time analysis: Compare qualifying vs race pace",
            "Strategy breakdown: Tire choices and pit stop timing",
            "Upgrade impact: Before/after performance metrics",
            "Driver consistency: Standard deviation of lap times",
            "Team trajectory: Points per race trend",
        ],
        "data_sources": [
            "FastF1 API (lap times, telemetry)",
            "Official F1 results",
            "Team technical announcements",
        ],
    },
    "property": {
        "name": "Property & Assets",
        "color": "#4CAF50",
        "search_queries": [
            "South Africa property market news",
            "Cape Town real estate trends",
            "Property investment analysis",
            "Rental yield trends South Africa",
        ],
        "analysis_frameworks": [
            "Suburb comparison: Yield vs growth potential",
            "Price-to-rent ratio analysis",
            "Supply/demand indicators by area",
            "Renovation ROI calculator",
            "Market timing: Interest rate impact",
        ],
        "data_sources": [
            "Property24 listings (your scraper)",
            "ABSA housing index",
            "StatsSA property data",
        ],
    },
    "skincare": {
        "name": "Skincare & Consumer Data",
        "color": "#E91E63",
        "search_queries": [
            "skincare brand news launches",
            "beauty industry acquisitions",
            "trending skincare ingredients",
            "skincare market analysis",
        ],
        "analysis_frameworks": [
            "Ingredient trend analysis: Search volume over time",
            "Brand sentiment: Social mentions vs sales",
            "Price positioning: Premium vs mass market",
            "Acquisition valuation: Revenue multiples",
            "Influencer impact: Claims vs clinical data",
        ],
        "data_sources": [
            "Google Trends (ingredient searches)",
            "Brand financial reports",
            "Clinical study databases",
        ],
    },
    "tech": {
        "name": "Tech, Data & Modeling",
        "color": "#2196F3",
        "search_queries": [
            "machine learning news applications",
            "data science trends",
            "AI model releases",
            "analytics tools launches",
        ],
        "analysis_frameworks": [
            "Model comparison: Simple vs complex accuracy",
            "Tool evaluation: When to use what",
            "Case study: Real-world ML applications",
            "Assumption testing: How models fail",
            "Explainability: Making ML accessible",
        ],
        "data_sources": [
            "ArXiv papers",
            "Hugging Face model hub",
            "GitHub trending repos",
        ],
    },
}


@dataclass
class NewsletterIdea:
    """A single newsletter topic idea with analysis suggestions."""
    pillar: str
    headline: str
    summary: str
    analysis_angle: str
    data_needed: list[str]
    urgency: str  # "timely", "evergreen", "trending"
    source_url: Optional[str] = None


def generate_ideas_for_pillar(pillar_key: str, ideas: list[dict]) -> list[NewsletterIdea]:
    """Convert raw search results into structured newsletter ideas."""
    pillar = PILLARS.get(pillar_key)
    if not pillar:
        return []

    newsletter_ideas = []
    frameworks = pillar["analysis_frameworks"]

    for i, idea in enumerate(ideas[:5]):  # Top 5 ideas per pillar
        # Rotate through analysis frameworks
        framework = frameworks[i % len(frameworks)]

        newsletter_ideas.append(NewsletterIdea(
            pillar=pillar["name"],
            headline=idea.get("title", "Untitled"),
            summary=idea.get("summary", ""),
            analysis_angle=framework,
            data_needed=pillar["data_sources"],
            urgency="timely" if i < 2 else "trending",
            source_url=idea.get("url"),
        ))

    return newsletter_ideas


def format_ideas_markdown(ideas: list[NewsletterIdea]) -> str:
    """Format ideas as markdown for easy reading."""
    output = []
    output.append(f"# Newsletter Ideas - {datetime.now().strftime('%B %d, %Y')}\n")

    current_pillar = None
    for idea in ideas:
        if idea.pillar != current_pillar:
            current_pillar = idea.pillar
            output.append(f"\n## {current_pillar}\n")

        urgency_emoji = {"timely": "🔥", "trending": "📈", "evergreen": "🌲"}.get(idea.urgency, "")

        output.append(f"### {urgency_emoji} {idea.headline}\n")
        if idea.summary:
            output.append(f"{idea.summary}\n")
        output.append(f"\n**Analysis Angle:** {idea.analysis_angle}\n")
        output.append(f"**Data Sources:** {', '.join(idea.data_needed)}\n")
        if idea.source_url:
            output.append(f"**Source:** {idea.source_url}\n")
        output.append("")

    return "\n".join(output)


def format_ideas_json(ideas: list[NewsletterIdea]) -> str:
    """Format ideas as JSON for programmatic use."""
    return json.dumps([
        {
            "pillar": idea.pillar,
            "headline": idea.headline,
            "summary": idea.summary,
            "analysis_angle": idea.analysis_angle,
            "data_needed": idea.data_needed,
            "urgency": idea.urgency,
            "source_url": idea.source_url,
        }
        for idea in ideas
    ], indent=2)


# Manual ideas based on current events (can be updated or fetched via API)
SAMPLE_IDEAS = {
    "f1": [
        {
            "title": "2025 Pre-Season Testing Analysis",
            "summary": "Teams reveal their 2025 cars - early lap times suggest shifts in competitive order",
            "url": "https://www.formula1.com"
        },
        {
            "title": "Regulation Changes Impact",
            "summary": "New 2025 regulations affecting car design - which teams adapted best?",
            "url": None
        },
        {
            "title": "Driver Market Moves",
            "summary": "Hamilton to Ferrari - analyzing historical team switch performance data",
            "url": None
        },
    ],
    "property": [
        {
            "title": "Interest Rate Decision Impact",
            "summary": "Latest SARB decision and what it means for property buyers",
            "url": None
        },
        {
            "title": "Cape Town Suburb Spotlight",
            "summary": "Emerging suburbs with strong yield potential - data-driven analysis",
            "url": None
        },
    ],
    "skincare": [
        {
            "title": "Rhode Skin Valuation Analysis",
            "summary": "Hailey Bieber's brand reportedly valued at $XXXm - breaking down the numbers",
            "url": None
        },
        {
            "title": "Peptide Trend Deep Dive",
            "summary": "Why peptides are trending - separating science from marketing hype",
            "url": None
        },
    ],
    "tech": [
        {
            "title": "When Linear Regression Beats Neural Networks",
            "summary": "Case studies showing simple models outperforming complex ones",
            "url": None
        },
        {
            "title": "MLflow for Newsletter Analytics",
            "summary": "Track your own newsletter performance with data science tools",
            "url": None
        },
    ],
}


def get_ideas(pillars: list[str] = None, output_format: str = "markdown") -> str:
    """
    Get newsletter ideas for specified pillars.

    Args:
        pillars: List of pillar keys to get ideas for. None = all pillars.
        output_format: "markdown" or "json"

    Returns:
        Formatted string of newsletter ideas
    """
    if pillars is None:
        pillars = list(PILLARS.keys())

    all_ideas = []
    for pillar_key in pillars:
        if pillar_key in SAMPLE_IDEAS:
            ideas = generate_ideas_for_pillar(pillar_key, SAMPLE_IDEAS[pillar_key])
            all_ideas.extend(ideas)

    if output_format == "json":
        return format_ideas_json(all_ideas)
    return format_ideas_markdown(all_ideas)


def main():
    """CLI entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Generate newsletter topic ideas")
    parser.add_argument(
        "--pillar", "-p",
        choices=list(PILLARS.keys()) + ["all"],
        default="all",
        help="Which pillar to get ideas for"
    )
    parser.add_argument(
        "--format", "-f",
        choices=["markdown", "json"],
        default="markdown",
        help="Output format"
    )
    parser.add_argument(
        "--list-pillars",
        action="store_true",
        help="List available pillars"
    )

    args = parser.parse_args()

    if args.list_pillars:
        print("\nAvailable Pillars:")
        for key, pillar in PILLARS.items():
            print(f"  {key}: {pillar['name']}")
        return

    pillars = None if args.pillar == "all" else [args.pillar]
    output = get_ideas(pillars=pillars, output_format=args.format)
    print(output)


if __name__ == "__main__":
    main()
