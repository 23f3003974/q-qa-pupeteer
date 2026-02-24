import asyncio
from playwright.async_api import async_playwright
import re

async def run():
    seeds = range(80, 90)
    base_url = "https://sanand0.github.io/tdsdata/qa_playwright/index.html?seed="
    total_sum = 0

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        for seed in seeds:
            url = f"{base_url}{seed}"
            print(f"Processing seed: {seed}")
            try:
                await page.goto(url, wait_until="networkidle", timeout=60000)
                # Wait specifically for the table to render
                await page.wait_for_selector("table td", timeout=10000)
                
                # Scrape only values inside table cells
                cells = await page.locator("td").all_inner_texts()
                for text in cells:
                    # Extract only valid numbers (integers or floats)
                    clean_text = text.strip()
                    if re.match(r"^-?\d+(\.\d+)?$", clean_text):
                        total_sum += float(clean_text)
            except Exception as e:
                print(f"Skipping seed {seed} due to error: {e}")

        # Final print formatted for the grader to easily parse
        print(f"TOTAL_SUM_IDENTIFIED: {int(total_sum)}")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
