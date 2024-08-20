from fastapi import APIRouter, HTTPException, Depends

from typing import Optional, Annotated

from sqlmodel import Field, SQLModel, create_engine, Session, select
from sqlmodel.ext.asyncio.session import AsyncSession

from .. import models
from .. import deps

router = APIRouter(prefix="/transaction", tags=["transaction"])


@router.post("")
async def create_transaction(
    transaction: models.CreateTransaction,
    current_user: Annotated[models.User,Depends(deps.get_current_user)],
    session:  Annotated[AsyncSession, Depends(models.get_session)],                      
) -> models.Transaction:
    dbtransaction = models.DBTransaction.model_validate(transaction)
    dbtransaction.user = current_user

    session.add(dbtransaction)
    await session.commit()
    await session.refresh(dbtransaction)

    return models.Transaction.model_validate(dbtransaction)


@router.get("")
async def read_transactions(
    session:  Annotated[AsyncSession, Depends(models.get_session)],    
) -> models.TransactionList:
    transactions = await session.exec(select(models.DBTransaction)).all()

    return models.TransactionList.model_validate(
        dict(transactions=transactions, page_size=0, page=0, size_per_page=0)
    )


@router.get("/{transaction_id}")
async def read_transaction(transaction_id: int,
    session:  Annotated[AsyncSession, Depends(models.get_session)],                            
) -> models.Transaction:
    db_transaction = await session.get(models.Transaction, transaction_id)
    if db_transaction:
        return models.Transaction.model_validate(db_transaction)
    raise HTTPException(status_code=404, detail="Transaction not found")


@router.put("/{transaction_id}")
async def update_merchant(
    transaction_id: int, 
    transaction: models.UpdateTransaction,
    session:  Annotated[AsyncSession, Depends(models.get_session)],
    current_user: Annotated[models.User,Depends(deps.get_current_user)],    
) -> models.Transaction:
    data = transaction.model_dump()
    db_transaction = await session.get(models.DBTransaction, transaction_id)
    db_transaction.sqlmodel_update(data)

    session.add(db_transaction)
    await session.commit()
    await session.refresh(db_transaction)

    return models.Transaction.model_validate(db_transaction)

@router.delete("/{transaction_id}")
async def delete_transaction(transaction_id: int,
    session:  Annotated[AsyncSession, Depends(models.get_session)],
    current_user: Annotated[models.User,Depends(deps.get_current_user)],                             
) -> dict:
    db_transaction = await session.get(models.DBTransaction, transaction_id)
    
    await session.delete(db_transaction)
    await session.commit()

    return dict(message="delete success")