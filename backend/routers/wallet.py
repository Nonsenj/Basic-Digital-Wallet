from fastapi import APIRouter, HTTPException, Depends

from typing import Optional, Annotated

from sqlmodel import Field, SQLModel, create_engine, Session, select
from sqlmodel.ext.asyncio.session import AsyncSession

from .. import models
from .. import deps

router = APIRouter(prefix="/wallet", tags=["wallet"])

@router.get("")
async def read_wallets(
    current_user: Annotated[models.User,Depends(deps.get_current_user)],
    session: Annotated[AsyncSession, Depends(models.get_session)],
) -> models.WalletList:
    result = await session.exec(
        select(models.DBWallet).where(models.DBWallet.user == current_user))
    
    wallets = result.all()
        
    return models.WalletList.model_validate(
        dict(wallets=wallets, page_size=0, page=0, size_per_page=0))


@router.post("")
async def create_wallet(
    wallet: models.CreateWallet,
    current_user: Annotated[models.User,Depends(deps.get_current_user)],
    session:  Annotated[AsyncSession, Depends(models.get_session)],                      
) -> models.Wallet:
    dbwallet = models.DBWallet.model_validate(wallet)
    dbwallet.user = current_user

    session.add(dbwallet)
    await session.commit()
    await session.refresh(dbwallet)

    return models.Wallet.model_validate(dbwallet)

@router.get("/{wallet_id}")
async def Get_Wallet(wallet_id: int,
    session:  Annotated[AsyncSession, Depends(models.get_session)],
    current_user: Annotated[models.User,Depends(deps.get_current_user)],                             
) -> models.Wallet:
    result = await session.exec(
        select(models.DBWallet).
        where(models.DBWallet.user == current_user, 
              models.DBWallet.id == wallet_id,)
    )

    db_wallet = result.one_or_none()

    if db_wallet :
        return models.Wallet.model_validate(db_wallet)
    raise HTTPException(status_code=404, detail="wallet not found")


@router.put("/{wallet_id}")
async def update_wallet(
    wallet_id: int, 
    wallet: models.UpdateWallet,
    session:  Annotated[AsyncSession, Depends(models.get_session)],
    current_user: Annotated[models.User,Depends(deps.get_current_user)],    
) -> models.Wallet:
    
    wallet.user_id = current_user.id
    data = wallet.model_dump()
    result = await session.exec(
        select(models.DBWallet).
        where(models.DBWallet.user == current_user, 
              models.DBWallet.id == wallet_id,)
    )

    db_wallet = result.one_or_none()
    db_wallet.sqlmodel_update(data)

    session.add(db_wallet)
    await session.commit()
    await session.refresh(db_wallet)

    return models.Wallet.model_validate(db_wallet)

@router.delete("/{wallet_id}")
async def delete_wallet(wallet_id: int,
    session:  Annotated[AsyncSession, Depends(models.get_session)],
    current_user: Annotated[models.User,Depends(deps.get_current_user)],                             
) -> dict:
    db_wallet = await session.get(models.DBWallet, wallet_id)
    
    await session.delete(db_wallet)
    await session.commit()

    return dict(message="delete success")