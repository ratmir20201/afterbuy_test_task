from urllib.parse import urlparse

from playwright.async_api import async_playwright

from auth import load_cookies
from crud.product import create_product
from ebay_lister.products import get_all_goods


async def save_product_detail():
    """Собирает все детали продукта и сохраняет его в бд."""

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()

        page = await context.new_page()

        await load_cookies(page)

        products = await get_all_goods()
        for i_product in products:
            product_url = i_product.get("Good_url", "")

            parsed_url = urlparse(product_url)
            if not parsed_url.scheme:
                product_url = "https://farm01.afterbuy.de" + product_url
            await page.goto(product_url)

            product_id = await page.input_value('input[name="I_Stammartikel"]')
            product_name_input = await page.query_selector("input#Artikelbeschreibung")
            product_name = await product_name_input.get_attribute("value")

            product_specifics = await page.query_selector_all(
                "tr.showHideClass_CustomItemSpecifics"
            )
            product_properties = {}
            for row in product_specifics:
                name_element = await row.query_selector(
                    'input[name^="cis_ItemSpecificName"]'
                )
                if name_element:
                    name = await name_element.get_attribute("value")

                    values = []
                    value_elements = await row.query_selector_all(
                        'input[name^="cis_ItemSpecificValue"]'
                    )
                    for value_element in value_elements:
                        value = await value_element.get_attribute("value")
                        if value:
                            values.append(value)

                    if values:
                        product_properties[name] = values

            product_details = await page.query_selector("a.ab-anchor")
            related_link = await product_details.get_attribute("href")
            second_product_url = "https://farm01.afterbuy.de" + related_link
            await page.goto(second_product_url)

            await page.wait_for_load_state("load")
            await page.wait_for_selector(
                'input[formcontrolname="ManufacturerPartNumber"]',
                timeout=60000,
            )

            product_ean = await page.input_value(
                'input[formcontrolname="ManufacturerPartNumber"]'
            )

            product_data = {
                "product_id": product_id,
                "name": product_name,
                "properties": product_properties,
                "ean": product_ean,
            }

            print(product_data)
            response = await create_product(product_data=product_data)
            print("Продукт успешно добавлен!")

        await browser.close()
