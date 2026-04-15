"""Keycloak OIDC client for shell auth operations."""

import logging
from typing import Any

import httpx

from shell_app.settings import ShellSettings

logger = logging.getLogger(__name__)


class KeycloakClient:
    """Client for Keycloak OIDC operations."""

    def __init__(self, settings: ShellSettings) -> None:
        self.base_url = settings.keycloak_url
        self.realm = settings.keycloak_realm
        self.client_id = settings.keycloak_client_id
        self.client_secret = settings.keycloak_client_secret

    @property
    def _realm_url(self) -> str:
        return f"{self.base_url}/realms/{self.realm}"

    @property
    def _token_url(self) -> str:
        return f"{self._realm_url}/protocol/openid-connect/token"

    @property
    def _userinfo_url(self) -> str:
        return f"{self._realm_url}/protocol/openid-connect/userinfo"

    @property
    def _logout_url(self) -> str:
        return f"{self._realm_url}/protocol/openid-connect/logout"

    async def get_openid_config(self) -> dict[str, Any]:
        """Fetch the OpenID Connect discovery document."""
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"{self._realm_url}/.well-known/openid-configuration",
                timeout=10.0,
            )
            resp.raise_for_status()
            result: dict[str, Any] = resp.json()
            return result

    async def exchange_code(self, code: str, redirect_uri: str) -> dict[str, Any]:
        """Exchange an authorization code for tokens."""
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                self._token_url,
                data={
                    "grant_type": "authorization_code",
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "code": code,
                    "redirect_uri": redirect_uri,
                },
                timeout=10.0,
            )
            resp.raise_for_status()
            result: dict[str, Any] = resp.json()
            return result

    async def get_userinfo(self, access_token: str) -> dict[str, Any]:
        """Get user info from Keycloak using an access token."""
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                self._userinfo_url,
                headers={"Authorization": f"Bearer {access_token}"},
                timeout=10.0,
            )
            resp.raise_for_status()
            result: dict[str, Any] = resp.json()
            return result

    async def logout_user(self, refresh_token: str) -> None:
        """Logout a user by invalidating their refresh token."""
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                self._logout_url,
                data={
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "refresh_token": refresh_token,
                },
                timeout=10.0,
            )
            resp.raise_for_status()
