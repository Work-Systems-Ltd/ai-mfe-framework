"""Base application settings for all MFE backend apps."""

from pydantic import Field
from pydantic_settings import BaseSettings


class BaseAppSettings(BaseSettings):
    """Base settings that every MFE backend app must configure."""

    app_name: str
    app_port: int = 8000
    log_level: str = "INFO"

    # Shell registration
    shell_register_address: str = Field(
        default="http://shell-backend:8000",
        description="URL of the shell's registration endpoint",
    )

    # App URLs (how the shell can reach this app)
    app_frontend_url: str = Field(
        default="",
        description="Internal Docker URL for this app's frontend, e.g. http://example-frontend:5173",
    )
    app_backend_url: str = Field(
        default="",
        description="Internal Docker URL for this app's backend, e.g. http://example-backend:8000",
    )
    app_path_prefix: str = Field(
        default="",
        description="Path prefix for this app, e.g. /apps/example1",
    )

    # Keycloak auth
    keycloak_url: str = "http://keycloak:8080"
    keycloak_realm: str = "mfe"
    keycloak_client_id: str = ""
    keycloak_client_secret: str = ""

    # OpenFGA permissions
    openfga_api_url: str = "http://openfga:8080"
    openfga_store_id: str = ""
    openfga_model_id: str = ""

    model_config = {"env_prefix": "", "env_file": ".env", "extra": "ignore"}
