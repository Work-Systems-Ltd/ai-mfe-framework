"""OpenFGA service - wraps the OpenFGA HTTP API."""

import logging
from typing import Any

import httpx

from permissions_app.settings import PermissionsSettings

logger = logging.getLogger(__name__)


class FGAService:
    """Service layer wrapping OpenFGA HTTP API operations."""

    def __init__(self, settings: PermissionsSettings) -> None:
        self.api_url = settings.openfga_api_url
        self.store_id = settings.openfga_store_id
        self.model_id = settings.openfga_model_id

    @property
    def _base_url(self) -> str:
        return f"{self.api_url}/stores/{self.store_id}"

    async def ensure_store(self) -> str:
        """Create store if it doesn't exist. Returns store ID."""
        if self.store_id:
            return self.store_id

        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{self.api_url}/stores",
                json={"name": "mfe-permissions"},
                timeout=10.0,
            )
            resp.raise_for_status()
            data: dict[str, Any] = resp.json()
            self.store_id = data["id"]
            logger.info("Created OpenFGA store", extra={"store_id": self.store_id})
            return self.store_id

    async def write_model(self, model_json: dict[str, Any]) -> str:
        """Write an authorization model. Returns model ID."""
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{self._base_url}/authorization-models",
                json=model_json,
                timeout=10.0,
            )
            resp.raise_for_status()
            data: dict[str, Any] = resp.json()
            self.model_id = data["authorization_model_id"]
            logger.info("Wrote authorization model", extra={"model_id": self.model_id})
            return self.model_id

    async def check(self, user: str, relation: str, obj: str) -> bool:
        """Check if a user has a relation to an object."""
        payload: dict[str, object] = {
            "tuple_key": {"user": user, "relation": relation, "object": obj},
        }
        if self.model_id:
            payload["authorization_model_id"] = self.model_id

        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{self._base_url}/check",
                json=payload,
                timeout=10.0,
            )
            resp.raise_for_status()
            data: dict[str, bool] = resp.json()
            return data.get("allowed", False)

    async def list_objects(self, user: str, relation: str, obj_type: str) -> list[str]:
        """List objects a user has a relation to."""
        payload: dict[str, object] = {
            "user": user,
            "relation": relation,
            "type": obj_type,
        }
        if self.model_id:
            payload["authorization_model_id"] = self.model_id

        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{self._base_url}/list-objects",
                json=payload,
                timeout=10.0,
            )
            resp.raise_for_status()
            data: dict[str, list[str]] = resp.json()
            return data.get("objects", [])

    async def write_tuple(self, user: str, relation: str, obj: str) -> None:
        """Write a relationship tuple."""
        payload: dict[str, Any] = {
            "writes": {
                "tuple_keys": [{"user": user, "relation": relation, "object": obj}],
            },
        }
        if self.model_id:
            payload["authorization_model_id"] = self.model_id

        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{self._base_url}/write",
                json=payload,
                timeout=10.0,
            )
            resp.raise_for_status()

    async def delete_tuple(self, user: str, relation: str, obj: str) -> None:
        """Delete a relationship tuple."""
        payload: dict[str, Any] = {
            "deletes": {
                "tuple_keys": [{"user": user, "relation": relation, "object": obj}],
            },
        }
        if self.model_id:
            payload["authorization_model_id"] = self.model_id

        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{self._base_url}/write",
                json=payload,
                timeout=10.0,
            )
            resp.raise_for_status()
