#!/usr/bin/env python3
"""
Tool Ideas for The Winning Formula Newsletter

Tracks tool ideas with free vs premium tiers:
- FREE: Static tools, spreadsheets, basic calculators
- PREMIUM: Interactive versions, live data, advanced features

Each pillar has associated tool opportunities.
"""

from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class ToolIdea:
    """A tool idea with free and premium versions."""
    pillar: str
    name: str
    description: str
    free_version: str
    premium_version: str
    data_source: str
    complexity: str  # "simple", "medium", "complex"
    newsletter_tie_in: str  # How to introduce in newsletter


# Tool ideas organized by pillar
TOOL_IDEAS = {
    "f1": [
        ToolIdea(
            pillar="F1 & Performance",
            name="Race Pace Calculator",
            description="Compare driver pace across races",
            free_version="Google Sheet with manual lap time entry, calculates average pace and consistency",
            premium_version="Interactive web tool that pulls live FastF1 data, auto-generates comparisons, visual charts",
            data_source="FastF1 API",
            complexity="medium",
            newsletter_tie_in="Include screenshot in race analysis post, link to free sheet, tease premium version",
        ),
        ToolIdea(
            pillar="F1 & Performance",
            name="Pit Stop Strategy Simulator",
            description="Model different pit strategies and predicted outcomes",
            free_version="Spreadsheet with tire degradation curves and pit loss calculations",
            premium_version="Interactive simulator with real track data, weather integration, Monte Carlo simulations",
            data_source="FastF1 + historical data",
            complexity="complex",
            newsletter_tie_in="Show strategy breakdown in post, offer sheet for readers to try their own scenarios",
        ),
        ToolIdea(
            pillar="F1 & Performance",
            name="Driver Form Tracker",
            description="Track driver performance trends over the season",
            free_version="Simple points-per-race chart template",
            premium_version="Live dashboard with qualifying/race splits, teammate comparisons, form predictions",
            data_source="Official F1 results",
            complexity="simple",
            newsletter_tie_in="Weekly update in newsletter with trends, sheet for readers to track favorites",
        ),
        ToolIdea(
            pillar="F1 & Performance",
            name="Upgrade Impact Analyzer",
            description="Quantify team upgrade effectiveness",
            free_version="Before/after comparison template with lap time inputs",
            premium_version="Automated tracking from announcements, statistical significance testing, visual timelines",
            data_source="FastF1 + team announcements",
            complexity="medium",
            newsletter_tie_in="Use when teams bring upgrades, show analysis method, share template",
        ),
    ],
    "property": [
        ToolIdea(
            pillar="Property & Assets",
            name="Rental Yield Calculator",
            description="Calculate gross and net rental yields",
            free_version="Google Sheet with inputs for price, rent, expenses - outputs yield percentages",
            premium_version="Interactive calculator with suburb averages, expense estimator, comparison view",
            data_source="Property24 scraper",
            complexity="simple",
            newsletter_tie_in="Every property post includes yield examples, link to calculator",
        ),
        ToolIdea(
            pillar="Property & Assets",
            name="Suburb Comparison Tool",
            description="Compare suburbs on key investment metrics",
            free_version="Spreadsheet template to input suburb data and rank by criteria",
            premium_version="Live dashboard with Property24 data, filterable maps, trend charts",
            data_source="Property24 scraper",
            complexity="medium",
            newsletter_tie_in="Monthly suburb spotlight uses tool, readers can do their own analysis",
        ),
        ToolIdea(
            pillar="Property & Assets",
            name="Renovation ROI Calculator",
            description="Estimate return on renovation investment",
            free_version="Sheet with renovation cost inputs and value-add estimates",
            premium_version="Photo-based AI estimator, comparable sales integration, contractor cost database",
            data_source="Market research + user input",
            complexity="medium",
            newsletter_tie_in="Renovation case study posts, share framework for evaluating projects",
        ),
        ToolIdea(
            pillar="Property & Assets",
            name="Affordability Calculator",
            description="Calculate what you can afford based on income and rates",
            free_version="Interest rate scenario sheet with monthly payment calculations",
            premium_version="Bank comparison, rate alerts, pre-qualification estimates",
            data_source="Current interest rates",
            complexity="simple",
            newsletter_tie_in="When rates change, update calculator and analyze impact",
        ),
    ],
    "skincare": [
        ToolIdea(
            pillar="Skincare & Consumer Data",
            name="Ingredient Decoder",
            description="Understand what ingredients do and their evidence base",
            free_version="PDF guide to top 20 ingredients with efficacy ratings",
            premium_version="Searchable database with clinical study links, concentration guidelines, product finder",
            data_source="PubMed + product databases",
            complexity="medium",
            newsletter_tie_in="Each ingredient post references decoder, builds comprehensive resource",
        ),
        ToolIdea(
            pillar="Skincare & Consumer Data",
            name="Routine Builder",
            description="Build a skincare routine based on concerns",
            free_version="Decision tree flowchart PDF",
            premium_version="Interactive quiz with personalized recommendations, product alternatives, routine scheduler",
            data_source="Curated product database",
            complexity="complex",
            newsletter_tie_in="Posts about routine building reference the tool, gather user feedback",
        ),
        ToolIdea(
            pillar="Skincare & Consumer Data",
            name="Brand Valuation Tracker",
            description="Track beauty brand valuations and exits",
            free_version="Spreadsheet of known acquisitions with revenue multiples",
            premium_version="Live tracker with news alerts, valuation estimates, market trend analysis",
            data_source="News + financial reports",
            complexity="medium",
            newsletter_tie_in="When brands get acquired, analyze with the framework",
        ),
    ],
    "tech": [
        ToolIdea(
            pillar="Tech, Data & Modeling",
            name="Model Complexity Chooser",
            description="Decision framework for when to use simple vs complex models",
            free_version="Flowchart PDF with decision tree",
            premium_version="Interactive tool that analyzes your dataset characteristics and recommends approach",
            data_source="Best practices + research",
            complexity="simple",
            newsletter_tie_in="Reference in posts about model selection, build intuition over time",
        ),
        ToolIdea(
            pillar="Tech, Data & Modeling",
            name="A/B Test Calculator",
            description="Calculate sample sizes and statistical significance",
            free_version="Google Sheet with sample size and significance formulas",
            premium_version="Interactive calculator with power analysis, Bayesian option, visualizations",
            data_source="Statistical formulas",
            complexity="medium",
            newsletter_tie_in="When discussing experiments, share the methodology and tool",
        ),
        ToolIdea(
            pillar="Tech, Data & Modeling",
            name="Dataset Quality Checker",
            description="Checklist for evaluating dataset quality before modeling",
            free_version="PDF checklist with common issues to look for",
            premium_version="Automated analysis tool that scans CSV/data and flags issues",
            data_source="Data quality best practices",
            complexity="medium",
            newsletter_tie_in="Posts about data quality reference the checklist",
        ),
    ],
}


