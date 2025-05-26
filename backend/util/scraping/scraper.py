import asyncio
from .playwright_scraper import scrape_wix
from .colorlib_scraper import scrape_colorlib
from database.db import add_template

async def scrape_templates(query: str = ""):
    print("Scraping templates...")

    wix_templates = await scrape_wix()
    colorlib_templates = await scrape_colorlib(query)

    all_templates = wix_templates + colorlib_templates

    for template in all_templates:
        add_template(template.title, template.title, template.image_url, template.link)

    print(f"✅ Added {len(all_templates)} templates to the database.")

# For manual testing
if __name__ == "__main__":
    asyncio.run(scrape_templates())
