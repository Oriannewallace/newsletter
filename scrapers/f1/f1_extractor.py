"""
F1 Data Extractor for The Winning Formula Newsletter
Uses FastF1 to extract lap times, race results, and performance data.
"""

import fastf1
from fastf1 import plotting
import pandas as pd
from pathlib import Path
from dataclasses import dataclass
from typing import Optional
import json


# Enable FastF1 cache for faster subsequent loads
CACHE_DIR = Path(__file__).parent / "cache"
CACHE_DIR.mkdir(exist_ok=True)
fastf1.Cache.enable_cache(str(CACHE_DIR))


@dataclass
class RaceAnalysis:
    """Container for race analysis results."""
    year: int
    race_name: str
    winner: str
    fastest_lap_driver: str
    fastest_lap_time: str
    total_laps: int
    safety_cars: int
    dnfs: int


class F1Extractor:
    """Extract and analyze F1 data using FastF1."""

    def __init__(self, year: int = 2024):
        self.year = year
        self._schedule = None

    @property
    def schedule(self) -> pd.DataFrame:
        """Get the race schedule for the year."""
        if self._schedule is None:
            self._schedule = fastf1.get_event_schedule(self.year)
        return self._schedule

    def list_races(self) -> list[dict]:
        """List all races in the season."""
        races = []
        for _, event in self.schedule.iterrows():
            if event['EventFormat'] != 'testing':
                races.append({
                    'round': event['RoundNumber'],
                    'name': event['EventName'],
                    'country': event['Country'],
                    'date': str(event['EventDate']),
                    'format': event['EventFormat']
                })
        return races

    def get_session(self, race: str | int, session_type: str = 'R'):
        """
        Load a session.

        Args:
            race: Race name or round number
            session_type: 'R' (Race), 'Q' (Qualifying), 'FP1', 'FP2', 'FP3', 'S' (Sprint)

        Returns:
            FastF1 Session object
        """
        session = fastf1.get_session(self.year, race, session_type)
        session.load()
        return session

    def get_race_results(self, race: str | int) -> pd.DataFrame:
        """Get final race results."""
        session = self.get_session(race, 'R')
        results = session.results[['Position', 'Abbreviation', 'TeamName',
                                    'GridPosition', 'Status', 'Points']].copy()
        results['PositionChange'] = results['GridPosition'] - results['Position']
        return results

    def get_qualifying_results(self, race: str | int) -> pd.DataFrame:
        """Get qualifying results."""
        session = self.get_session(race, 'Q')
        return session.results[['Position', 'Abbreviation', 'TeamName',
                                'Q1', 'Q2', 'Q3']].copy()

    def get_lap_times(self, race: str | int, driver: Optional[str] = None) -> pd.DataFrame:
        """
        Get lap times for a race.

        Args:
            race: Race name or round number
            driver: Optional driver abbreviation (e.g., 'VER', 'HAM')

        Returns:
            DataFrame with lap times
        """
        session = self.get_session(race, 'R')
        laps = session.laps

        if driver:
            laps = laps.pick_drivers(driver)

        return laps[['Driver', 'LapNumber', 'LapTime', 'Sector1Time',
                     'Sector2Time', 'Sector3Time', 'Compound', 'TyreLife',
                     'IsPersonalBest']].copy()

    def get_driver_lap_analysis(self, race: str | int, driver: str) -> dict:
        """
        Detailed lap analysis for a driver.

        Returns stats like average pace, consistency, tire deg, etc.
        """
        laps = self.get_lap_times(race, driver)

        # Filter out pit laps and safety car laps (very slow laps)
        valid_laps = laps[laps['LapTime'].notna()].copy()
        valid_laps['LapTimeSeconds'] = valid_laps['LapTime'].dt.total_seconds()

        # Remove outliers (pit laps, SC laps) - laps more than 20% slower than median
        median_time = valid_laps['LapTimeSeconds'].median()
        clean_laps = valid_laps[valid_laps['LapTimeSeconds'] < median_time * 1.2]

        if len(clean_laps) == 0:
            return {'driver': driver, 'error': 'No valid laps found'}

        # Calculate stats
        lap_times = clean_laps['LapTimeSeconds']

        return {
            'driver': driver,
            'total_laps': len(laps),
            'valid_laps': len(clean_laps),
            'average_lap': lap_times.mean(),
            'fastest_lap': lap_times.min(),
            'slowest_lap': lap_times.max(),
            'std_dev': lap_times.std(),  # Consistency measure
            'consistency_score': 100 - (lap_times.std() / lap_times.mean() * 100),  # Higher = more consistent
            'tire_compounds_used': clean_laps['Compound'].unique().tolist(),
        }

    def compare_drivers(self, race: str | int, drivers: list[str]) -> pd.DataFrame:
        """Compare multiple drivers' performance in a race."""
        comparisons = []
        for driver in drivers:
            analysis = self.get_driver_lap_analysis(race, driver)
            if 'error' not in analysis:
                comparisons.append(analysis)

        return pd.DataFrame(comparisons)

    def get_position_changes(self, race: str | int) -> pd.DataFrame:
        """Analyze position changes from grid to finish."""
        results = self.get_race_results(race)
        results = results.sort_values('PositionChange', ascending=False)
        return results[['Abbreviation', 'TeamName', 'GridPosition',
                        'Position', 'PositionChange', 'Points']]

    def get_team_performance(self, race: str | int) -> pd.DataFrame:
        """Analyze team performance (combined driver results)."""
        results = self.get_race_results(race)
        team_stats = results.groupby('TeamName').agg({
            'Points': 'sum',
            'Position': 'mean',
            'PositionChange': 'mean'
        }).round(2)
        team_stats.columns = ['TotalPoints', 'AvgPosition', 'AvgPositionChange']
        return team_stats.sort_values('TotalPoints', ascending=False)

    def get_season_standings(self) -> tuple[pd.DataFrame, pd.DataFrame]:
        """Get current driver and constructor standings."""
        # FastF1 doesn't directly provide standings, we need to calculate
        # For now, return the latest available
        driver_standings = []
        constructor_standings = {}

        # Get results from each race
        for event in self.schedule.iterrows():
            event = event[1]
            if event['EventFormat'] == 'testing':
                continue

            try:
                results = self.get_race_results(event['RoundNumber'])
                for _, row in results.iterrows():
                    driver_standings.append({
                        'Driver': row['Abbreviation'],
                        'Team': row['TeamName'],
                        'Points': row['Points']
                    })
            except Exception:
                continue  # Race hasn't happened yet

        # Aggregate
        if driver_standings:
            df = pd.DataFrame(driver_standings)
            drivers = df.groupby(['Driver', 'Team'])['Points'].sum().reset_index()
            drivers = drivers.sort_values('Points', ascending=False)

            constructors = df.groupby('Team')['Points'].sum().reset_index()
            constructors = constructors.sort_values('Points', ascending=False)

            return drivers, constructors

        return pd.DataFrame(), pd.DataFrame()


