from fastapi import APIRouter, HTTPException

from typing import Optional

from sqlmodel import Field, SQLModel, create_engine, Session, select

from ..models import Item, CreatedItem, UpdatedItem, ItemList, DBItem, engine


router = APIRouter(prefix="/items")

@router.get("")
async def read_items() -> ItemList:
    with Session(engine) as session:
        items = session.exec(select(DBItem)).all()
        
    return ItemList.model_validate(dict(items=items, page_size=0, page=0, size_per_page=0))

@router.post("")
async def create(item: CreatedItem) -> Item:
    data = item.model_dump()
    dbitem = DBItem(**data)
    with Session(engine) as sesssion:
        sesssion.add(dbitem)
        sesssion.commit()
        sesssion.refresh(dbitem)

    return Item.model_validate(dbitem)

@router.get("/{item_id}")
async def read_item(item_id: int) -> Item:
    with Session(engine) as session:
        db_item = session.get(DBItem, item_id)
        if db_item:
            return Item.model_validate(db_item)
    raise HTTPException(status_code=404, detail="Item not found")


@router.put("/{item_id}")
async def update_item(item_id: int, item: UpdatedItem) -> Item:
    print("update_item", item)
    data = item.model_dump()
    with Session(engine) as session:
        db_item = session.get(DBItem, item_id)
        db_item.sqlmodel_update(data)
        session.add(db_item)
        session.commit()
        session.refresh(db_item)

    # return Item.parse_obj(dbitem.model_dump())
    return Item.model_validate(db_item)


@router.delete("/{item_id}")
async def delete_item(item_id: int) -> dict:
    with Session(engine) as session:
        db_item = session.get(DBItem, item_id)
        session.delete(db_item)
        session.commit()

    return dict(message="delete success")