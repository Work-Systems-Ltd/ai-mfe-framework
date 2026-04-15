"""Permissions service settings."""

from mfe_common.settings import BaseAppSettings


class PermissionsSettings(BaseAppSettings):
    """Permissions app specific settings."""

    app_name: str = "permissions"
    app_port: int = 8000
