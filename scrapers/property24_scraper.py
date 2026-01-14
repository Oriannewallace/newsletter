"""
Property24 Scraper for The Winning Formula Newsletter
Scrapes rental and sales listings with full property details.
"""

import asyncio
import json
import re
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Optional

from playwright.async_api import async_playwright, Page


@dataclass
class PropertyListing:
    """Represents a single property listing."""
    url: str
    price: Optional[int]  # in ZAR
    price_text: str
    suburb: str
    property_type: str
    bedrooms: Optional[int]
    bathrooms: Optional[int]
    parking: Optional[int]
    size_sqm: Optional[float]
    title: str
    listing_type: str  # "rent" or "sale"
    scraped_at: str


class Property24Scraper:
    """Scraper for Property24.com listings."""

    BASE_URL = "https://www.property24.com"

    # Known area codes for Cape Town suburbs
    AREA_CODES = {
        "kenilworth": "8669",
        "kenilworth-upper": "14224",
        "claremont": "8667",
        "rondebosch": "8671",
        "newlands": "8670",
        "wynberg": "8675",
        "constantia": "8668",
        "plumstead": "8674",
        "diep-river": "8673",
        "bergvliet": "8666",
        "tokai": "8676",
        "retreat": "8678",
        "muizenberg": "8680",
        "lakeside": "8679",
        "observatory": "8665",
        "mowbray": "8672",
        "gardens": "8659",
        "oranjezicht": "8661",
        "tamboerskloof": "8663",
        "sea-point": "8657",
        "green-point": "8656",
        "waterfront": "8655",
        "camps-bay": "8652",
        "hout-bay": "8651",
        "pinelands": "8683",
        "thornton": "8686",
        "milnerton": "1737",
        "tableview": "10043",
        "bloubergstrand": "1734",
        "parklands": "8684",
        "woodstock": "8664",
        "salt-river": "8681",
    }

    def __init__(self, headless: bool = True):
        self.headless = headless
        self.browser = None
        self.context = None

    async def __aenter__(self):
        playwright = await async_playwright().start()
        self.browser = await playwright.chromium.launch(headless=self.headless)
        self.context = await self.browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        )
        return self

    async def __aexit__(self, *args):
        if self.browser:
            await self.browser.close()

    def _build_url(self, suburb: str, province: str, city: str, listing_type: str, page: int = 1) -> str:
        """Build Property24 search URL."""
        # Property24 URL format: /to-rent/suburb/city/province/area-code
        # or /for-sale/suburb/city/province/area-code
        base = "to-rent" if listing_type == "rent" else "for-sale"
        suburb_slug = suburb.lower().replace(" ", "-")
        city_slug = city.lower().replace(" ", "-")
        province_slug = province.lower().replace(" ", "-")

        # Get area code if known
        area_code = self.AREA_CODES.get(suburb_slug, "")

        url = f"{self.BASE_URL}/{base}/{suburb_slug}/{city_slug}/{province_slug}"
        if area_code:
            url += f"/{area_code}"
        if page > 1:
            url += f"/p{page}"
        return url

    def _parse_price(self, price_text: str) -> Optional[int]:
        """Parse price from text like 'R 8 250' or 'R 1 500 000'."""
        if not price_text:
            return None
        # Remove 'R', spaces, 'pm', 'p/m', etc.
        cleaned = re.sub(r'[^\d]', '', price_text.split('p')[0])
        try:
            return int(cleaned) if cleaned else None
        except ValueError:
            return None

    def _parse_bedrooms(self, text: str) -> Optional[int]:
        """Extract bedroom count from text."""
        match = re.search(r'(\d+)\s*(?:bed|bedroom)', text.lower())
        return int(match.group(1)) if match else None

    def _parse_bathrooms(self, text: str) -> Optional[int]:
        """Extract bathroom count from text."""
        match = re.search(r'(\d+)\s*(?:bath|bathroom)', text.lower())
        return int(match.group(1)) if match else None

    def _parse_size(self, text: str) -> Optional[float]:
        """Extract size in sqm from text."""
        match = re.search(r'(\d+(?:\.\d+)?)\s*m[²2]', text)
        return float(match.group(1)) if match else None

    async def _extract_listings_from_page(self, page: Page, suburb: str, listing_type: str) -> list[PropertyListing]:
        """Extract all listings from a loaded page."""
        listings = []
        seen_urls = set()

        # Wait for page to fully load
        await page.wait_for_load_state("networkidle", timeout=20000)
        await asyncio.sleep(3)  # Extra wait for JS rendering

        # Scroll to trigger lazy loading
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight / 2)")
        await asyncio.sleep(1)
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await asyncio.sleep(2)

        # Property24 uses various selectors - try multiple approaches
        listing_type_path = "to-rent" if listing_type == "rent" else "for-sale"

        # Approach 1: Find all links that look like listing detail pages
        # Listing URLs contain the area code followed by a listing ID
        all_links = await page.query_selector_all(f'a[href*="/{listing_type_path}/"]')

        for link in all_links:
            try:
                href = await link.get_attribute("href")
                if not href:
                    continue

                # Listing detail pages have numeric IDs at the end like /8669/116563352
                if not re.search(r'/\d+/\d+$', href):
                    continue

                url = href if href.startswith("http") else f"{self.BASE_URL}{href}"

                # Skip duplicates
                if url in seen_urls:
                    continue
                seen_urls.add(url)

                # Get the parent tile/card element
                card = link
                for _ in range(5):  # Go up to 5 levels to find card container
                    parent = await card.evaluate_handle("el => el.parentElement")
                    if parent:
                        card = parent
                        parent_class = await card.evaluate("el => el.className || ''")
                        if 'tile' in parent_class.lower() or 'card' in parent_class.lower() or 'listing' in parent_class.lower():
                            break

                # Get text content from the card area
                text_content = await card.evaluate("el => el.innerText || ''")

                # Extract price - look for R followed by numbers
                price_text = ""
                price_match = re.search(r'R\s*([\d\s]+)', text_content)
                if price_match:
                    price_text = "R " + price_match.group(1).strip()

                # Extract title (usually first line or contains bedroom info)
                lines = [l.strip() for l in text_content.split('\n') if l.strip()]
                title = lines[0] if lines else ""

                # Determine property type
                property_type = "Unknown"
                for ptype in ["House", "Apartment", "Flat", "Townhouse", "Studio", "Room", "Commercial"]:
                    if ptype.lower() in text_content.lower():
                        property_type = ptype
                        break

                listing = PropertyListing(
                    url=url,
                    price=self._parse_price(price_text),
                    price_text=price_text.strip(),
                    suburb=suburb,
                    property_type=property_type,
                    bedrooms=self._parse_bedrooms(text_content),
                    bathrooms=self._parse_bathrooms(text_content),
                    parking=None,
                    size_sqm=self._parse_size(text_content),
                    title=title[:200],
                    listing_type=listing_type,
                    scraped_at=datetime.now().isoformat()
                )
                listings.append(listing)

            except Exception as e:
                print(f"Error parsing listing: {e}")
                continue

        return listings

    async def scrape_suburb(
        self,
        suburb: str,
        city: str = "cape-town",
        province: str = "western-cape",
        listing_type: str = "rent",
        max_pages: int = 5
    ) -> list[PropertyListing]:
        """
        Scrape all listings for a suburb.

        Args:
            suburb: Suburb name (e.g., "kenilworth")
            city: City name (e.g., "cape-town")
            province: Province name (e.g., "western-cape")
            listing_type: "rent" or "sale"
            max_pages: Maximum pages to scrape

        Returns:
            List of PropertyListing objects
        """
        all_listings = []
        page = await self.context.new_page()

        try:
            for page_num in range(1, max_pages + 1):
                url = self._build_url(suburb, province, city, listing_type, page_num)
                print(f"Scraping: {url}")

                await page.goto(url, wait_until="domcontentloaded")
                listings = await self._extract_listings_from_page(page, suburb, listing_type)

                if not listings:
                    print(f"No listings found on page {page_num}, stopping.")
                    break

                all_listings.extend(listings)
                print(f"Found {len(listings)} listings on page {page_num}")

                # Check if there's a next page
                next_button = await page.query_selector('a[rel="next"], .pagination-next, [aria-label="Next"]')
                if not next_button:
                    break

                await asyncio.sleep(1)  # Be respectful

        finally:
            await page.close()

        return all_listings

    async def scrape_listing_details(self, url: str, page: Page = None) -> Optional[PropertyListing]:
        """Scrape detailed information from a single listing page."""
        should_close = False
        if page is None:
            page = await self.context.new_page()
            should_close = True

        try:
            await page.goto(url, wait_until="networkidle", timeout=30000)
            await asyncio.sleep(2)

            # Get the full page text
            text = await page.inner_text("body")
            html = await page.content()

            # Extract price - Property24 usually has price prominently
            price = None
            price_text = ""
            price_match = re.search(r'R\s*([\d\s]+)(?:\s*p/?m|\s*per\s*month)?', text)
            if price_match:
                price_text = "R " + price_match.group(1).strip()
                price = self._parse_price(price_text)

            # Extract bedrooms
            bedrooms = None
            bed_match = re.search(r'(\d+)\s*(?:Bed|bedroom)', text, re.I)
            if bed_match:
                bedrooms = int(bed_match.group(1))

            # Extract bathrooms
            bathrooms = None
            bath_match = re.search(r'(\d+)\s*(?:Bath|bathroom)', text, re.I)
            if bath_match:
                bathrooms = int(bath_match.group(1))

            # Extract parking
            parking = None
            park_match = re.search(r'(\d+)\s*(?:Parking|Garage|Car)', text, re.I)
            if park_match:
                parking = int(park_match.group(1))

            # Extract size
            size = None
            size_match = re.search(r'(\d+(?:\.\d+)?)\s*m[²2]', text)
            if size_match:
                size = float(size_match.group(1))

            # Extract property type from title or page
            property_type = "Unknown"
            for ptype in ["House", "Apartment", "Flat", "Townhouse", "Studio", "Room", "Commercial", "Duplex"]:
                if ptype.lower() in text.lower():
                    property_type = ptype
                    break

            # Get title from h1 or first significant text
            title = ""
            title_el = await page.query_selector('h1')
            if title_el:
                title = await title_el.inner_text()

            # Determine listing type from URL
            listing_type = "rent" if "/to-rent/" in url else "sale"

            # Extract suburb from URL
            suburb_match = re.search(r'/(?:to-rent|for-sale)/([^/]+)/', url)
            suburb = suburb_match.group(1) if suburb_match else "unknown"

            if price:  # Only return if we found a price
                return PropertyListing(
                    url=url,
                    price=price,
                    price_text=price_text,
                    suburb=suburb,
                    property_type=property_type,
                    bedrooms=bedrooms,
                    bathrooms=bathrooms,
                    parking=parking,
                    size_sqm=size,
                    title=title[:200],
                    listing_type=listing_type,
                    scraped_at=datetime.now().isoformat()
                )

        except Exception as e:
            print(f"Error scraping {url}: {e}")

        finally:
            if should_close:
                await page.close()

        return None

    async def scrape_suburb_detailed(
        self,
        suburb: str,
        city: str = "cape-town",
        province: str = "western-cape",
        listing_type: str = "rent",
        max_listings: int = 30
    ) -> list[PropertyListing]:
        """
        Scrape listings with full details by visiting each listing page.
        Slower but more accurate.
        """
        all_listings = []
        page = await self.context.new_page()

        try:
            # First get all listing URLs from search page
            url = self._build_url(suburb, province, city, listing_type, 1)
            print(f"Getting listing URLs from: {url}")

            await page.goto(url, wait_until="networkidle", timeout=30000)
            await asyncio.sleep(3)

            # Scroll to load all listings
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await asyncio.sleep(2)

            # Find all listing links
            listing_type_path = "to-rent" if listing_type == "rent" else "for-sale"
            links = await page.query_selector_all(f'a[href*="/{listing_type_path}/"]')

            urls = set()
            for link in links:
                href = await link.get_attribute("href")
                if href and re.search(r'/\d+/\d+$', href):
                    full_url = href if href.startswith("http") else f"{self.BASE_URL}{href}"
                    urls.add(full_url)

            print(f"Found {len(urls)} listing URLs")

            # Scrape each listing page
            urls_to_scrape = list(urls)[:max_listings]
            for i, listing_url in enumerate(urls_to_scrape, 1):
                print(f"Scraping {i}/{len(urls_to_scrape)}: {listing_url}")
                listing = await self.scrape_listing_details(listing_url, page)
                if listing:
                    all_listings.append(listing)
                await asyncio.sleep(0.5)  # Be respectful

        finally:
            await page.close()

        return all_listings


