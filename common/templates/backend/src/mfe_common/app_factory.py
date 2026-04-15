"""FastAPI application factory."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI

from mfe_common.internal.router import internal_router
from mfe_common.logging import setup_logging
from mfe_common.settings import BaseAppSettings


def create_app(
    settings: BaseAppSettings,
    sidebar_links: list[dict[str, Any]] | None = None,
    register_with_shell: bool = True,
) -> FastAPI:
    """Create a configured FastAPI application.

    Args:
        settings: Application settings.
        sidebar_links: Sidebar link definitions for shell registration.
        register_with_shell: Whether to register with the shell on startup.

    Returns:
        Configured FastAPI app with internal routes and logging.
    """
    setup_logging(log_level=settings.log_level, app_name=settings.app_name)

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
        if register_with_shell and sidebar_links is not None:
            from mfe_common.internal.registration import register_with_shell as do_register

            await do_register(settings, sidebar_links)
        yield

    app = FastAPI(
        title=settings.app_name,
        lifespan=lifespan,
    )
    app.include_router(internal_router)

    return app
