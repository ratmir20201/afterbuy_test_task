from playwright.async_api import async_playwright

from auth import load_cookies


async def enter_ebay_lister():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()

        page = await context.new_page()

        await load_cookies(page)

        await page.goto(
            "https://farm01.afterbuy.de/afterbuy/ebayliste2.aspx?newsearch=1&DT=1",
            timeout=0,
        )

        print(page.url)

        await browser.close()
