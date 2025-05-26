from bs4 import BeautifulSoup
from backend.models.template import Template
import aiohttp

async def scrape_colorlib(query: str = ""):
    url = "https://colorlib.com/wp/templates/"
    headers = {"User-Agent": "Mozilla/5.0"}

    templates = []

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as resp:
                html = await resp.text()
                soup = BeautifulSoup(html, "html.parser")

                for article in soup.select("article"):
                    title_el = article.select_one("h3")
                    img_el = article.select_one("img")
                    link_el = article.select_one("a")

                    if title_el and img_el and link_el:
                        templates.append(Template(
                            title=title_el.text.strip(),
                            image_url=img_el.get("src"),
                            link=link_el.get("href"),
                            source="Colorlib"
                        ))

    except Exception as e:
        print(f"Error scraping Colorlib: {e}")

    return templates
