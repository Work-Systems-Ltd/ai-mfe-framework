"""Shell application entry point."""

import asyncio
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from mfe_common.auth.dependencies import get_auth_dependency
from mfe_common.internal.router import internal_router
from mfe_common.logging import setup_logging
from shell_app.routers import apps, auth, proxy
from shell_app.services.health_checker import run_health_checks
from shell_app.settings import ShellSettings

settings = ShellSettings()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """App lifespan: start background health checker."""
    task = asyncio.create_task(run_health_checks(settings))
    yield
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass


def create_app() -> FastAPI:
    """Create the shell FastAPI application."""
    setup_logging(log_level=settings.log_level, app_name=settings.app_name)

    app = FastAPI(
        title="MFE Shell",
        description="Micro-frontend framework shell application",
        lifespan=lifespan,
    )

    # Configure auth
    get_current_user = get_auth_dependency(settings)
    auth.configure_auth_router(get_current_user)

    # Include routers
    app.include_router(internal_router)  # /internal/health, /internal/ready
    app.include_router(apps.internal_router)  # /internal/register
    app.include_router(auth.router)  # /api/auth/*
    app.include_router(apps.router)  # /api/apps/*
    app.include_router(proxy.router)  # /apps/{app_name}/*

    return app


app = create_app()
