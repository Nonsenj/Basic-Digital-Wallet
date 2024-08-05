from fastapi import FastAPI
from .routers import router
from .models import init_db

def create_app():
    app = FastAPI()

    init_db()

    app.include_router(router)

    return app



