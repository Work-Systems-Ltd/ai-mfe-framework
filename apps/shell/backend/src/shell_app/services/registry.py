"""In-memory app registry for MFE app registrations."""

import logging
from datetime import UTC, datetime

from shell_app.models.registration import AppRegistration, RegisteredApp

logger = logging.getLogger(__name__)


class AppRegistry:
    """Thread-safe in-memory registry of registered MFE apps."""

    def __init__(self) -> None:
        self._apps: dict[str, RegisteredApp] = {}

    def register(self, registration: AppRegistration) -> RegisteredApp:
        """Register or re-register an app."""
        app = RegisteredApp(
            **registration.model_dump(),
            registered_at=datetime.now(UTC),
            healthy=True,
            consecutive_failures=0,
        )
        self._apps[registration.name] = app
        logger.info("App registered", extra={"app_name": registration.name})
        return app

    def get(self, name: str) -> RegisteredApp | None:
        """Get a registered app by name."""
        return self._apps.get(name)

    def list_all(self) -> list[RegisteredApp]:
        """List all registered apps."""
        return list(self._apps.values())

    def list_healthy(self) -> list[RegisteredApp]:
        """List all healthy registered apps."""
        return [app for app in self._apps.values() if app.healthy]

    def mark_unhealthy(self, name: str) -> None:
        """Mark an app as unhealthy."""
        app = self._apps.get(name)
        if app:
            app.consecutive_failures += 1
            if app.consecutive_failures >= 3:
                app.healthy = False
                logger.warning("App marked unhealthy", extra={"app_name": name})

    def mark_healthy(self, name: str) -> None:
        """Mark an app as healthy (resets failure count)."""
        app = self._apps.get(name)
        if app:
            app.consecutive_failures = 0
            app.healthy = True

    def unregister(self, name: str) -> bool:
        """Remove an app from the registry."""
        if name in self._apps:
            del self._apps[name]
            return True
        return False


# Singleton registry instance
registry = AppRegistry()
