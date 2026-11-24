from fastapi import APIRouter, HTTPException

from app.api.schemas import PlaneCreateSchema, PlaneSchema
from app.domain.models import PlaneCreate
from app.domain.services import PlaneService


def create_router(service: PlaneService) -> APIRouter:
    router = APIRouter()

    @router.post(
        "/planes",
        response_model=PlaneSchema,
        status_code=201,
    )
    def create_plane(data: PlaneCreateSchema) -> PlaneSchema:
        try:
            plane = service.create(
                PlaneCreate(
                    registration=data.registration,
                    model=data.model,
                    airline=data.airline,
                )
            )
        except ValueError as exc:
            raise HTTPException(
                status_code=422,
                detail=str(exc),
            ) from exc

        return PlaneSchema.model_validate(plane)

    @router.get(
        "/planes/{plane_id}",
        response_model=PlaneSchema,
    )
    def get_plane(plane_id: int) -> PlaneSchema:
        try:
            plane = service.get(plane_id)
        except ValueError as exc:
            raise HTTPException(
                status_code=422,
                detail=str(exc),
            ) from exc

        if plane is None:
            raise HTTPException(
                status_code=404,
                detail="Plane not found",
            )

        return PlaneSchema.model_validate(plane)

    return router
