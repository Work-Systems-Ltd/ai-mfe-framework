"""Auth routes - login, logout, current user info."""

from fastapi import APIRouter, Depends

from mfe_common.auth.models import UserInfo

router = APIRouter(prefix="/api/auth", tags=["auth"])

# NOTE: get_current_user dependency is injected at app setup time
# This avoids circular imports and allows settings-based configuration
_get_current_user = None  # type: ignore[assignment]


def configure_auth_router(get_current_user):  # type: ignore[no-untyped-def]
    """Configure the auth router with the get_current_user dependency."""
    global _get_current_user  # noqa: PLW0603
    _get_current_user = get_current_user


@router.get("/me")
async def get_me(user: UserInfo = Depends(lambda: _get_current_user)) -> UserInfo:
    """Get current authenticated user information."""
    return user


# NOTE: Login is handled client-side via keycloak-js PKCE flow.
# The /api/auth/me endpoint validates the token server-side.
# Logout is also handled client-side by keycloak-js.
