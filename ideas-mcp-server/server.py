#!/usr/bin/env python3
"""
Newsletter Ideas MCP Server
Provides on-demand research tools for The Winning Formula newsletter.

Tools:
- get_reddit_trending: Fetch trending posts from pillar subreddits
- get_rss_news: Fetch latest news from RSS feeds
- get_ideas: Combined research across all sources
"""

import asyncio
import json
from datetime import datetime
from typing import Optional
import httpx
import feedparser
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# Initialize MCP server
server = Server("newsletter-ideas")

# Pillar configurations
PILLARS = {
    "f1": {
        "name": "F1 & Performance",
        "subreddits": ["formula1", "F1Technical", "F1Statistics"],
        "rss_feeds": [
            ("Motorsport.com", "https://www.motorsport.com/rss/f1/news/"),
            ("The Race", "https://www.the-race.com/feed/"),
            ("RaceFans", "https://www.racefans.net/feed/"),
        ],
        "keywords": ["f1", "formula 1", "verstappen", "hamilton", "norris", "mclaren", "ferrari", "red bull", "mercedes"],
    },
    "property": {
        "name": "Property & Assets",
        "subreddits": ["PropertyInvesting", "southafrica", "PersonalFinanceZA", "capetown"],
        "rss_feeds": [
            ("BusinessTech Property", "https://businesstech.co.za/news/property/feed/"),
        ],
        "keywords": ["property", "real estate", "rental", "yield", "investment", "suburb", "cape town"],
    },
    "skincare": {
        "name": "Skincare & Beauty",
        "subreddits": ["SkincareAddiction", "AsianBeauty", "30PlusSkinCare", "SkincareAddicts"],
        "rss_feeds": [],
        "keywords": ["skincare", "retinol", "serum", "moisturizer", "spf", "ingredient", "routine", "brand"],
    },
    "tech": {
        "name": "Tech & Data",
        "subreddits": ["datascience", "MachineLearning", "analytics", "Python", "dataengineering"],
        "rss_feeds": [],
        "keywords": ["data", "python", "machine learning", "analytics", "dashboard", "sql", "ai", "model"],
    },
}


async def fetch_reddit(subreddit: str, limit: int = 10) -> list[dict]:
    """Fetch hot posts from a subreddit."""
    url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit={limit}"
    headers = {"User-Agent": "TWF-Newsletter-Bot/1.0"}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=10.0)
            response.raise_for_status()
            data = response.json()

            posts = []
            for child in data.get("data", {}).get("children", []):
                post = child.get("data", {})
                posts.append({
                    "title": post.get("title", ""),
                    "score": post.get("score", 0),
                    "comments": post.get("num_comments", 0),
                    "url": f"https://reddit.com{post.get('permalink', '')}",
                    "subreddit": subreddit,
                    "created": datetime.fromtimestamp(post.get("created_utc", 0)).strftime("%Y-%m-%d %H:%M"),
                })
            return posts
        except Exception as e:
            return [{"error": f"Failed to fetch r/{subreddit}: {str(e)}"}]


async def fetch_rss(feed_name: str, feed_url: str, limit: int = 5) -> list[dict]:
    """Fetch latest items from an RSS feed."""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(feed_url, timeout=10.0)
            response.raise_for_status()
            feed = feedparser.parse(response.text)

            items = []
            for entry in feed.entries[:limit]:
                items.append({
                    "title": entry.get("title", ""),
                    "link": entry.get("link", ""),
                    "source": feed_name,
                    "published": entry.get("published", ""),
                })
            return items
        except Exception as e:
            return [{"error": f"Failed to fetch {feed_name}: {str(e)}"}]


def format_reddit_results(posts: list[dict], pillar_name: str) -> str:
    """Format Reddit posts as markdown."""
    output = [f"## Reddit: {pillar_name}\n"]

    for post in posts:
        if "error" in post:
            output.append(f"- Error: {post['error']}\n")
            continue
        output.append(f"### {post['title']}")
        output.append(f"- **Score:** {post['score']} | **Comments:** {post['comments']}")
        output.append(f"- **Subreddit:** r/{post['subreddit']}")
        output.append(f"- **Link:** {post['url']}")
        output.append("")

    return "\n".join(output)


def format_rss_results(items: list[dict], pillar_name: str) -> str:
    """Format RSS items as markdown."""
    output = [f"## RSS News: {pillar_name}\n"]

    for item in items:
        if "error" in item:
            output.append(f"- Error: {item['error']}\n")
            continue
        output.append(f"### {item['title']}")
        output.append(f"- **Source:** {item['source']}")
        output.append(f"- **Link:** {item['link']}")
        output.append("")

    return "\n".join(output)


