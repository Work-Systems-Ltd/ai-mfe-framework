"""Reverse proxy service for forwarding requests to registered MFE apps."""

import logging

import httpx
from fastapi import Request, Response

logger = logging.getLogger(__name__)

# Hop-by-hop headers that should not be forwarded
_HOP_BY_HOP = frozenset({
    "connection",
    "keep-alive",
    "proxy-authenticate",
    "proxy-authorization",
    "te",
    "trailers",
    "transfer-encoding",
    "upgrade",
})


async def proxy_request(
    request: Request,
    target_base_url: str,
    path: str,
) -> Response:
    """Forward an HTTP request to a target URL.

    Args:
        request: Incoming FastAPI request.
        target_base_url: Base URL of the target service.
        path: Path to append to the base URL.

    Returns:
        Response from the target service.
    """
    target_url = f"{target_base_url}/{path}"
    if request.url.query:
        target_url += f"?{request.url.query}"

    # Forward headers, stripping hop-by-hop
    headers = {
        k: v
        for k, v in request.headers.items()
        if k.lower() not in _HOP_BY_HOP and k.lower() != "host"
    }

    body = await request.body()

    async with httpx.AsyncClient() as client:
        resp = await client.request(
            method=request.method,
            url=target_url,
            headers=headers,
            content=body,
            timeout=30.0,
        )

    # Forward response headers, stripping hop-by-hop
    response_headers = {
        k: v
        for k, v in resp.headers.items()
        if k.lower() not in _HOP_BY_HOP
    }

    return Response(
        content=resp.content,
        status_code=resp.status_code,
        headers=response_headers,
    )
