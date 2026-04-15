"""FastAPI dependencies for JWT authentication via Keycloak."""

import logging
import time
from typing import Any

import httpx
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from mfe_common.auth.models import TokenPayload, UserInfo
from mfe_common.settings import BaseAppSettings

logger = logging.getLogger(__name__)

security = HTTPBearer()

# JWKS cache
_jwks_cache: dict[str, Any] = {}
_jwks_cache_expiry: float = 0.0
_JWKS_CACHE_TTL: float = 300.0  # 5 minutes


async def _get_jwks(settings: BaseAppSettings) -> dict[str, Any]:
    """Fetch and cache JWKS from Keycloak."""
    global _jwks_cache, _jwks_cache_expiry  # noqa: PLW0603

    if _jwks_cache and time.time() < _jwks_cache_expiry:
        return _jwks_cache

    jwks_url = f"{settings.keycloak_url}/realms/{settings.keycloak_realm}/protocol/openid-connect/certs"
    async with httpx.AsyncClient() as client:
        resp = await client.get(jwks_url, timeout=10.0)
        resp.raise_for_status()
        _jwks_cache = resp.json()
        _jwks_cache_expiry = time.time() + _JWKS_CACHE_TTL

    return _jwks_cache


def _create_get_current_user(settings: BaseAppSettings):  # type: ignore[no-untyped-def]
    """Create a get_current_user dependency bound to specific settings."""

    async def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security),
    ) -> UserInfo:
        """Validate JWT token and return current user info."""
        token = credentials.credentials
        try:
            jwks = await _get_jwks(settings)
            jwks_client = jwt.PyJWKClient.__new__(jwt.PyJWKClient)
            jwks_client.jwk_set = jwt.PyJWKSet.from_dict(jwks)
            signing_key = jwks_client.get_signing_key_from_jwt(token)

            payload_data = jwt.decode(
                token,
                signing_key.key,
                algorithms=["RS256"],
                issuer=f"{settings.keycloak_url}/realms/{settings.keycloak_realm}",
                options={"verify_aud": False},
            )
            payload = TokenPayload(**payload_data)

            realm_roles = payload.realm_access.get("roles", [])

            return UserInfo(
                sub=payload.sub,
                username=payload.preferred_username,
                email=payload.email,
                first_name=payload.given_name,
                last_name=payload.family_name,
                roles=realm_roles,
            )
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
            )
        except jwt.InvalidTokenError as e:
            logger.warning("Invalid JWT token", extra={"error": str(e)})
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )

    return get_current_user


def get_auth_dependency(settings: BaseAppSettings):  # type: ignore[no-untyped-def]
    """Get a configured get_current_user dependency for the given settings.

    Usage in app setup:
        get_current_user = get_auth_dependency(settings)

    Then in routes:
        @router.get("/me")
        async def me(user: UserInfo = Depends(get_current_user)):
            return user
    """
    return _create_get_current_user(settings)
