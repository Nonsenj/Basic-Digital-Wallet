from typing import Optional
from pydantic import BaseModel, ConfigDict
from sqlmodel import Field, SQLModel, create_engine, Session, select, Relationship

from . import users

class BaseWallet(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    owner: str
    balance: float = 0.00 
    currency: str | None
    user_id: int | None

class Wallet(BaseWallet):
    id: int

class WalletList(BaseModel):
    wallet: list[Wallet]
    page: int
    page_size: int
    size_per_page: int

class DBItem(BaseWallet, SQLModel, table=True):
    __tablename__ = "Transaction"
    id: Optional[int] = Field(default=None, primary_key=True)


    user_id: int = Field(default=None, foreign_key="users.id")
    user: users.DBUser | None = Relationship()
