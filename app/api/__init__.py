from fastapi import APIRouter
from . import products

api_router = APIRouter()
api_router.include_router(products.router)
