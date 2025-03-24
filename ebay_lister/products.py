from playwright.async_api import async_playwright

from auth import load_cookies
from utils.pages import calculate_pages


async def get_all_goods() -> list[dict[str, str]]:
    """Отдает все продукты поставщика Aliden."""

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()

        page = await context.new_page()

        await load_cookies(page)

        await page.goto(
            "https://farm01.afterbuy.de/afterbuy/ebayliste2.aspx?newsearch=1&DT=1",
            timeout=0,
        )
        await page.select_option(
            'select[name="lAWKollektion"]',
            value="501972",
        )

        await page.click(
            "input#ctl00_innerContentPlaceHolder_AllBox_ebaylister_btn_Suchen"
        )

        text_with_goods = await page.text_content("#totalItemsCount")
        total_goods = text_with_goods.split()[1]
        print(total_goods)

        await page.fill('input[name="maxgesamt"]', total_goods)
        await page.click(
            "input#ctl00_innerContentPlaceHolder_AllBox_ebaylister_btn_Suchen"
        )

        try:
            await page.wait_for_selector("#totalItemsCount", timeout=60000)
            print("Товары загружены, начинаю извлечение данных")
        except Exception as e:
            print("Ошибка при ожидании загрузки товаров:", e)
            await browser.close()
            return

        goods = []
        current_page = 1
        next_rsposition = 10

        for _ in range(calculate_pages(int(total_goods))):
            await page.wait_for_selector("tr", state="attached", timeout=60000)

            rows = await page.query_selector_all("tr")

            if rows:
                for row in rows:
                    edit_links = await row.query_selector_all('a[href*="art=edit"]')
                    unwanted_links = await row.query_selector_all(
                        'a[href*="art=editstart"]'
                    )

                    if unwanted_links:
                        continue

                    if edit_links:
                        for edit_link in edit_links:
                            link = await edit_link.get_attribute("href")
                            good = {"Good_url": link}
                            if good not in goods:
                                goods.append(good)
            else:
                print("Товары не найдены, проверьте селектор.")

            next_page_link = await page.query_selector(
                f'a[href*="jump=2&rsposition={next_rsposition}"]'
            )

            if next_page_link:
                print(f"Переход на страницу {current_page + 1}")
                await next_page_link.click()

                await page.wait_for_load_state("load")
                current_page += 1
                next_rsposition += 10
            else:
                print("Следующей страницы нет, завершение.")
                break

        filtered_goods = [
            good for good in goods if "ebayliste2.aspx" in good["Good_url"]
        ]

        print(filtered_goods)
        print(len(filtered_goods))

        await browser.close()

        return filtered_goods
