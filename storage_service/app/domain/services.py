from app.domain.models import Plane, PlaneCreate
from app.domain.ports import PlaneRepository


class PlaneService:

    def __init__(self, repo: PlaneRepository) -> None:
        self._repo = repo

    def create(self, plane: PlaneCreate) -> Plane:
        registration = plane.registration.strip().upper()
        model = plane.model.strip()
        airline = plane.airline.strip()

        if not registration:
            raise ValueError("Registration must not be empty")

        if not model:
            raise ValueError("Model must not be empty")

        if not airline:
            raise ValueError("Airline must not be empty")

        normalized = PlaneCreate(
            registration=registration,
            model=model,
            airline=airline,
        )

        return self._repo.save(normalized)

    def get(self, plane_id: int) -> Plane | None:
        if plane_id <= 0:
            raise ValueError("ID must be positive")

        return self._repo.get(plane_id)
