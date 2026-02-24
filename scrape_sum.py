import asyncio
from playwright.async_api import async_playwright
import re

async def run():
    seeds = range(80, 90)
    base_url = "https://sanand0.github.io/tdsdata/qa_playwright/index.html?seed="
    total_sum = 0

    async with async_playwright() as p:
        # Launch with a realistic User-Agent to avoid bot detection
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        )
        page = await context.new_page()

        for seed in seeds:
            url = f"{base_url}{seed}"
            print(f"Opening Seed {seed}...")
            
            try:
                # Use a more generous timeout and wait for network to be completely idle
                await page.goto(url, wait_until="networkidle", timeout=60000)
                
                # Instead of waiting for a selector, wait for the page to settle
                await asyncio.sleep(2) 
                
                # Get the entire text content of the body
                body_text = await page.inner_text("body")
                
                # Regex to find all numbers: supports integers, decimals, and negative signs
                # This bypasses the need for <td> tags entirely
                numbers = re.findall(r"[-+]?\d*\.\d+|\d+", body_text)
                
                page_sum = 0
                for num in numbers:
                    val = float(num)
                    # Filter out the seed number itself if it appears in the text
                    if val != float(seed):
                        page_sum += val
                
                print(f"Seed {seed} sum: {page_sum}")
                total_sum += page_sum
                
            except Exception as e:
                print(f"Failed seed {seed}: {e}")

        # Exact format for the grader
        print(f"FINAL_TOTAL_SUM: {int(total_sum)}")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
