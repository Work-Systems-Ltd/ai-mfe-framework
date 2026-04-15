"""Tests for internal health/ready endpoints."""

import pytest
from httpx import ASGITransport, AsyncClient

from mfe_common.app_factory import create_app
from mfe_common.settings import BaseAppSettings


@pytest.fixture
def settings() -> BaseAppSettings:
    return BaseAppSettings(
        app_name="test-app",
        shell_register_address="http://localhost:8000",
    )


@pytest.fixture
def app(settings: BaseAppSettings):  # type: ignore[no-untyped-def]
    return create_app(settings, register_with_shell=False)


@pytest.mark.asyncio
async def test_health(app) -> None:  # type: ignore[no-untyped-def]
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.get("/internal/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_ready(app) -> None:  # type: ignore[no-untyped-def]
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.get("/internal/ready")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ready"}


@pytest.mark.asyncio
async def test_internal_routes_not_in_openapi(app) -> None:  # type: ignore[no-untyped-def]
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.get("/openapi.json")
    openapi = resp.json()
    paths = list(openapi.get("paths", {}).keys())
    assert not any(p.startswith("/internal") for p in paths)
