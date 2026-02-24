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
            await page.goto(url)
            # Wait for dynamic table to load
            await page.wait_for_selector("table")
            
            # Extract all text from table cells
            cells = await page.query_selector_all("td")
            for cell in cells:
                text = await cell.inner_text()
                # Find all numbers (including decimals)
                numbers = re.findall(r"[-+]?\d*\.\d+|\d+", text)
                for num in numbers:
                    total_sum += float(num)

        print(f"FINAL_TOTAL_SUM: {int(total_sum)}")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
