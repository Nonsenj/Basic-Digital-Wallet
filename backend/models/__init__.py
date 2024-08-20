from typing import Optional
from ..config import Settings

from sqlmodel import Field, SQLModel, create_engine, Session, select
from sqlmodel.ext.asyncio.session import AsyncSession

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

from . import items
from . import merchants
from . import users
from . import transaction
from . import wallet

from .items import *
from .merchants import *
from .users import *
from .transaction import *
from .wallet import *

connect_args = {}

engine = None

def init_db(settings: Settings):
    global engine

    engine = create_async_engine(
        settings.SQLDB_URL,
        echo=True,
        future=True,
        connect_args= connect_args,
    )

async def create_all():
    async with engine.begin() as conn:
        #await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session() -> AsyncSession:
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session