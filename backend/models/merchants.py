from typing import Optional
from pydantic import BaseModel, ConfigDict
from sqlmodel import Field, SQLModel, create_engine, Session, select, Relationship

from . import items
from . import users

class BaseMerchant(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    description: str | None = None
    tax_id: str | None = None
    user_id: int | None 

class Merchant(BaseMerchant):
    id: int
    user_id: int

class CreatedMerchant(BaseMerchant):
    pass


class UpdatedMerchant(BaseMerchant):
    pass

class DBMerchant(BaseMerchant, SQLModel, table=True):
    __tablename__ = "merchants"
    id: Optional[int] = Field(default=None, primary_key=True)
    
    user_id: int =  Field(default=None, foreign_key="users.id")
    user: users.DBUser | None = Relationship()

class MerchantList(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    items: list[Merchant]
    page: int
    page_size: int
    size_per_page: int