def save_listings(listings: list[PropertyListing], filename: str):
    """Save listings to JSON file."""
    output_dir = Path(__file__).parent / "data"
    output_dir.mkdir(exist_ok=True)

    filepath = output_dir / filename
    data = [asdict(listing) for listing in listings]

    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)

    print(f"Saved {len(listings)} listings to {filepath}")
    return filepath


async def main():
    """Example usage."""
    async with Property24Scraper(headless=True) as scraper:
        # Scrape rentals in Kenilworth
        rentals = await scraper.scrape_suburb(
            suburb="kenilworth",
            city="cape-town",
            province="western-cape",
            listing_type="rent",
            max_pages=3
        )
        save_listings(rentals, "kenilworth_rentals.json")

        # Scrape sales in Kenilworth
        sales = await scraper.scrape_suburb(
            suburb="kenilworth",
            city="cape-town",
            province="western-cape",
            listing_type="sale",
            max_pages=3
        )
        save_listings(sales, "kenilworth_sales.json")

        # Print summary
        print(f"\n=== Summary ===")
        print(f"Rentals: {len(rentals)}")
        if rentals:
            prices = [r.price for r in rentals if r.price]
            if prices:
                print(f"  Avg rent: R {sum(prices) / len(prices):,.0f}")
                print(f"  Min: R {min(prices):,} | Max: R {max(prices):,}")

        print(f"Sales: {len(sales)}")
        if sales:
            prices = [s.price for s in sales if s.price]
            if prices:
                print(f"  Avg price: R {sum(prices) / len(prices):,.0f}")
                print(f"  Min: R {min(prices):,} | Max: R {max(prices):,}")


if __name__ == "__main__":
    asyncio.run(main())