def format_laptime(seconds: float) -> str:
    """Format lap time in seconds to MM:SS.mmm"""
    if pd.isna(seconds):
        return "N/A"
    mins = int(seconds // 60)
    secs = seconds % 60
    return f"{mins}:{secs:06.3f}"


def main():
    """Example usage."""
    extractor = F1Extractor(year=2024)

    # List races
    print("=== 2024 F1 Season ===\n")
    races = extractor.list_races()
    for race in races[:5]:  # First 5 races
        print(f"Round {race['round']}: {race['name']} ({race['country']})")

    print("\n" + "=" * 50)

    # Analyze a specific race (Bahrain GP - Round 1)
    print("\n=== Bahrain GP Analysis ===\n")

    try:
        # Race results
        print("Top 10 Finishers:")
        results = extractor.get_race_results(1)
        print(results.head(10).to_string(index=False))

        print("\n\nBiggest Position Gainers:")
        changes = extractor.get_position_changes(1)
        print(changes.head(5).to_string(index=False))

        print("\n\nTeam Performance:")
        teams = extractor.get_team_performance(1)
        print(teams.to_string())

        print("\n\nDriver Comparison (VER vs LEC):")
        comparison = extractor.compare_drivers(1, ['VER', 'LEC'])
        for _, row in comparison.iterrows():
            print(f"\n{row['driver']}:")
            print(f"  Avg Lap: {format_laptime(row['average_lap'])}")
            print(f"  Fastest: {format_laptime(row['fastest_lap'])}")
            print(f"  Consistency: {row['consistency_score']:.1f}%")

    except Exception as e:
        print(f"Error loading race data: {e}")
        print("(Race data may not be available yet)")


if __name__ == "__main__":
    main()
