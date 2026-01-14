#!/usr/bin/env python3
"""
CLI for F1 data analysis tools.

Usage:
    python cli.py races                     # List all races
    python cli.py results 1                 # Show race results for round 1
    python cli.py compare 1 VER LEC HAM     # Compare drivers in round 1
    python cli.py consistency 1             # Analyze driver consistency
    python cli.py teammates 1               # Compare teammates
    python cli.py summary 1                 # Full race summary
"""

import argparse
import sys
from pathlib import Path

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from f1_extractor import F1Extractor, format_laptime
from f1_analyzer import F1Analyzer


def cmd_races(args):
    """List all races in the season."""
    extractor = F1Extractor(args.year)
    races = extractor.list_races()

    print(f"\n=== {args.year} F1 Season ===\n")
    print(f"{'Round':<6} {'Race':<30} {'Country':<20} {'Date':<12}")
    print("-" * 70)

    for race in races:
        print(f"{race['round']:<6} {race['name']:<30} {race['country']:<20} {race['date']:<12}")


def cmd_results(args):
    """Show race results."""
    extractor = F1Extractor(args.year)

    print(f"\n=== Race Results: Round {args.race} ===\n")

    try:
        results = extractor.get_race_results(args.race)
        print(results.to_string(index=False))
    except Exception as e:
        print(f"Error loading results: {e}")


def cmd_qualifying(args):
    """Show qualifying results."""
    extractor = F1Extractor(args.year)

    print(f"\n=== Qualifying Results: Round {args.race} ===\n")

    try:
        results = extractor.get_qualifying_results(args.race)
        print(results.to_string(index=False))
    except Exception as e:
        print(f"Error loading qualifying: {e}")


def cmd_compare(args):
    """Compare drivers in a race."""
    extractor = F1Extractor(args.year)

    print(f"\n=== Driver Comparison: Round {args.race} ===")
    print(f"Drivers: {', '.join(args.drivers)}\n")

    try:
        comparison = extractor.compare_drivers(args.race, args.drivers)

        for _, row in comparison.iterrows():
            print(f"{row['driver']}:")
            print(f"  Average Lap:    {format_laptime(row['average_lap'])}")
            print(f"  Fastest Lap:    {format_laptime(row['fastest_lap'])}")
            print(f"  Consistency:    {row['consistency_score']:.1f}%")
            print(f"  Std Deviation:  {row['std_dev']:.3f}s")
            print(f"  Valid Laps:     {row['valid_laps']}")
            print()

    except Exception as e:
        print(f"Error: {e}")


def cmd_consistency(args):
    """Analyze driver consistency."""
    analyzer = F1Analyzer(args.year)

    print(f"\n=== Driver Consistency: Round {args.race} ===\n")

    try:
        consistency = analyzer.analyze_driver_consistency(args.race, args.top)

        print(f"{'Driver':<8} {'Avg Lap':<12} {'Fastest':<12} {'Std Dev':<10} {'Consistency':<12}")
        print("-" * 55)

        for _, row in consistency.iterrows():
            print(f"{row['Driver']:<8} "
                  f"{format_laptime(row['AvgLap']):<12} "
                  f"{format_laptime(row['FastestLap']):<12} "
                  f"{row['StdDev']:.3f}s    "
                  f"{row['ConsistencyScore']:.1f}%")

    except Exception as e:
        print(f"Error: {e}")


def cmd_teammates(args):
    """Compare teammates."""
    analyzer = F1Analyzer(args.year)

    print(f"\n=== Teammate Battles: Round {args.race} ===\n")

    try:
        battles = analyzer.compare_teammates(args.race)

        for battle in battles:
            winner = battle['faster_driver']
            loser = battle['driver1'] if winner == battle['driver2'] else battle['driver2']
            print(f"{battle['team']}:")
            print(f"  {winner} (P{battle['driver1_pos'] if winner == battle['driver1'] else battle['driver2_pos']}) "
                  f"beat {loser} (P{battle['driver2_pos'] if winner == battle['driver1'] else battle['driver1_pos']})")
            print(f"  Gap: {battle['gap_seconds']:.3f}s per lap")
            print()

    except Exception as e:
        print(f"Error: {e}")


