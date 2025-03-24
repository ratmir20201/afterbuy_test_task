import asyncio

from auth import authentication
from db.db import create_tables
from ebay_lister.product_detail import save_product_detail


async def run_main():
    await authentication()
    await save_product_detail()


if __name__ == "__main__":
    asyncio.run(create_tables())
    asyncio.run(run_main())
