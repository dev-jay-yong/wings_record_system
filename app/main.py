from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from app.middlewares.access_controller import access_control
from app.routers import api_router


def create_app() -> FastAPI:
    fastapi_app = FastAPI()
    fastapi_app.add_middleware(middleware_class=BaseHTTPMiddleware, dispatch=access_control)
    fastapi_app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    fastapi_app.include_router(api_router)
    return fastapi_app


app = create_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", port=8000, host="0.0.0.0")