def cmd_summary(args):
    """Generate race summary."""
    analyzer = F1Analyzer(args.year)

    try:
        summary = analyzer.generate_race_summary(args.race)
        print(summary)
    except Exception as e:
        print(f"Error generating summary: {e}")


def cmd_teams(args):
    """Show team performance."""
    extractor = F1Extractor(args.year)

    print(f"\n=== Team Performance: Round {args.race} ===\n")

    try:
        teams = extractor.get_team_performance(args.race)
        print(teams.to_string())
    except Exception as e:
        print(f"Error: {e}")


def cmd_strategy(args):
    """Analyze tire strategy for a driver."""
    analyzer = F1Analyzer(args.year)

    print(f"\n=== Tire Strategy: {args.driver} in Round {args.race} ===\n")

    try:
        strategy = analyzer.analyze_tire_strategy(args.race, args.driver)

        print(f"Driver: {strategy['driver']}")
        print(f"Total Stints: {strategy['total_stints']}")
        print(f"Compounds Used: {', '.join(strategy['compounds_used'])}")
        print()

        print(f"{'Stint':<6} {'Compound':<10} {'Laps':<6} {'Avg Pace':<12} {'Best Lap':<12} {'Deg/Lap':<10}")
        print("-" * 60)

        for stint in strategy['stints']:
            deg_str = f"{stint['deg_per_lap']:.3f}s" if stint['deg_per_lap'] else "N/A"
            print(f"{stint['stint']:<6} "
                  f"{stint['compound']:<10} "
                  f"{stint['laps']:<6} "
                  f"{format_laptime(stint['avg_pace']):<12} "
                  f"{format_laptime(stint['best_lap']):<12} "
                  f"{deg_str:<10}")

    except Exception as e:
        print(f"Error: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="F1 Data Analysis Tools for The Winning Formula"
    )
    parser.add_argument("--year", type=int, default=2024, help="F1 season year (default: 2024)")

    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Races command
    races_parser = subparsers.add_parser("races", help="List all races in the season")
    races_parser.set_defaults(func=cmd_races)

    # Results command
    results_parser = subparsers.add_parser("results", help="Show race results")
    results_parser.add_argument("race", type=int, help="Race round number")
    results_parser.set_defaults(func=cmd_results)

    # Qualifying command
    quali_parser = subparsers.add_parser("qualifying", help="Show qualifying results")
    quali_parser.add_argument("race", type=int, help="Race round number")
    quali_parser.set_defaults(func=cmd_qualifying)

    # Compare command
    compare_parser = subparsers.add_parser("compare", help="Compare drivers")
    compare_parser.add_argument("race", type=int, help="Race round number")
    compare_parser.add_argument("drivers", nargs="+", help="Driver abbreviations (e.g., VER LEC HAM)")
    compare_parser.set_defaults(func=cmd_compare)

    # Consistency command
    consistency_parser = subparsers.add_parser("consistency", help="Analyze driver consistency")
    consistency_parser.add_argument("race", type=int, help="Race round number")
    consistency_parser.add_argument("--top", type=int, default=10, help="Number of drivers to analyze")
    consistency_parser.set_defaults(func=cmd_consistency)

    # Teammates command
    teammates_parser = subparsers.add_parser("teammates", help="Compare teammates")
    teammates_parser.add_argument("race", type=int, help="Race round number")
    teammates_parser.set_defaults(func=cmd_teammates)

    # Summary command
    summary_parser = subparsers.add_parser("summary", help="Generate race summary")
    summary_parser.add_argument("race", type=int, help="Race round number")
    summary_parser.set_defaults(func=cmd_summary)

    # Teams command
    teams_parser = subparsers.add_parser("teams", help="Show team performance")
    teams_parser.add_argument("race", type=int, help="Race round number")
    teams_parser.set_defaults(func=cmd_teams)

    # Strategy command
    strategy_parser = subparsers.add_parser("strategy", help="Analyze tire strategy")
    strategy_parser.add_argument("race", type=int, help="Race round number")
    strategy_parser.add_argument("driver", help="Driver abbreviation (e.g., VER)")
    strategy_parser.set_defaults(func=cmd_strategy)

    args = parser.parse_args()

    if args.command:
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
