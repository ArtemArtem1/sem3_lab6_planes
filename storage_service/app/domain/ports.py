from typing import Protocol

from app.domain.models import Plane, PlaneCreate


class PlaneRepository(Protocol):

    def save(self, plane: PlaneCreate) -> Plane:
        ...

    def get(self, plane_id: int) -> Plane | None:
        ...
