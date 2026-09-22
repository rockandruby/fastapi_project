from fastapi import APIRouter
from app.api.routes.v1.users import router as users_router
from app.api.routes.v1.orders import router as orders_router
from app.api.routes.login import router as login_router
from app.api.routes.custom import router as custom_router
from app.settings import API_V1_PREFIX

api_router = APIRouter()
api_router.include_router(users_router, prefix=API_V1_PREFIX)
api_router.include_router(orders_router, prefix=API_V1_PREFIX)
api_router.include_router(login_router)
api_router.include_router(custom_router)
