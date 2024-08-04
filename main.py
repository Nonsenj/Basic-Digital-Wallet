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

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/item/{item_id}")
async def read_time(item_id: int):
    return {"Item_id": item_id}

@app.put("/items/{item_id}")
async def create_item(item_id: int, item: BaseItem):
    return {"item_id": item_id, **item.model_dump()}