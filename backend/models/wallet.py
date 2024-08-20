from typing import Optional
from pydantic import BaseModel, ConfigDict
from sqlmodel import Field, SQLModel, create_engine, Session, select, Relationship

from . import users

class BaseWallet(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    owner: str
    balance: float = 0.00 
    currency: str | None
    user_id: int | None = 0


class Wallet(BaseWallet):
    id: int

class CreateWallet(BaseWallet):
    pass

class UpdateWallet(BaseWallet):
    pass

class DBWallet(BaseWallet, SQLModel, table=True):
    __tablename__ = "wallet"
    id: Optional[int] = Field(default=None, primary_key=True)

    user_id: int = Field(default=None, foreign_key="users.id")
    user: users.DBUser | None = Relationship()

class WalletList(BaseModel):
    wallets: list[Wallet]
    page: int
    page_size: int
    size_per_page: int

