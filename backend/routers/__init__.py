from fastapi import FastAPI,APIRouter
from . import items
from . import merchants

def init_router(app: FastAPI):
    app.include_router(router)
    app.include_router(items.router)
    app.include_router(merchants.router)

router = APIRouter()

@router.get("/")
async def root():
    return {"message": "Hello World"}
