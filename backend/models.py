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


connect_args = {}

engine = create_engine(
    "postgresql+pg8000://postgres:28272754@localhost/digimondb",
    echo=True,
    connect_args=connect_args,
)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session