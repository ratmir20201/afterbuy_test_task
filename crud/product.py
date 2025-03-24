from sqlalchemy import select

from db.db import get_async_context_session
from models.product import Product


async def create_product(product_data: dict):
    async with get_async_context_session() as session:
        product = Product(**product_data)
        session.add(product)
        await session.commit()
