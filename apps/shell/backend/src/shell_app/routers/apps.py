"""App listing and registration routes."""

from fastapi import APIRouter

from shell_app.models.registration import AppRegistration, RegisteredApp
from shell_app.services.registry import registry

# Public API router (shows in Swagger)
router = APIRouter(prefix="/api/apps", tags=["apps"])

# Internal registration router (hidden from Swagger)
internal_router = APIRouter(prefix="/internal", include_in_schema=False)


@internal_router.post("/register")
async def register_app(registration: AppRegistration) -> RegisteredApp:
    """Register an MFE app with the shell. Called by apps on startup."""
    return registry.register(registration)


@router.get("")
async def list_apps() -> list[RegisteredApp]:
    """List all registered MFE apps."""
    return registry.list_all()


@router.get("/healthy")
async def list_healthy_apps() -> list[RegisteredApp]:
    """List only healthy registered MFE apps."""
    return registry.list_healthy()


@router.get("/{app_name}")
async def get_app(app_name: str) -> RegisteredApp | None:
    """Get a specific registered app by name."""
    return registry.get(app_name)
