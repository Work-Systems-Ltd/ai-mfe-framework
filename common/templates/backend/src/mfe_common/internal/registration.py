"""Shell registration - called on app startup to register with the shell app."""

import asyncio
import logging
from typing import Any

import httpx

from mfe_common.settings import BaseAppSettings

logger = logging.getLogger(__name__)


async def register_with_shell(
    settings: BaseAppSettings,
    sidebar_links: list[dict[str, Any]],
) -> None:
    """Register this app with the shell's internal registration endpoint.

    Called as part of the FastAPI lifespan. Retries with exponential backoff
    since the shell may not be up yet when this app starts.

    Args:
        settings: App settings containing shell address and app metadata.
        sidebar_links: List of sidebar link definitions for the shell's navigation.
    """
    payload = {
        "name": settings.app_name,
        "display_name": settings.app_name.replace("-", " ").title(),
        "frontend_url": settings.app_frontend_url,
        "backend_url": settings.app_backend_url,
        "path_prefix": settings.app_path_prefix,
        "sidebar_links": sidebar_links,
        "health_check_url": f"{settings.app_backend_url}/internal/health",
    }
    url = f"{settings.shell_register_address}/internal/register"

    for attempt in range(10):
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.post(url, json=payload, timeout=5.0)
                resp.raise_for_status()
                logger.info("Registered with shell successfully", extra={"app_name": settings.app_name})
                return
        except (httpx.ConnectError, httpx.HTTPStatusError) as exc:
            wait = min(2**attempt * 0.5, 30.0)
            logger.warning(
                "Failed to register with shell, retrying",
                extra={"attempt": attempt + 1, "wait_seconds": wait, "error": str(exc)},
            )
            await asyncio.sleep(wait)

    raise RuntimeError(f"Failed to register with shell after 10 attempts: {url}")
