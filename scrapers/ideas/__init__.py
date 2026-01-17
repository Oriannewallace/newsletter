"""
Newsletter Ideas Generator Module

Tools for generating newsletter topic ideas and tracking tool development.

Usage:
    from ideas import newsletter_ideas, tool_ideas, live_ideas

    # Get template ideas
    ideas = newsletter_ideas.get_ideas(pillars=["f1", "property"])

    # Get tool roadmap
    roadmap = tool_ideas.format_tool_roadmap()

    # Get live ideas (requires API keys)
    import asyncio
    live = asyncio.run(live_ideas.get_live_ideas("f1"))
"""

from . import newsletter_ideas
from . import tool_ideas

__all__ = ["newsletter_ideas", "tool_ideas"]
