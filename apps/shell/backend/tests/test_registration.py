"""Tests for app registration flow."""

import pytest
from httpx import ASGITransport, AsyncClient

from shell_app.main import app
from shell_app.services.registry import registry


@pytest.fixture(autouse=True)
def clear_registry():
    """Clear registry between tests."""
    registry._apps.clear()
    yield
    registry._apps.clear()


@pytest.mark.asyncio
async def test_register_app() -> None:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.post(
            "/internal/register",
            json={
                "name": "test-app",
                "display_name": "Test App",
                "frontend_url": "http://test-frontend:5173",
                "backend_url": "http://test-backend:8000",
                "path_prefix": "/apps/test-app",
                "sidebar_links": [
                    {
                        "label": "Dashboard",
                        "path": "/",
                        "sublinks": [
                            {"label": "Items", "path": "/items"},
                        ],
                    }
                ],
            },
        )
    assert resp.status_code == 200
    data = resp.json()
    assert data["name"] == "test-app"
    assert data["healthy"] is True


@pytest.mark.asyncio
async def test_list_apps_after_registration() -> None:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # Register an app
        await client.post(
            "/internal/register",
            json={
                "name": "app1",
                "display_name": "App 1",
                "frontend_url": "http://app1-frontend:5173",
                "backend_url": "http://app1-backend:8000",
                "path_prefix": "/apps/app1",
            },
        )

        # List apps
        resp = await client.get("/api/apps")

    assert resp.status_code == 200
    apps = resp.json()
    assert len(apps) == 1
    assert apps[0]["name"] == "app1"


@pytest.mark.asyncio
async def test_re_registration_overwrites() -> None:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        payload = {
            "name": "app1",
            "display_name": "App 1",
            "frontend_url": "http://app1-frontend:5173",
            "backend_url": "http://app1-backend:8000",
            "path_prefix": "/apps/app1",
        }

        await client.post("/internal/register", json=payload)
        payload["display_name"] = "App 1 Updated"
        await client.post("/internal/register", json=payload)

        resp = await client.get("/api/apps")

    apps = resp.json()
    assert len(apps) == 1
    assert apps[0]["display_name"] == "App 1 Updated"
