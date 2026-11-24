import pytest

from app.domain.models import Plane, PlaneCreate
from app.domain.services import PlaneService


class FakePlaneRepository:

    def __init__(self) -> None:
        self._data: dict[int, Plane] = {}

    def save(self, plane: PlaneCreate) -> Plane:
        result = Plane(
            id=len(self._data) + 1,
            registration=plane.registration,
            model=plane.model,
            airline=plane.airline,
        )

        self._data[result.id] = result
        return result

    def get(self, plane_id: int) -> Plane | None:
        return self._data.get(plane_id)


def test_create_plane() -> None:
    service = PlaneService(FakePlaneRepository())

    plane = service.create(
        PlaneCreate("RA-73175", "Boeing 737", "Aeroflot")
    )

    assert plane.id == 1
    assert plane.registration == "RA-73175"


def test_normalization() -> None:
    service = PlaneService(FakePlaneRepository())

    plane = service.create(
        PlaneCreate(" ra-73175 ", " Boeing 737 ", " Aeroflot ")
    )

    assert plane.registration == "RA-73175"
    assert plane.model == "Boeing 737"
    assert plane.airline == "Aeroflot"


def test_empty_registration() -> None:
    service = PlaneService(FakePlaneRepository())

    with pytest.raises(ValueError):
        service.create(
            PlaneCreate(" ", "Boeing 737", "Aeroflot")
        )


def test_get_plane() -> None:
    service = PlaneService(FakePlaneRepository())

    plane = service.create(
        PlaneCreate("RA-73175", "Boeing 737", "Aeroflot")
    )

    assert service.get(plane.id) == plane


def test_plane_not_found() -> None:
    service = PlaneService(FakePlaneRepository())

    assert service.get(99999) is None
