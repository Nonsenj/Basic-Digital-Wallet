from typing import Optional
from pydantic import BaseModel, ConfigDict
from sqlmodel import Field, SQLModel, create_engine, Session, select, Relationship

from . import merchants
from . import users

class BaseItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    description: Optional[str] = None
    price: float = 0.14
    tax: float | None = None

    merchant_id: int | None
    user_id: int | None = 0

class Item(BaseItem):
    id: int
    merchant_id: int

class CreatedItem(BaseItem):
    pass

class UpdatedItem(BaseItem):
    pass


class DBItem(BaseItem, SQLModel, table=True):
    __tablename__ = "items"
    id: Optional[int] = Field(default=None, primary_key=True)

    merchant_id: int = Field(default=None, foreign_key="merchants.id")
    merchant: merchants.DBMerchant = Relationship()

    user_id: int = Field(default=None, foreign_key="users.id")
    user: users.DBUser | None = Relationship()


class ItemList(BaseModel):
    items: list[Item]
    page: int
    page_size: int
    size_per_page: int