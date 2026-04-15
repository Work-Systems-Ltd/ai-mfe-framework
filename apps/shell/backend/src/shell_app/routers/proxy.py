"""Reverse proxy routes for forwarding requests to registered MFE apps."""

from fastapi import APIRouter, HTTPException, Request, Response

from shell_app.services.proxy import proxy_request
from shell_app.services.registry import registry

router = APIRouter(include_in_schema=False)


@router.api_route(
    "/apps/{app_name}/{path:path}",
    methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"],
)
async def proxy_to_app(app_name: str, path: str, request: Request) -> Response:
    """Proxy requests to registered MFE apps.

    Routes containing /api/ in the path are forwarded to the app's backend_url.
    All other routes are forwarded to the app's frontend_url.
    """
    registered_app = registry.get(app_name)
    if not registered_app:
        raise HTTPException(status_code=404, detail=f"App '{app_name}' not registered")

    if not registered_app.healthy:
        raise HTTPException(status_code=503, detail=f"App '{app_name}' is unhealthy")

    # Route to backend or frontend based on path
    if path.startswith("api/") or path == "api":
        target_base = registered_app.backend_url
    else:
        target_base = registered_app.frontend_url

    return await proxy_request(request, target_base, path)
