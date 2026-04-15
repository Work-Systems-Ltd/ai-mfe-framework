"""Relationship tuple management endpoints."""

from fastapi import APIRouter
from pydantic import BaseModel

from permissions_app.services.fga_service import FGAService

router = APIRouter(prefix="/api/permissions/tuples", tags=["tuples"])


class TupleRequest(BaseModel):
    """Tuple write/delete request."""

    user: str
    relation: str
    object: str


_fga_service: FGAService | None = None


def configure_tuples_router(fga_service: FGAService) -> None:
    """Configure the router with an FGA service instance."""
    global _fga_service  # noqa: PLW0603
    _fga_service = fga_service


@router.post("")
async def write_tuple(request: TupleRequest) -> dict[str, str]:
    """Write a new relationship tuple."""
    assert _fga_service is not None
    await _fga_service.write_tuple(
        user=request.user,
        relation=request.relation,
        obj=request.object,
    )
    return {"status": "ok"}


@router.delete("")
async def delete_tuple(request: TupleRequest) -> dict[str, str]:
    """Delete a relationship tuple."""
    assert _fga_service is not None
    await _fga_service.delete_tuple(
        user=request.user,
        relation=request.relation,
        obj=request.object,
    )
    return {"status": "ok"}
