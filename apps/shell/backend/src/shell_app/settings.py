"""Shell application settings."""

from mfe_common.settings import BaseAppSettings


class ShellSettings(BaseAppSettings):
    """Shell-specific settings."""

    app_name: str = "shell"
    app_port: int = 8000

    # Health check interval for registered apps (seconds)
    health_check_interval: int = 30
    # Number of consecutive failures before marking app unhealthy
    health_check_max_failures: int = 3
