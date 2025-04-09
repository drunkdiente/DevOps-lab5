import uvicorn
from fastapi import FastAPI

from .settings import settings
from src.routers.user import router as user_router

app = FastAPI(debug=False)
app.include_router(user_router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run(
        app=app,
        host=settings.SERVER_ADDR,
        port=settings.SERVER_PORT,
        log_level="info"
    )
