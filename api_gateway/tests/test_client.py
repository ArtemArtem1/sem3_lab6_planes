from unittest.mock import patch

import httpx
import pytest

from app.domain.errors import StorageUnavailableError
from app.storage.client import HTTPPlaneRepository


def test_storage_unavailable() -> None:
    repo = HTTPPlaneRepository(
        base_url="http://storage.test",
        timeout=3.0,
    )

    with patch(
        "httpx.Client.request",
        side_effect=httpx.ConnectError("Connection refused"),
    ), pytest.raises(StorageUnavailableError):
        repo.get(1)


def test_storage_timeout() -> None:
    repo = HTTPPlaneRepository(
        base_url="http://storage.test",
        timeout=3.0,
    )

    with patch(
        "httpx.Client.request",
        side_effect=httpx.ReadTimeout("Request timed out"),
    ), pytest.raises(StorageUnavailableError):
        repo.get(1)
