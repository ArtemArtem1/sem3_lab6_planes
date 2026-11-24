import logging
from dataclasses import asdict

import httpx
from pydantic import TypeAdapter, ValidationError

from app.domain.errors import StorageUnavailableError
from app.domain.models import Plane, PlaneCreate

logger = logging.getLogger(__name__)


class HTTPPlaneRepository:

    def __init__(self, base_url: str, timeout: float) -> None:
        self._base_url = base_url
        self._timeout = timeout
        self._adapter: TypeAdapter[Plane] = TypeAdapter(Plane)

    def _request(
        self,
        method: str,
        path: str,
        data: dict[str, str] | None = None,
    ) -> httpx.Response:
        try:
            with httpx.Client(
                base_url=self._base_url,
                timeout=self._timeout,
            ) as client:
                response = client.request(
                    method,
                    path,
                    json=data,
                )

            if method == "GET" and response.status_code == 404:
                return response

            response.raise_for_status()

            return response

        except httpx.HTTPError as exc:
            logger.warning(
                "Storage request failed: %s",
                type(exc).__name__,
            )
            raise StorageUnavailableError(
                "Storage service unavailable"
            ) from exc

    def _parse_plane(self, response: httpx.Response) -> Plane:
        try:
            return self._adapter.validate_json(response.content)
        except ValidationError as exc:
            logger.warning("Invalid response from storage")
            raise StorageUnavailableError(
                "Invalid response from storage service"
            ) from exc

    def save(self, plane: PlaneCreate) -> Plane:
        response = self._request(
            "POST",
            "/planes",
            asdict(plane),
        )

        return self._parse_plane(response)

    def get(self, plane_id: int) -> Plane | None:
        response = self._request(
            "GET",
            f"/planes/{plane_id}",
        )

        if response.status_code == 404:
            return None

        return self._parse_plane(response)
