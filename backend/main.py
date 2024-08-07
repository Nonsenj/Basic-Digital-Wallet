from fastapi import FastAPI
from . import config
from . import routers
from . import models

def create_app():
    setting = config.get_setting()
    app = FastAPI()

    models.init_db(setting)

    routers.init_router(app)

    @app.on_event("startup")
    async def on_startup():
        await models.create_all()

    return app




