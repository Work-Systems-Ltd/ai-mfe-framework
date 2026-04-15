"""OpenFGA client wrapper."""

import logging

import httpx

from mfe_common.settings import BaseAppSettings

logger = logging.getLogger(__name__)


class OpenFGAClient:
    """Thin wrapper around the OpenFGA HTTP API."""

    def __init__(self, settings: BaseAppSettings) -> None:
        self.api_url = settings.openfga_api_url
        self.store_id = settings.openfga_store_id
        self.model_id = settings.openfga_model_id

    @property
    def _base_url(self) -> str:
        return f"{self.api_url}/stores/{self.store_id}"

    async def check(self, user: str, relation: str, obj: str) -> bool:
        """Check if a user has a relation to an object.

        Args:
            user: User identifier, e.g. "user:alice".
            relation: Relation name, e.g. "can_view".
            obj: Object identifier, e.g. "resource:doc1".

        Returns:
            True if the relation is allowed.
        """
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
        """List objects a user has a relation to.

        Args:
            user: User identifier.
            relation: Relation name.
            obj_type: Object type to list.

        Returns:
            List of object identifiers.
        """
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
        payload = {
            "writes": {
                "tuple_keys": [{"user": user, "relation": relation, "object": obj}],
            },
        }
        if self.model_id:
            payload["authorization_model_id"] = self.model_id  # type: ignore[assignment]

        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{self._base_url}/write",
                json=payload,
                timeout=10.0,
            )
            resp.raise_for_status()

    async def delete_tuple(self, user: str, relation: str, obj: str) -> None:
        """Delete a relationship tuple."""
        payload = {
            "deletes": {
                "tuple_keys": [{"user": user, "relation": relation, "object": obj}],
            },
        }
        if self.model_id:
            payload["authorization_model_id"] = self.model_id  # type: ignore[assignment]

        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{self._base_url}/write",
                json=payload,
                timeout=10.0,
            )
            resp.raise_for_status()
