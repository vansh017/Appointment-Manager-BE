from fastapi import APIRouter
from api.api_v1.endpoints import auth, user

main_router = APIRouter()

# front end routers
router = APIRouter()
router.include_router(auth)
router.include_router(user)

main_router.include_router(router)