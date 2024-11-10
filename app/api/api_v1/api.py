from fastapi import APIRouter
from api.api_v1.endpoints import auth

main_router = APIRouter()

# front end routers
router = APIRouter()
router.include_router(auth)

main_router.include_router(router)