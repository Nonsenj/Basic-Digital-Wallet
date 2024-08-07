from fastapi import APIRouter, HTTPException, Depends

from typing import Optional, Annotated

from sqlmodel import Field, SQLModel, Session, select
from sqlmodel.ext.asyncio.session import AsyncSession

from .. import models

router = APIRouter(prefix="/items")

@router.get("")
async def read_items(
    session: Annotated[AsyncSession, Depends(models.get_session)],
) -> models.ItemList:
    result = await session.exec(select(models.DBItem))
    items = result.all()
        
    return models.ItemList.model_validate(
        dict(items=items, page_size=0, page=0, size_per_page=0))

@router.post("")
async def create(item: models.CreatedItem,
    session: Annotated[AsyncSession, Depends(models.get_session)],
) -> models.Item:
    data = item.model_dump()
    dbitem = models.DBItem(**data)
    session.add(dbitem)
    await session.commit()
    await session.refresh(dbitem)

    return models.Item.model_validate(dbitem)

@router.get("/{item_id}")
async def read_item(item_id: int,
    session: Annotated[AsyncSession, Depends(models.get_session)],
) -> models.Item:
    db_item = await session.get(models.DBItem, item_id)
    if db_item:
        return models.Item.model_validate(db_item)

    raise HTTPException(status_code=404, detail="Item not found")


@router.put("/{item_id}")
async def update_item(
    item_id: int, 
    item: models.UpdatedItem,
    session: Annotated[AsyncSession, Depends(models.get_session)],
) -> models.Item:
    print("update_item", item)
    data = item.model_dump()
    db_item = await session.get(models.DBItem, item_id)
    db_item.sqlmodel_update(data)
    session.add(db_item)
    await session.commit()
    await session.refresh(db_item)

    # return Item.parse_obj(dbitem.model_dump())
    return models.Item.model_validate(db_item)


@router.delete("/{item_id}")
async def delete_item(item_id: int,
    session: Annotated[AsyncSession, Depends(models.get_session)],
) -> dict:
    db_item = await session.get(models.DBItem, item_id)
    await session.delete(db_item)
    await session.commit()

    return dict(message="delete success")