def get_all_tools() -> list[ToolIdea]:
    """Get all tool ideas across pillars."""
    all_tools = []
    for pillar_tools in TOOL_IDEAS.values():
        all_tools.extend(pillar_tools)
    return all_tools


def get_tools_by_pillar(pillar: str) -> list[ToolIdea]:
    """Get tool ideas for a specific pillar."""
    return TOOL_IDEAS.get(pillar, [])


def get_simple_tools() -> list[ToolIdea]:
    """Get tools that are simple to build (good starting points)."""
    return [t for t in get_all_tools() if t.complexity == "simple"]


def format_tool_roadmap() -> str:
    """Format a tool development roadmap."""
    output = ["# The Winning Formula - Tool Roadmap\n"]
    output.append("## Freemium Model")
    output.append("- **FREE**: Static tools, spreadsheets, PDFs shared in newsletter")
    output.append("- **PREMIUM**: Interactive web versions with live data\n")

    for pillar_key, tools in TOOL_IDEAS.items():
        pillar_name = tools[0].pillar if tools else pillar_key
        output.append(f"\n## {pillar_name}\n")

        for tool in tools:
            complexity_emoji = {"simple": "🟢", "medium": "🟡", "complex": "🔴"}[tool.complexity]
            output.append(f"### {complexity_emoji} {tool.name}")
            output.append(f"*{tool.description}*\n")
            output.append(f"**FREE:** {tool.free_version}\n")
            output.append(f"**PREMIUM:** {tool.premium_version}\n")
            output.append(f"**Newsletter Tie-in:** {tool.newsletter_tie_in}\n")

    return "\n".join(output)


def main():
    """Print the tool roadmap."""
    print(format_tool_roadmap())


if __name__ == "__main__":
    main()
