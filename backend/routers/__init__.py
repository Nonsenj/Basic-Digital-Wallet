from fastapi import FastAPI,APIRouter
from . import items
from . import merchants
from . import users
from . import authentication
from . import transaction
from . import wallet

def init_router(app: FastAPI):
    app.include_router(router)
    app.include_router(items.router)
    app.include_router(merchants.router)
    app.include_router(users.router)
    app.include_router(authentication.router)
    app.include_router(transaction.router)
    app.include_router(wallet.router)

router = APIRouter()

@router.get("/")
async def root():
    return {"message": "Hello World"}
