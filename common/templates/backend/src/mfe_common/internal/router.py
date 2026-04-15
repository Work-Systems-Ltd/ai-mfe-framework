"""Internal router with health and readiness endpoints.

All routes under /internal are excluded from OpenAPI/Swagger docs.
"""

from fastapi import APIRouter

internal_router = APIRouter(prefix="/internal", include_in_schema=False)


@internal_router.get("/health")
async def health() -> dict[str, str]:
    """Basic health check."""
    return {"status": "ok"}


@internal_router.get("/ready")
async def ready() -> dict[str, str]:
    """Readiness check."""
    return {"status": "ready"}
