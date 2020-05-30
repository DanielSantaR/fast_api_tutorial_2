from fastapi import APIRouter
from app.endpoints import pets, owners
from app.security import security

api_router = APIRouter()
api_router.include_router(pets.router, prefix='/pets', tags=['pets'])
api_router.include_router(owners.router, prefix='/owners', tags=['owners'])
