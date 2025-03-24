import pickle
import os

from playwright.async_api import async_playwright

from config import settings


async def save_cookies(page, cookie_file="cookies.pkl"):
    cookies = await page.context.cookies()
    with open(cookie_file, "wb") as f:
        pickle.dump(cookies, f)


async def load_cookies(page, cookie_file="cookies.pkl"):
    if os.path.exists(cookie_file):
        with open(cookie_file, "rb") as f:
            cookies = pickle.load(f)
            await page.context.add_cookies(cookies)


async def authentication():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()

        page = await context.new_page()

        await load_cookies(page)

        if not os.path.exists("cookies.pkl"):
            await page.goto("https://login.afterbuy.de/Account/Login", timeout=0)
            await page.fill('input[name="Username"]', settings.api_auth.username)
            await page.fill('input[name="Password"]', settings.api_auth.password)

            locator = await page.wait_for_selector(
                'xpath=//*[@id="CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"]',
                timeout=20000,
            )
            await locator.click()

            print("Cookie confirmation button clicked!")
            await page.click('button[name="B1"]')

            await page.wait_for_load_state("load")
            print(f"Logged in: {page.url}")

            await save_cookies(page)
        else:
            print("Cookies loaded, already logged in!")

        await browser.close()
