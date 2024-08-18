from fastapi import FastAPI,APIRouter
from . import items
from . import merchants
from . import users
from . import authentication

def init_router(app: FastAPI):
    app.include_router(router)
    app.include_router(items.router)
    app.include_router(merchants.router)
    app.include_router(users.router)
    app.include_router(authentication.router)

router = APIRouter()

@router.get("/")
async def root():
    return {"message": "Hello World"}
