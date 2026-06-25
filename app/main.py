from fastapi import FastAPI

from fastapi.responses import JSONResponse
from fastapi import Request
from app.api.address import router as address_router
from app.core.config import settings
from app.core.database import Base, engine
from app.core.logger import logger

logger.info("Starting Address Book API")

# Create database tables
Base.metadata.create_all(bind=engine)
logger.info("Database tables initialized")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="REST API for managing an address book with nearby search.",
)


from fastapi.responses import JSONResponse
from fastapi import Request


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error"},
    )
# Register routers
app.include_router(address_router)


@app.get("/", tags=["Health"])
def health_check():
    return {
        "status": "healthy",
        "message": "Address Book API is running",
    }