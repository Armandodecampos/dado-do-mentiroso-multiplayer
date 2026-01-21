import asyncio
from playwright.async_api import async_playwright
import os
import time

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        # Construct the file path with a cache-busting query parameter
        file_path = f"file://{os.path.abspath('index.htm')}?v={int(time.time())}"

        await page.goto(file_path, wait_until='networkidle')
        await page.wait_for_timeout(2000) # Wait for any JS to execute

        # Ensure the output directory exists
        os.makedirs("/home/jules/verification", exist_ok=True)

        await page.screenshot(path="/home/jules/verification/cache_bust_attempt.png", full_page=True)
        await browser.close()

asyncio.run(main())
