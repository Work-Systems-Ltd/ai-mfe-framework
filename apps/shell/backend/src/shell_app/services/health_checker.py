"""Background health checker for registered MFE apps."""

import asyncio
import logging

import httpx

from shell_app.services.registry import registry
from shell_app.settings import ShellSettings

logger = logging.getLogger(__name__)


async def run_health_checks(settings: ShellSettings) -> None:
    """Periodically check health of all registered apps.

    Runs in a background task during the app's lifespan.
    """
    while True:
        await asyncio.sleep(settings.health_check_interval)

        for app in registry.list_all():
            if not app.health_check_url:
                continue

            try:
                async with httpx.AsyncClient() as client:
                    resp = await client.get(app.health_check_url, timeout=5.0)
                    resp.raise_for_status()
                    registry.mark_healthy(app.name)
            except (httpx.ConnectError, httpx.HTTPStatusError, httpx.TimeoutException):
                registry.mark_unhealthy(app.name)
                logger.warning(
                    "Health check failed",
                    extra={
                        "app_name": app.name,
                        "url": app.health_check_url,
                        "consecutive_failures": app.consecutive_failures + 1,
                    },
                )
