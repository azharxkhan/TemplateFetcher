import aiohttp
import asyncio
from bs4 import BeautifulSoup
from database import add_template

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

TEMPLATE_SITES = [
    "https://www.wix.com/templates",
    "https://colorlib.com/wp/templates/"
]

async def fetch_template(session, url):
    try:
        async with session.get(url, headers=HEADERS) as response:
            html = await response.text()
            return html
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

async def scrape_templates(query: str):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_template(session, url) for url in TEMPLATE_SITES]
        responses = await asyncio.gather(*tasks)

        for html in responses:
            if html:
                soup = BeautifulSoup(html, "html.parser")
                templates = parse_templates(soup)
                for title, description, thumbnail, link in templates:
                    add_template(title, description, thumbnail, link)

def parse_templates(soup):
    templates = []

    # Wix example
    for template in soup.select(".template-card"):  # Update this based on actual site HTML
        title = template.select_one(".template-title").text.strip()
        description = template.select_one(".template-description").text.strip()
        thumbnail = template.select_one("img").get("src")
        link = template.get("href")
        templates.append((title, description, thumbnail, link))
    
    return templates