from fastapi import FastAPI
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

SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/items")
async def create(item: CreatedItem) -> Item:
    data = item.model_dump()
    dbitem = DBItem(**data)
    with Session(engine) as sesssion:
        sesssion.add(dbitem)
        sesssion.commit()
        sesssion.refresh(dbitem)

    return Item.model_validate(dbitem)



# @app.get("/item/{item_id}")
# async def read_time(item_id: int):
#     return {"Item_id": item_id}

# @app.put("/items/{item_id}")
# async def create_item(item_id: int, item: BaseItem):
#     return {"item_id": item_id, **item.model_dump()}