from typing import Optional
from pydantic import BaseModel, ConfigDict
from sqlmodel import Field, SQLModel, create_engine, Session, select

class BaseItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    description: Optional[str] = None
    price: float = 0.14
    tax: float | None = None

class Item(BaseItem):
    id: int

class CreatedItem(BaseItem):
    pass

class UpdatedItem(BaseItem):
    pass


class DBItem(Item, SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class ItemList(BaseModel):
    items: list[Item]
    page: int
    page_size: int
    size_per_page: int