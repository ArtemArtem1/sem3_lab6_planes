import logging
import sys

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.http import create_router
from app.config import get_settings
from app.domain.errors import StorageUnavailableError
from app.domain.services import PlaneService
from app.storage.client import HTTPPlaneRepository

settings = get_settings()

logging.basicConfig(
    level=settings.log_level,
    format="%(asctime)s %(levelname)s %(message)s",
    stream=sys.stdout,
)

repository = HTTPPlaneRepository(
    base_url=str(settings.storage_url),
    timeout=settings.request_timeout_s,
)

service = PlaneService(repository)

app = FastAPI(title="Plane API Gateway")

app.include_router(create_router(service))


@app.exception_handler(StorageUnavailableError)
async def storage_error_handler(
    request: Request,
    exc: StorageUnavailableError,
) -> JSONResponse:
    return JSONResponse(
        status_code=503,
        content={"detail": str(exc)},
    )

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
