from fastapi import FastAPI,APIRouter
from . import items

def init_router(app: FastAPI):
    app.include_router(router)
    app.include_router(items.router)

router = APIRouter()

@router.get("/")
async def root():
    return {"message": "Hello World"}
