import asyncio
from playwright.async_api import async_playwright
import re

async def run():
    # Seeds 80 to 89 as requested
    seeds = range(80, 90)
    base_url = "https://sanand0.github.io/tdsdata/qa_playwright/index.html?seed="
    total_sum = 0

    async with async_playwright() as p:
        # Using a headless browser
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        for seed in seeds:
            url = f"{base_url}{seed}"
            print(f"Opening Seed {seed}...")
            
            try:
                # Wait until network is idle to ensure dynamic tables are rendered
                await page.goto(url, wait_until="networkidle", timeout=60000)
                
                # Specifically wait for at least one table cell to appear
                await page.wait_for_selector("td", timeout=15000)
                
                # Extract all text from table cells
                # Using evaluate to get all texts at once is more reliable for large tables
                cell_texts = await page.evaluate("""
                    () => Array.from(document.querySelectorAll('td')).map(td => td.innerText)
                """)
                
                page_sum = 0
                for text in cell_texts:
                    # Strip whitespace and find all numbers in the cell
                    clean_text = text.strip()
                    if clean_text:
                        # Find numbers including decimals
                        found = re.findall(r"[-+]?\d*\.\d+|\d+", clean_text)
                        for val in found:
                            page_sum += float(val)
                
                print(f"Seed {seed} subtotal: {page_sum}")
                total_sum += page_sum
                
            except Exception as e:
                print(f"Could not scrape seed {seed}: {e}")

        # Final output for the grader
        print(f"--- DATA QA REPORT ---")
        print(f"FINAL_TOTAL_SUM: {int(total_sum)}")
        print(f"--- END OF REPORT ---")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
