"""
Suburb Analysis Module for The Winning Formula Newsletter
Calculates yield, market metrics, and investment insights from scraped data.
"""

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Optional
import statistics


@dataclass
class SuburbMetrics:
    """Comprehensive metrics for a suburb."""
    suburb: str

    # Rental metrics
    rental_count: int
    avg_rent: Optional[float]
    median_rent: Optional[float]
    min_rent: Optional[float]
    max_rent: Optional[float]
    rent_std_dev: Optional[float]

    # Sales metrics
    sales_count: int
    avg_price: Optional[float]
    median_price: Optional[float]
    min_price: Optional[float]
    max_price: Optional[float]
    price_std_dev: Optional[float]

    # Yield metrics
    gross_yield: Optional[float]  # Annual rent / price as percentage
    estimated_net_yield: Optional[float]  # After typical expenses

    # Property mix
    property_types: dict
    bedroom_distribution: dict

    # Market signals
    price_to_rent_ratio: Optional[float]


class SuburbAnalyzer:
    """Analyzes property data to generate investment insights."""

    # Typical expense ratios for net yield calculation
    VACANCY_RATE = 0.05  # 5% vacancy
    MANAGEMENT_FEE = 0.08  # 8% of rent
    MAINTENANCE_RATE = 0.01  # 1% of property value annually
    INSURANCE_RATE = 0.002  # 0.2% of property value
    RATES_ESTIMATE = 0.005  # 0.5% of property value (varies by area)

    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)

    def load_listings(self, filename: str) -> list[dict]:
        """Load listings from JSON file."""
        filepath = self.data_dir / filename
        if not filepath.exists():
            return []
        with open(filepath) as f:
            return json.load(f)

    def _calculate_stats(self, values: list[float]) -> dict:
        """Calculate basic statistics for a list of values."""
        if not values:
            return {"avg": None, "median": None, "min": None, "max": None, "std": None}

        return {
            "avg": statistics.mean(values),
            "median": statistics.median(values),
            "min": min(values),
            "max": max(values),
            "std": statistics.stdev(values) if len(values) > 1 else 0
        }

    def _count_property_types(self, listings: list[dict]) -> dict:
        """Count listings by property type."""
        counts = {}
        for listing in listings:
            ptype = listing.get("property_type", "Unknown")
            counts[ptype] = counts.get(ptype, 0) + 1
        return counts

    def _count_bedrooms(self, listings: list[dict]) -> dict:
        """Count listings by bedroom count."""
        counts = {}
        for listing in listings:
            beds = listing.get("bedrooms")
            if beds is not None:
                key = f"{beds} bed"
                counts[key] = counts.get(key, 0) + 1
        return counts

    def analyze_suburb(self, suburb: str) -> SuburbMetrics:
        """
        Analyze a suburb using scraped rental and sales data.

        Args:
            suburb: Suburb name (used to find data files)

        Returns:
            SuburbMetrics with comprehensive analysis
        """
        # Load data
        rentals = self.load_listings(f"{suburb}_rentals.json")
        sales = self.load_listings(f"{suburb}_sales.json")

        # Extract prices
        rental_prices = [r["price"] for r in rentals if r.get("price")]
        sale_prices = [s["price"] for s in sales if s.get("price")]

        # Calculate statistics
        rental_stats = self._calculate_stats(rental_prices)
        sale_stats = self._calculate_stats(sale_prices)

        # Calculate yields
        gross_yield = None
        net_yield = None
        price_to_rent = None

        if rental_stats["median"] and sale_stats["median"]:
            annual_rent = rental_stats["median"] * 12
            median_price = sale_stats["median"]

            # Gross yield
            gross_yield = (annual_rent / median_price) * 100

            # Net yield (after typical expenses)
            effective_rent = annual_rent * (1 - self.VACANCY_RATE)
            management_cost = effective_rent * self.MANAGEMENT_FEE
            maintenance_cost = median_price * self.MAINTENANCE_RATE
            insurance_cost = median_price * self.INSURANCE_RATE
            rates_cost = median_price * self.RATES_ESTIMATE

            net_income = effective_rent - management_cost - maintenance_cost - insurance_cost - rates_cost
            net_yield = (net_income / median_price) * 100

            # Price to rent ratio (years of rent to buy)
            price_to_rent = median_price / annual_rent

        # Combine property type counts
        all_listings = rentals + sales
        property_types = self._count_property_types(all_listings)
        bedroom_dist = self._count_bedrooms(all_listings)

        return SuburbMetrics(
            suburb=suburb,
            rental_count=len(rentals),
            avg_rent=rental_stats["avg"],
            median_rent=rental_stats["median"],
            min_rent=rental_stats["min"],
            max_rent=rental_stats["max"],
            rent_std_dev=rental_stats["std"],
            sales_count=len(sales),
            avg_price=sale_stats["avg"],
            median_price=sale_stats["median"],
            min_price=sale_stats["min"],
            max_price=sale_stats["max"],
            price_std_dev=sale_stats["std"],
            gross_yield=gross_yield,
            estimated_net_yield=net_yield,
            property_types=property_types,
            bedroom_distribution=bedroom_dist,
            price_to_rent_ratio=price_to_rent
        )

    def compare_suburbs(self, suburbs: list[str]) -> list[SuburbMetrics]:
        """Compare multiple suburbs."""
        return [self.analyze_suburb(suburb) for suburb in suburbs]

    def generate_report(self, metrics: SuburbMetrics) -> str:
        """Generate a human-readable report."""
        lines = [
            f"=== {metrics.suburb.title()} Market Analysis ===",
            "",
            "RENTAL MARKET",
            f"  Listings: {metrics.rental_count}",
        ]

        if metrics.median_rent:
            lines.extend([
                f"  Median Rent: R {metrics.median_rent:,.0f} /month",
                f"  Range: R {metrics.min_rent:,.0f} - R {metrics.max_rent:,.0f}",
                f"  Std Dev: R {metrics.rent_std_dev:,.0f}" if metrics.rent_std_dev else "",
            ])

        lines.extend([
            "",
            "SALES MARKET",
            f"  Listings: {metrics.sales_count}",
        ])

        if metrics.median_price:
            lines.extend([
                f"  Median Price: R {metrics.median_price:,.0f}",
                f"  Range: R {metrics.min_price:,.0f} - R {metrics.max_price:,.0f}",
            ])

        lines.extend([
            "",
            "INVESTMENT METRICS",
        ])

        if metrics.gross_yield:
            lines.extend([
                f"  Gross Yield: {metrics.gross_yield:.2f}%",
                f"  Est. Net Yield: {metrics.estimated_net_yield:.2f}%",
                f"  Price-to-Rent Ratio: {metrics.price_to_rent_ratio:.1f} years",
            ])

        lines.extend([
            "",
            "PROPERTY MIX",
            f"  Types: {metrics.property_types}",
            f"  Bedrooms: {metrics.bedroom_distribution}",
        ])

        return "\n".join(lines)

    def yield_breakdown(self, metrics: SuburbMetrics) -> str:
        """Generate detailed yield breakdown like in the newsletter."""
        if not metrics.median_rent or not metrics.median_price:
            return "Insufficient data for yield breakdown."

        annual_rent = metrics.median_rent * 12
        price = metrics.median_price

        # Calculate each component
        vacancy_loss = annual_rent * self.VACANCY_RATE
        effective_rent = annual_rent - vacancy_loss
        management = effective_rent * self.MANAGEMENT_FEE
        maintenance = price * self.MAINTENANCE_RATE
        insurance = price * self.INSURANCE_RATE
        rates = price * self.RATES_ESTIMATE
        net_income = effective_rent - management - maintenance - insurance - rates

        return f"""
YIELD BREAKDOWN: {metrics.suburb.title()}
{"=" * 50}

GROSS INCOME
  Annual Rent (R {metrics.median_rent:,.0f} x 12):    R {annual_rent:,.0f}
  Less: Vacancy ({self.VACANCY_RATE*100:.0f}%):                 -R {vacancy_loss:,.0f}
  Effective Gross Income:                R {effective_rent:,.0f}

EXPENSES
  Property Management ({self.MANAGEMENT_FEE*100:.0f}%):          -R {management:,.0f}
  Maintenance ({self.MAINTENANCE_RATE*100:.1f}% of value):        -R {maintenance:,.0f}
  Insurance ({self.INSURANCE_RATE*100:.1f}% of value):           -R {insurance:,.0f}
  Rates & Levies (est.):                 -R {rates:,.0f}

NET OPERATING INCOME:                    R {net_income:,.0f}

{"=" * 50}
PROPERTY VALUE:                          R {price:,.0f}

GROSS YIELD:                             {metrics.gross_yield:.2f}%
NET YIELD:                               {metrics.estimated_net_yield:.2f}%
PRICE-TO-RENT RATIO:                     {metrics.price_to_rent_ratio:.1f} years

INTERPRETATION:
{"> 5% net yield = Good cash flow" if metrics.estimated_net_yield and metrics.estimated_net_yield > 5 else ""}
{"  3-5% net yield = Moderate, watch expenses" if metrics.estimated_net_yield and 3 <= metrics.estimated_net_yield <= 5 else ""}
{"  < 3% net yield = Growth play, not cash flow" if metrics.estimated_net_yield and metrics.estimated_net_yield < 3 else ""}
{"  Price-to-rent < 15 = Generally affordable" if metrics.price_to_rent_ratio and metrics.price_to_rent_ratio < 15 else ""}
{"  Price-to-rent > 20 = Premium market" if metrics.price_to_rent_ratio and metrics.price_to_rent_ratio > 20 else ""}
"""


async def main():
    """Example usage."""
    analyzer = SuburbAnalyzer(data_dir=Path(__file__).parent / "data")

    # Analyze Kenilworth
    metrics = analyzer.analyze_suburb("kenilworth")

    print(analyzer.generate_report(metrics))
    print("\n")
    print(analyzer.yield_breakdown(metrics))


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
