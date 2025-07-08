from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError
import asyncio
import re
from dataclasses import dataclass
from typing import List, Optional
import os
import time
import json

@dataclass
class TemplateData:
    title: str
    description: str
    thumbnail: str
    url: str

async def extract_template_data(card) -> Optional[TemplateData]:
    try:
        title = await card.locator("h3").inner_text()
        url_elem = await card.locator("a").first
        url = await url_elem.get_attribute("href")
        full_url = f"https://www.wix.com{url}" if url and url.startswith("/") else url or ""

        thumbnail_style = await card.locator("div[data-testid='templateItemThumbnail']").get_attribute("style")
        match = re.search(r'url\("(.*?)"\)', thumbnail_style or "")
        thumbnail = match.group(1) if match else ""

        return TemplateData(
            title=title.strip(),
            description="Template found on Wix",
            thumbnail=thumbnail,
            url=full_url
        )
    except Exception as e:
        print(f"Error extracting template data: {str(e)}")
        return None

async def scrape_templates():
    print("Launching browser...")
    start_time = time.time()

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,  # Show browser so you can inspect
            slow_mo=50,
            args=['--disable-blink-features=AutomationControlled']
        )
        page = await browser.new_page()

        try:
            url = "https://www.wix.com/website/templates/?criteria=black"
            print(f"Loading {url}")
            await page.goto(url, timeout=60000, wait_until="domcontentloaded")

            # PAUSE here to inspect the page manually
            print("Pausing script for inspection. Use DevTools to inspect the page.")
            await page.pause()

            # After inspection, script resumes here

            # Wait for template items to load
            try:
                await page.wait_for_selector("li[data-testid='templateItem']", timeout=15000)
                print("Template items loaded, proceeding...")
            except PlaywrightTimeoutError:
                print("Timeout waiting for template items - page may not have loaded correctly")
                return []

            templates: List[TemplateData] = []
            seen_urls = set()
            previous_count = 0
            max_scrolls = 20
            scrolls = 0

            while scrolls < max_scrolls:
                await page.evaluate('window.scrollBy(0, window.innerHeight)')
                await asyncio.sleep(2)

                template_cards = page.locator("li[data-testid='templateItem']")
                count = await template_cards.count()

                print(f"Detected {count} template cards")

                if count == previous_count:
                    print("No new templates loaded. Stopping scroll.")
                    break

                previous_count = count
                scrolls += 1

            print(f"Finished scrolling. Extracting templates...")

            for i in range(previous_count):
                card = template_cards.nth(i)
                data = await extract_template_data(card)
                if data and data.url not in seen_urls:
                    templates.append(data)
                    seen_urls.add(data.url)

            print(f"\n✅ Scraped {len(templates)} unique templates:")

            os.makedirs("output", exist_ok=True)
            with open("output/templates_black.json", "w", encoding="utf-8") as f:
                json.dump([t.__dict__ for t in templates], f, ensure_ascii=False, indent=4)
            print(f"Saved {len(templates)} templates to output/templates_black.json")

            return templates

        except Exception as e:
            print(f"Error during scraping: {str(e)}")
            raise
        finally:
            await browser.close()
            print(f"Browser closed (total execution time: {time.time() - start_time:.2f} seconds)")

if __name__ == "__main__":
    asyncio.run(scrape_templates())
