"""
F1 Analysis Module for The Winning Formula Newsletter
Generates newsletter-ready insights from F1 data.
"""

import pandas as pd
from typing import Optional
from dataclasses import dataclass

from f1_extractor import F1Extractor, format_laptime


@dataclass
class RaceInsight:
    """A newsletter-ready insight from race data."""
    headline: str
    key_stat: str
    explanation: str
    data_points: list[str]


class F1Analyzer:
    """Generate newsletter insights from F1 data."""

    def __init__(self, year: int = 2024):
        self.extractor = F1Extractor(year)
        self.year = year

    def analyze_qualifying_vs_race(self, race: str | int) -> RaceInsight:
        """
        Analyze how qualifying position affected race results.
        Great for: "Does pole position actually matter?"
        """
        results = self.extractor.get_race_results(race)
        results = results[results['Position'].notna()]

        # Pole position win rate for this race
        pole_winner = results[results['GridPosition'] == 1]['Position'].iloc[0] == 1

        # Average position change
        avg_change = results['PositionChange'].mean()

        # Biggest mover
        biggest_gainer = results.loc[results['PositionChange'].idxmax()]

        # Correlation between grid and finish
        correlation = results['GridPosition'].corr(results['Position'])

        return RaceInsight(
            headline=f"Qualifying vs Race: {'Pole Converted' if pole_winner else 'Pole Lost'}",
            key_stat=f"Grid-to-finish correlation: {correlation:.2f}",
            explanation=(
                f"A correlation of {correlation:.2f} means qualifying position "
                f"{'strongly' if correlation > 0.7 else 'moderately' if correlation > 0.4 else 'weakly'} "
                f"predicted race finish. "
                f"{'Pole position was converted to a win.' if pole_winner else 'The pole sitter did not win.'}"
            ),
            data_points=[
                f"Pole sitter finished P{int(results[results['GridPosition'] == 1]['Position'].iloc[0])}",
                f"Average position change: {avg_change:+.1f} places",
                f"Biggest gainer: {biggest_gainer['Abbreviation']} (+{int(biggest_gainer['PositionChange'])} places)",
                f"Grid-Finish correlation: {correlation:.2f}"
            ]
        )

    def analyze_tire_strategy(self, race: str | int, driver: str) -> dict:
        """
        Analyze a driver's tire strategy and its impact.
        Great for: "Why this strategy won the race"
        """
        laps = self.extractor.get_lap_times(race, driver)
        laps = laps[laps['LapTime'].notna()].copy()
        laps['LapTimeSeconds'] = laps['LapTime'].dt.total_seconds()

        # Find stint boundaries (compound changes)
        laps['StintChange'] = laps['Compound'] != laps['Compound'].shift()
        laps['Stint'] = laps['StintChange'].cumsum()

        stint_analysis = []
        for stint_num in laps['Stint'].unique():
            stint_laps = laps[laps['Stint'] == stint_num]
            compound = stint_laps['Compound'].iloc[0]
            stint_length = len(stint_laps)

            # Calculate tire degradation (pace loss per lap)
            if stint_length > 3:
                # Simple linear regression for deg
                first_5_avg = stint_laps.head(5)['LapTimeSeconds'].mean()
                last_5_avg = stint_laps.tail(5)['LapTimeSeconds'].mean()
                deg_per_lap = (last_5_avg - first_5_avg) / max(stint_length - 5, 1)
            else:
                deg_per_lap = 0

            stint_analysis.append({
                'stint': stint_num,
                'compound': compound,
                'laps': stint_length,
                'avg_pace': stint_laps['LapTimeSeconds'].mean(),
                'best_lap': stint_laps['LapTimeSeconds'].min(),
                'deg_per_lap': deg_per_lap
            })

        return {
            'driver': driver,
            'total_stints': len(stint_analysis),
            'stints': stint_analysis,
            'compounds_used': laps['Compound'].unique().tolist()
        }

    def analyze_driver_consistency(self, race: str | int, top_n: int = 10) -> pd.DataFrame:
        """
        Rank drivers by consistency (low lap time variance = consistent).
        Great for: "The most consistent drivers aren't always the fastest"
        """
        results = self.extractor.get_race_results(race)
        top_drivers = results.head(top_n)['Abbreviation'].tolist()

        consistency_data = []
        for driver in top_drivers:
            analysis = self.extractor.get_driver_lap_analysis(race, driver)
            if 'error' not in analysis:
                consistency_data.append({
                    'Driver': driver,
                    'AvgLap': analysis['average_lap'],
                    'FastestLap': analysis['fastest_lap'],
                    'StdDev': analysis['std_dev'],
                    'ConsistencyScore': analysis['consistency_score'],
                    'ValidLaps': analysis['valid_laps']
                })

        df = pd.DataFrame(consistency_data)
        df = df.sort_values('ConsistencyScore', ascending=False)
        return df

    def compare_teammates(self, race: str | int) -> list[dict]:
        """
        Compare teammate performance.
        Great for: "Who's beating their teammate?"
        """
        results = self.extractor.get_race_results(race)

        teams = results.groupby('TeamName')
        comparisons = []

        for team_name, team_drivers in teams:
            if len(team_drivers) == 2:
                d1, d2 = team_drivers.iloc[0], team_drivers.iloc[1]

                # Get lap data for both
                try:
                    d1_analysis = self.extractor.get_driver_lap_analysis(race, d1['Abbreviation'])
                    d2_analysis = self.extractor.get_driver_lap_analysis(race, d2['Abbreviation'])

                    if 'error' in d1_analysis or 'error' in d2_analysis:
                        continue

                    gap = d1_analysis['average_lap'] - d2_analysis['average_lap']

                    comparisons.append({
                        'team': team_name,
                        'driver1': d1['Abbreviation'],
                        'driver1_pos': int(d1['Position']),
                        'driver1_avg': d1_analysis['average_lap'],
                        'driver2': d2['Abbreviation'],
                        'driver2_pos': int(d2['Position']),
                        'driver2_avg': d2_analysis['average_lap'],
                        'gap_seconds': abs(gap),
                        'faster_driver': d1['Abbreviation'] if gap < 0 else d2['Abbreviation']
                    })
                except Exception:
                    continue

        return sorted(comparisons, key=lambda x: x['gap_seconds'], reverse=True)

    def generate_race_summary(self, race: str | int) -> str:
        """Generate a newsletter-ready race summary."""
        results = self.extractor.get_race_results(race)
        quali_insight = self.analyze_qualifying_vs_race(race)
        teams = self.extractor.get_team_performance(race)

        winner = results.iloc[0]
        podium = results.head(3)

        summary = f"""
## Race Summary

**Winner:** {winner['Abbreviation']} ({winner['TeamName']})
**Podium:** {', '.join(podium['Abbreviation'].tolist())}

### Key Insight: {quali_insight.headline}
{quali_insight.explanation}

**Data Points:**
"""
        for point in quali_insight.data_points:
            summary += f"- {point}\n"

        summary += f"""
### Team Performance
| Team | Points | Avg Position |
|------|--------|--------------|
"""
        for team, row in teams.head(5).iterrows():
            summary += f"| {team} | {int(row['TotalPoints'])} | {row['AvgPosition']:.1f} |\n"

        return summary

    def find_upgrade_impact(self, race1: str | int, race2: str | int, team: str) -> dict:
        """
        Compare team performance between two races to spot upgrade impact.
        Great for: "Why this upgrade mattered more than pole position"
        """
        try:
            results1 = self.extractor.get_race_results(race1)
            results2 = self.extractor.get_race_results(race2)

            team1 = results1[results1['TeamName'] == team]
            team2 = results2[results2['TeamName'] == team]

            if len(team1) == 0 or len(team2) == 0:
                return {'error': f'Team {team} not found in one or both races'}

            # Compare average positions
            avg_pos1 = team1['Position'].mean()
            avg_pos2 = team2['Position'].mean()
            pos_improvement = avg_pos1 - avg_pos2

            # Compare points
            points1 = team1['Points'].sum()
            points2 = team2['Points'].sum()

            return {
                'team': team,
                'race1_avg_position': avg_pos1,
                'race2_avg_position': avg_pos2,
                'position_improvement': pos_improvement,
                'race1_points': points1,
                'race2_points': points2,
                'points_improvement': points2 - points1,
                'interpretation': (
                    f"{team} improved by {pos_improvement:.1f} positions on average "
                    f"and scored {points2 - points1:+.0f} more points."
                    if pos_improvement > 0 else
                    f"{team} dropped {abs(pos_improvement):.1f} positions on average."
                )
            }
        except Exception as e:
            return {'error': str(e)}


def main():
    """Example analysis."""
    analyzer = F1Analyzer(2024)

    print("=== F1 Analysis Demo ===\n")

    try:
        # Race summary
        print(analyzer.generate_race_summary(1))

        print("\n" + "=" * 50)
        print("\n=== Driver Consistency Analysis ===\n")

        consistency = analyzer.analyze_driver_consistency(1)
        print("Most Consistent Drivers (Top 10 finishers):")
        for _, row in consistency.iterrows():
            print(f"  {row['Driver']}: {row['ConsistencyScore']:.1f}% "
                  f"(avg: {format_laptime(row['AvgLap'])}, std: {row['StdDev']:.3f}s)")

        print("\n" + "=" * 50)
        print("\n=== Teammate Battles ===\n")

        teammates = analyzer.compare_teammates(1)
        for battle in teammates[:5]:
            print(f"{battle['team']}:")
            print(f"  {battle['faster_driver']} beat {battle['driver1'] if battle['faster_driver'] == battle['driver2'] else battle['driver2']}")
            print(f"  Gap: {battle['gap_seconds']:.3f}s per lap on average")
            print()

    except Exception as e:
        print(f"Error: {e}")
        print("(Make sure FastF1 data is available for the selected race)")


if __name__ == "__main__":
    main()
