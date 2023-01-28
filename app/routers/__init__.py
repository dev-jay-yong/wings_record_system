from fastapi import APIRouter, Depends
from fastapi.security import APIKeyHeader

from .user import router as user_router
from .team import router as team_router

API_KEY_HEADER = APIKeyHeader(name="Authorization", auto_error=False)

api_router = APIRouter()
api_router.include_router(user_router)
api_router.include_router(team_router, dependencies=[Depends(API_KEY_HEADER)])
