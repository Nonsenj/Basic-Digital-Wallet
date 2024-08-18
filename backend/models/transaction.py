import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict
from sqlmodel import Field, SQLModel, create_engine, Session, select, Relationship

from . import users
from . import merchants

class BaseTransaction(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    item: str
    amount: float | None
    time_stemp: datetime.datetime | None
    merchant_id: int | None
    user_id: int | None
    

class Transaction(BaseTransaction):
    id: int
    
class DBItem(BaseTransaction, SQLModel, table=True):
    __tablename__ = "Transaction"
    id: Optional[int] = Field(default=None, primary_key=True)

    merchant_id: int = Field(default=None, foreign_key="merchants.id")
    merchant: merchants.DBMerchant = Relationship()

    user_id: int = Field(default=None, foreign_key="users.id")
    user: users.DBUser | None = Relationship()


class TransactionList(BaseModel):
    transaction: list[Transaction]
    page: int
    page_size: int
    size_per_page: int
