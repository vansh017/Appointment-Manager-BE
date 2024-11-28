from fastapi import APIRouter
from api.api_v1.endpoints import auth, user, shop

main_router = APIRouter()

# front end routers
router = APIRouter()
router.include_router(auth)
router.include_router(user)
router.include_router(shop)

main_router.include_router(router)