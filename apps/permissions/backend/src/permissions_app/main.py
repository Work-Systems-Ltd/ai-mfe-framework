"""Permissions service entry point."""

from mfe_common.app_factory import create_app
from permissions_app.routers import checks, tuples
from permissions_app.services.fga_service import FGAService
from permissions_app.settings import PermissionsSettings

settings = PermissionsSettings()

# Create FGA service and configure routers
fga_service = FGAService(settings)
checks.configure_checks_router(fga_service)
tuples.configure_tuples_router(fga_service)

app = create_app(
    settings=settings,
    sidebar_links=[],  # Permissions app has no frontend/sidebar
    register_with_shell=True,
)

app.include_router(checks.router)
app.include_router(tuples.router)
