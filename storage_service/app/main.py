import logging
import sys

import uvicorn
from fastapi import FastAPI

from app.api.http import create_router
from app.config import get_settings
from app.domain.services import PlaneService
from app.storage.repository import SQLitePlaneRepository

settings = get_settings()

logging.basicConfig(
    level=settings.log_level,
    format="%(asctime)s %(levelname)s %(message)s",
    stream=sys.stdout,
)

repository = SQLitePlaneRepository(settings.db_path)
service = PlaneService(repository)

app = FastAPI(title="Plane Storage Service")

app.include_router(create_router(service))

@app.get("/health")
def health() -> dict[str, str]:
    service.get(1)
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(
        app,
        host=settings.host,
        port=settings.port,
        log_level=settings.log_level.lower(),
    )