@server.list_tools()
async def list_tools():
    """List available tools."""
    return [
        Tool(
            name="get_reddit_trending",
            description="Get trending posts from Reddit for a specific pillar (f1, property, skincare, tech) or all pillars",
            inputSchema={
                "type": "object",
                "properties": {
                    "pillar": {
                        "type": "string",
                        "description": "Pillar to search: f1, property, skincare, tech, or 'all'",
                        "enum": ["f1", "property", "skincare", "tech", "all"],
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Number of posts per subreddit (default 5)",
                        "default": 5,
                    },
                },
                "required": ["pillar"],
            },
        ),
        Tool(
            name="get_rss_news",
            description="Get latest news from RSS feeds for a specific pillar (f1, property) or all",
            inputSchema={
                "type": "object",
                "properties": {
                    "pillar": {
                        "type": "string",
                        "description": "Pillar to search: f1, property, or 'all'",
                        "enum": ["f1", "property", "all"],
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Number of items per feed (default 5)",
                        "default": 5,
                    },
                },
                "required": ["pillar"],
            },
        ),
        Tool(
            name="get_newsletter_ideas",
            description="Get combined newsletter ideas from Reddit and RSS for all pillars or a specific one",
            inputSchema={
                "type": "object",
                "properties": {
                    "pillar": {
                        "type": "string",
                        "description": "Pillar to research: f1, property, skincare, tech, or 'all'",
                        "enum": ["f1", "property", "skincare", "tech", "all"],
                    },
                },
                "required": ["pillar"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict):
    """Handle tool calls."""

    if name == "get_reddit_trending":
        pillar = arguments.get("pillar", "all")
        limit = arguments.get("limit", 5)

        pillars_to_search = list(PILLARS.keys()) if pillar == "all" else [pillar]

        results = []
        for p in pillars_to_search:
            if p not in PILLARS:
                continue
            config = PILLARS[p]
            all_posts = []

            for subreddit in config["subreddits"]:
                posts = await fetch_reddit(subreddit, limit)
                all_posts.extend(posts)

            # Sort by score
            all_posts.sort(key=lambda x: x.get("score", 0), reverse=True)
            results.append(format_reddit_results(all_posts[:limit * 2], config["name"]))

        return [TextContent(type="text", text="\n\n".join(results))]

    elif name == "get_rss_news":
        pillar = arguments.get("pillar", "all")
        limit = arguments.get("limit", 5)

        pillars_to_search = list(PILLARS.keys()) if pillar == "all" else [pillar]

        results = []
        for p in pillars_to_search:
            if p not in PILLARS:
                continue
            config = PILLARS[p]

            if not config["rss_feeds"]:
                continue

            all_items = []
            for feed_name, feed_url in config["rss_feeds"]:
                items = await fetch_rss(feed_name, feed_url, limit)
                all_items.extend(items)

            results.append(format_rss_results(all_items, config["name"]))

        if not results:
            return [TextContent(type="text", text="No RSS feeds configured for the selected pillar(s).")]

        return [TextContent(type="text", text="\n\n".join(results))]

    elif name == "get_newsletter_ideas":
        pillar = arguments.get("pillar", "all")
        pillars_to_search = list(PILLARS.keys()) if pillar == "all" else [pillar]

        output = [f"# Newsletter Ideas - {datetime.now().strftime('%B %d, %Y')}\n"]

        for p in pillars_to_search:
            if p not in PILLARS:
                continue
            config = PILLARS[p]
            output.append(f"\n## {config['name']}\n")

            # Fetch Reddit
            all_posts = []
            for subreddit in config["subreddits"][:2]:  # Limit subreddits for speed
                posts = await fetch_reddit(subreddit, 5)
                all_posts.extend(posts)

            all_posts.sort(key=lambda x: x.get("score", 0), reverse=True)

            output.append("### Trending on Reddit\n")
            for post in all_posts[:5]:
                if "error" not in post:
                    output.append(f"- **{post['title']}** ({post['score']} upvotes)")
                    output.append(f"  - r/{post['subreddit']} | {post['url']}")

            # Fetch RSS if available
            if config["rss_feeds"]:
                output.append("\n### Latest News\n")
                for feed_name, feed_url in config["rss_feeds"][:2]:
                    items = await fetch_rss(feed_name, feed_url, 3)
                    for item in items:
                        if "error" not in item:
                            output.append(f"- **{item['title']}**")
                            output.append(f"  - {item['source']} | {item['link']}")

            output.append("")

        return [TextContent(type="text", text="\n".join(output))]

    return [TextContent(type="text", text=f"Unknown tool: {name}")]


async def main():
    """Run the MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
