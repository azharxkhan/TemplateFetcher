from playwright.async_api import async_playwright
from backend.models.template import Template

async def scrape_wix():
    templates = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto("https://www.wix.com/templates")
        await page.wait_for_selector(".template-card")

        cards = await page.query_selector_all(".template-card")

        for card in cards:
            title_el = await card.query_selector(".template-title")
            img_el = await card.query_selector("img")
            link_el = await card.query_selector("a")

            title = await title_el.inner_text() if title_el else "Untitled"
            image_url = await img_el.get_attribute("src") if img_el else ""
            link = await link_el.get_attribute("href") if link_el else "#"

            templates.append(Template(
                title=title.strip(),
                image_url=image_url,
                link=f"https://www.wix.com{link}" if link.startswith("/") else link,
                source="Wix"
            ))

        await browser.close()

    return templates
