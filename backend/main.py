# ssl patch
from gevent import monkey

monkey.patch_all()

from fastapi import FastAPI
from contextlib import asynccontextmanager

from . import config
from . import models

from . import routers


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    if models.engine is not None:
        # Close the DB connection
        await models.close_session()


def create_app(settings=None):
    if not settings:
        settings = config.get_setting()

    app = FastAPI(lifespan=lifespan)

    models.init_db(settings)

    routers.init_router(app)
    return app
