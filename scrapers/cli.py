#!/usr/bin/env python3
"""
CLI for The Winning Formula property tools.

Usage:
    python cli.py scrape kenilworth --city cape-town --province western-cape
    python cli.py analyze kenilworth
    python cli.py compare kenilworth claremont rondebosch
"""

import argparse
import asyncio
from pathlib import Path

from property24_scraper import Property24Scraper, save_listings
from suburb_analyzer import SuburbAnalyzer


async def cmd_scrape(args):
    """Scrape property listings for a suburb."""
    async with Property24Scraper(headless=not args.show_browser) as scraper:
        print(f"\nScraping {args.suburb}...")
        print(f"  City: {args.city}")
        print(f"  Province: {args.province}")
        print(f"  Max listings: {args.max_listings}")
        print(f"  Mode: {'detailed (slower but accurate)' if args.detailed else 'fast (URLs only)'}")
        print()

        if args.detailed:
            # Use detailed scraping - visits each listing page
            print("Fetching rentals (detailed mode)...")
            rentals = await scraper.scrape_suburb_detailed(
                suburb=args.suburb,
                city=args.city,
                province=args.province,
                listing_type="rent",
                max_listings=args.max_listings
            )
            if rentals:
                save_listings(rentals, f"{args.suburb}_rentals.json")

            print("\nFetching sales (detailed mode)...")
            sales = await scraper.scrape_suburb_detailed(
                suburb=args.suburb,
                city=args.city,
                province=args.province,
                listing_type="sale",
                max_listings=args.max_listings
            )
            if sales:
                save_listings(sales, f"{args.suburb}_sales.json")
        else:
            # Fast mode - just get URLs from search pages
            print("Fetching rentals...")
            rentals = await scraper.scrape_suburb(
                suburb=args.suburb,
                city=args.city,
                province=args.province,
                listing_type="rent",
                max_pages=args.pages
            )
            if rentals:
                save_listings(rentals, f"{args.suburb}_rentals.json")

            print("\nFetching sales...")
            sales = await scraper.scrape_suburb(
                suburb=args.suburb,
                city=args.city,
                province=args.province,
                listing_type="sale",
                max_pages=args.pages
            )
            if sales:
                save_listings(sales, f"{args.suburb}_sales.json")

        print(f"\nDone! Found {len(rentals)} rentals and {len(sales)} sales listings.")

        # Show summary if we have price data
        if rentals:
            prices = [r.price for r in rentals if r.price]
            if prices:
                print(f"\nRental Summary:")
                print(f"  Median: R {sorted(prices)[len(prices)//2]:,}")
                print(f"  Range: R {min(prices):,} - R {max(prices):,}")

        if sales:
            prices = [s.price for s in sales if s.price]
            if prices:
                print(f"\nSales Summary:")
                print(f"  Median: R {sorted(prices)[len(prices)//2]:,}")
                print(f"  Range: R {min(prices):,} - R {max(prices):,}")


def cmd_analyze(args):
    """Analyze scraped data for a suburb."""
    analyzer = SuburbAnalyzer(data_dir=Path(__file__).parent / "data")
    metrics = analyzer.analyze_suburb(args.suburb)

    print(analyzer.generate_report(metrics))

    if args.detailed:
        print("\n")
        print(analyzer.yield_breakdown(metrics))


def cmd_compare(args):
    """Compare multiple suburbs."""
    analyzer = SuburbAnalyzer(data_dir=Path(__file__).parent / "data")
    all_metrics = analyzer.compare_suburbs(args.suburbs)

    print("\n=== SUBURB COMPARISON ===\n")
    print(f"{'Suburb':<15} {'Rentals':<8} {'Sales':<8} {'Med Rent':<12} {'Med Price':<15} {'Gross %':<10} {'Net %':<10}")
    print("-" * 90)

    for m in all_metrics:
        rent_str = f"R {m.median_rent:,.0f}" if m.median_rent else "N/A"
        price_str = f"R {m.median_price:,.0f}" if m.median_price else "N/A"
        gross_str = f"{m.gross_yield:.2f}%" if m.gross_yield else "N/A"
        net_str = f"{m.estimated_net_yield:.2f}%" if m.estimated_net_yield else "N/A"

        print(f"{m.suburb:<15} {m.rental_count:<8} {m.sales_count:<8} {rent_str:<12} {price_str:<15} {gross_str:<10} {net_str:<10}")


def main():
    parser = argparse.ArgumentParser(
        description="The Winning Formula - Property Analysis Tools"
    )
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Scrape command
    scrape_parser = subparsers.add_parser("scrape", help="Scrape Property24 listings")
    scrape_parser.add_argument("suburb", help="Suburb name (e.g., kenilworth)")
    scrape_parser.add_argument("--city", default="cape-town", help="City (default: cape-town)")
    scrape_parser.add_argument("--province", default="western-cape", help="Province (default: western-cape)")
    scrape_parser.add_argument("--pages", type=int, default=3, help="Max pages to scrape in fast mode (default: 3)")
    scrape_parser.add_argument("--max-listings", type=int, default=20, help="Max listings in detailed mode (default: 20)")
    scrape_parser.add_argument("--detailed", "-d", action="store_true", help="Use detailed mode (slower but gets prices)")
    scrape_parser.add_argument("--show-browser", action="store_true", help="Show browser window")
    scrape_parser.set_defaults(func=lambda args: asyncio.run(cmd_scrape(args)))

    # Analyze command
    analyze_parser = subparsers.add_parser("analyze", help="Analyze scraped suburb data")
    analyze_parser.add_argument("suburb", help="Suburb name")
    analyze_parser.add_argument("--detailed", "-d", action="store_true", help="Show detailed yield breakdown")
    analyze_parser.set_defaults(func=cmd_analyze)

    # Compare command
    compare_parser = subparsers.add_parser("compare", help="Compare multiple suburbs")
    compare_parser.add_argument("suburbs", nargs="+", help="Suburb names to compare")
    compare_parser.set_defaults(func=cmd_compare)

    args = parser.parse_args()

    if args.command:
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
