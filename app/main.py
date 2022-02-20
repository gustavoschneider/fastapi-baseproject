from fastapi import FastAPI
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi_versioning import VersionedFastAPI

from .config import settings
from . import api

origins = [
    'http://localhost',
    'http://localhost:8000',
    'http://localhost:4200'
]

MIDDLEWARES = [
    Middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=['*'], allow_headers=['*']),
]

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
