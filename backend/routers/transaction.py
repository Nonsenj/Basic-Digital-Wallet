from fastapi import APIRouter, HTTPException, Depends

from typing import Optional, Annotated

from sqlmodel import Field, SQLModel, create_engine, Session, select
from sqlmodel.ext.asyncio.session import AsyncSession

from .. import models

router = APIRouter(prefix="/transaction", tags=["transaction"])


@router.get("")
async def read_items(
    session: Annotated[AsyncSession, Depends(models.get_session)],
) -> models.ItemList:
    result = await session.exec(select(models.DBItem))
    items = result.all()
        
    return models.ItemList.model_validate(
        dict(items=items, page_size=0, page=0, size_per_page=0))