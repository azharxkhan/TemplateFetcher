from playwright.async_api import async_playwright
from backend.database import add_template
import re
import os
from typing import List, Dict
from dataclasses import dataclass
import asyncio
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

WIX_SEARCH_URL = "https://www.wix.com/website/templates/html/all/1?criteria=black"

@dataclass
class TemplateData:
    title: str
    description: str
    thumbnail: str
    url: str

async def extract_template_data(card) -> TemplateData:
    """Extract template information from a card element."""
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
            description="Dark-themed template with 'black' in search results",
            thumbnail=thumbnail,
            url=full_url
        )
    except Exception as e:
        logging.error(f"Error extracting template data: {str(e)}")
        return None

async def scrape_wix():
    """Scrape Wix templates using Playwright."""
    logging.info("Launching browser...")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            slow_mo=100,
            args=['--disable-blink-features=AutomationControlled']
        )
        page = await browser.new_page()
        
        try:
            await page.goto(WIX_SEARCH_URL, timeout=60000, wait_until="domcontentloaded")
            await page.wait_for_timeout(3000)
            
            templates: List[TemplateData] = []
            scrolls = 0
            max_scrolls = 10
            
            while len(templates) < 100 and scrolls < max_scrolls:
                logging.info(f"Scroll attempt {scrolls + 1}/{max_scrolls}")
                
                # Smooth scroll using JavaScript
                await page.evaluate('''
                    window.scrollBy({
                        top: window.innerHeight,
                        behavior: 'smooth'
                    });
                ''')
                
                # Wait for dynamic content loading
                await asyncio.sleep(2)
                
                # Debug screenshots
                os.makedirs("debug", exist_ok=True)
                await page.screenshot(path=f"debug/screenshot_scroll_{scrolls}.png", full_page=True)
                
                template_cards = page.locator("li[data-testid='templateItem']")
                count = await template_cards.count()
                
                # Extract new templates
                for i in range(min(100, count)):
                    card = template_cards.nth(i)
                    template_data = await extract_template_data(card)
                    if template_data:
                        templates.append(template_data)
                
                logging.info(f"Found {len(templates)} templates after scroll {scrolls + 1}")
                
                # Break if no new templates found
                if len(templates) >= 100:
                    break
                    
                scrolls += 1
            
            # Save to database
            logging.info("Saving templates to database...")
            for template in templates[:100]:  # Limit to 100 templates
                await add_template(template.title, template.description, template.thumbnail, template.url)
            
            logging.info(f"Successfully scraped {len(templates)} templates")
            return templates[:100]
            
        except Exception as e:
            logging.error(f"Error during scraping: {str(e)}")
            raise
        finally:
            await browser.close()
            logging.info("Browser closed")