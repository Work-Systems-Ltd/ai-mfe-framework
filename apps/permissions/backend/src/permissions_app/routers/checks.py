"""Permission check endpoints."""

from fastapi import APIRouter
from pydantic import BaseModel

from permissions_app.services.fga_service import FGAService

router = APIRouter(prefix="/api/permissions", tags=["permissions"])


class CheckRequest(BaseModel):
    """Permission check request."""

    user: str  # e.g. "user:alice"
    relation: str  # e.g. "can_view"
    object: str  # e.g. "resource:doc1"


class CheckResponse(BaseModel):
    """Permission check response."""

    allowed: bool


class ListObjectsRequest(BaseModel):
    """List objects request."""

    user: str
    relation: str
    type: str  # object type to list


class ListObjectsResponse(BaseModel):
    """List objects response."""

    objects: list[str]


_fga_service: FGAService | None = None


def configure_checks_router(fga_service: FGAService) -> None:
    """Configure the router with an FGA service instance."""
    global _fga_service  # noqa: PLW0603
    _fga_service = fga_service


@router.post("/check")
async def check_permission(request: CheckRequest) -> CheckResponse:
    """Check if a user has a specific relation to an object."""
    assert _fga_service is not None
    allowed = await _fga_service.check(
        user=request.user,
        relation=request.relation,
        obj=request.object,
    )
    return CheckResponse(allowed=allowed)


@router.post("/list-objects")
async def list_objects(request: ListObjectsRequest) -> ListObjectsResponse:
    """List objects a user has a specific relation to."""
    assert _fga_service is not None
    objects = await _fga_service.list_objects(
        user=request.user,
        relation=request.relation,
        obj_type=request.type,
    )
    return ListObjectsResponse(objects=objects)
