"""Example app settings."""

from mfe_common.settings import BaseAppSettings


class ExampleAppSettings(BaseAppSettings):
    """Example app specific settings."""

    app_name: str = "example1"
    app_port: int = 8000
    app_path_prefix: str = "/apps/example1"
