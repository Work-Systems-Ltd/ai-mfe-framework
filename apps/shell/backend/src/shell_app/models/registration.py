"""App registration models for the MFE shell."""

from datetime import datetime

from pydantic import BaseModel


class SidebarSubLink(BaseModel):
    """A sub-link within a sidebar section."""

    label: str
    path: str  # relative to the app's path prefix
    icon: str | None = None


class SidebarLink(BaseModel):
    """A top-level sidebar link with optional sub-links."""

    label: str
    path: str
    icon: str | None = None
    sublinks: list[SidebarSubLink] = []


class AppRegistration(BaseModel):
    """Payload sent by MFE apps to register with the shell."""

    name: str  # unique identifier, e.g. "example1"
    display_name: str
    frontend_url: str  # internal docker URL, e.g. "http://example-frontend:5173"
    backend_url: str  # internal docker URL, e.g. "http://example-backend:8000"
    path_prefix: str  # e.g. "/apps/example1"
    sidebar_links: list[SidebarLink] = []
    health_check_url: str | None = None


class RegisteredApp(AppRegistration):
    """An app that has been registered with the shell."""

    registered_at: datetime
    healthy: bool = True
    consecutive_failures: int = 0
