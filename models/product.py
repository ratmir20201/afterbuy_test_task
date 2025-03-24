from sqlalchemy import JSON
from sqlalchemy.orm import Mapped, mapped_column

from db.db import Base


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    product_id: Mapped[str]
    name: Mapped[str]
    properties: Mapped[dict] = mapped_column(JSON)
    ean: Mapped[str]
