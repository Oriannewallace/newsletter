"""Debug script to understand Property24 page structure."""

import asyncio
from playwright.async_api import async_playwright


async def debug_page():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        url = "https://www.property24.com/to-rent/kenilworth/cape-town/western-cape/10048"
        print(f"Loading: {url}")

        await page.goto(url)
        await page.wait_for_load_state("networkidle")
        await asyncio.sleep(3)

        # Save screenshot
        await page.screenshot(path="debug_screenshot.png", full_page=True)
        print("Saved screenshot to debug_screenshot.png")

        # Get page content
        content = await page.content()
        with open("debug_page.html", "w") as f:
            f.write(content)
        print("Saved HTML to debug_page.html")

        # Try to find any listing elements
        selectors_to_try = [
            ".p24_regularTile",
            ".js_listingTile",
            "[data-testid]",
            ".listing-result",
            ".property-card",
            ".p24_results a",
            ".sc-1reuh5j-0",  # styled-components
            "article",
            ".tile",
            "div[class*='listing']",
            "div[class*='Listing']",
            "div[class*='result']",
            "div[class*='Result']",
        ]

        print("\nTrying selectors:")
        for selector in selectors_to_try:
            elements = await page.query_selector_all(selector)
            if elements:
                print(f"  {selector}: {len(elements)} elements found")
                # Get first element's HTML
                if elements:
                    first_html = await elements[0].inner_html()
                    print(f"    Sample: {first_html[:200]}...")

        # Look for any links that might be listings
        links = await page.query_selector_all("a[href*='/to-rent/']")
        print(f"\nFound {len(links)} links containing '/to-rent/'")

        await browser.close()


if __name__ == "__main__":
    asyncio.run(debug_page())
