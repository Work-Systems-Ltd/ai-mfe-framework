"""FastAPI dependencies for permission checks via OpenFGA."""

import logging
from collections.abc import Callable, Coroutine
from typing import Any

from fastapi import Depends, HTTPException, status

from mfe_common.auth.models import UserInfo
from mfe_common.permissions.client import OpenFGAClient
from mfe_common.settings import BaseAppSettings

logger = logging.getLogger(__name__)


def require_permission(
    relation: str,
    object_type: str,
    settings: BaseAppSettings,
    get_current_user: Callable[..., Coroutine[Any, Any, UserInfo]],
    object_id_param: str = "id",
) -> Callable[..., Coroutine[Any, Any, None]]:
    """Create a FastAPI dependency that checks a permission via OpenFGA.

    Usage:
        @router.get(
            "/items/{id}",
            dependencies=[Depends(require_permission("can_view", "resource", settings, get_current_user))],
        )
        async def get_item(id: str): ...

    Args:
        relation: The relation to check, e.g. "can_view".
        object_type: The OpenFGA object type, e.g. "resource".
        settings: App settings with OpenFGA configuration.
        get_current_user: The auth dependency for getting current user.
        object_id_param: The path parameter name containing the object ID.
    """
    fga_client = OpenFGAClient(settings)

    async def _check_permission(
        user: UserInfo = Depends(get_current_user),
        **kwargs: str,
    ) -> None:
        object_id = kwargs.get(object_id_param, "")
        fga_object = f"{object_type}:{object_id}"
        fga_user = f"user:{user.sub}"

        allowed = await fga_client.check(user=fga_user, relation=relation, obj=fga_object)
        if not allowed:
            logger.warning(
                "Permission denied",
                extra={
                    "user": fga_user,
                    "relation": relation,
                    "object": fga_object,
                },
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permission denied",
            )

    return _check_permission
