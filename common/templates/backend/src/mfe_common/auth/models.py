"""Auth-related Pydantic models."""

from pydantic import BaseModel


class TokenPayload(BaseModel):
    """Decoded JWT token payload from Keycloak."""

    sub: str
    exp: int
    iat: int
    iss: str
    aud: str | list[str] = ""
    realm_access: dict[str, list[str]] = {}
    resource_access: dict[str, dict[str, list[str]]] = {}
    preferred_username: str = ""
    email: str = ""
    given_name: str = ""
    family_name: str = ""


class UserInfo(BaseModel):
    """Current authenticated user information."""

    sub: str
    username: str
    email: str
    first_name: str
    last_name: str
    roles: list[str]
