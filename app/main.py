from fastapi import FastAPI
from fastapi_versioning import VersionedFastAPI
from .config import settings
from . import api

MIDDLEWARES = []

app = FastAPI(
    title = f'{settings.app_name} version {settings.app_version}',
    middleware=MIDDLEWARES
)
app.include_router(api.api_router)
app = VersionedFastAPI(
    app,
    prefix='/v{major}',
    enable_latest=True,
    middleware=MIDDLEWARES
)
