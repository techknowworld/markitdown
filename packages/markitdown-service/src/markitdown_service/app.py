# SPDX-License-Identifier: MIT
"""Combined REST + MCP HTTP service for MarkItDown.

Exposes:
  * GET  /health           - unauthenticated liveness/readiness probe
  * GET  /about            - unauthenticated HTML landing page
  * POST /convert          - {"uri": "..."} -> {"markdown": "..."}
                              (add ?format=text for a plain-text response)
  * POST /convert/upload   - multipart file upload -> {"markdown": "..."}
                              (add ?format=text for a plain-text response)
  * /mcp                   - the same MCP tool as markitdown-mcp, over
                              Streamable HTTP

Unlike markitdown-mcp (which is documented as local-only, unauthenticated,
bound to localhost), this service is meant to be reachable over the
network, so every route except /health requires an API key, and the
`file:` URI scheme is disallowed to avoid exposing the container's
filesystem to callers.
"""
import contextlib
import logging
import os
import tempfile
from collections.abc import AsyncIterator
from pathlib import Path

from fastapi import FastAPI, HTTPException, Query, UploadFile
from markitdown import MarkItDown
from mcp.server.fastmcp import FastMCP
from mcp.server.streamable_http_manager import StreamableHTTPSessionManager
from starlette.responses import HTMLResponse, JSONResponse, PlainTextResponse
from starlette.routing import Mount

from markitdown_service.about import ABOUT_HTML

UNAUTHENTICATED_PATHS = {"/health", "/about"}

logger = logging.getLogger("markitdown_service")

ALLOWED_URI_SCHEMES = {"http", "https", "data"}

API_KEY_HEADER_NAME = "x-api-key"


def _plugins_enabled() -> bool:
    return os.getenv("MARKITDOWN_ENABLE_PLUGINS", "false").strip().lower() in (
        "true",
        "1",
        "yes",
    )


def _get_markitdown() -> MarkItDown:
    return MarkItDown(enable_plugins=_plugins_enabled())


def _check_scheme(uri: str) -> None:
    scheme = uri.split(":", 1)[0].lower() if ":" in uri else ""
    if scheme not in ALLOWED_URI_SCHEMES:
        raise ValueError(
            f"URI scheme '{scheme}' is not allowed. Allowed schemes: "
            f"{', '.join(sorted(ALLOWED_URI_SCHEMES))}"
        )


def convert_uri_to_markdown(uri: str) -> str:
    """Shared conversion logic used by both the MCP tool and the REST route."""
    _check_scheme(uri)
    return _get_markitdown().convert_uri(uri).markdown


class ApiKeyAuthMiddleware:
    """Pure-ASGI (not BaseHTTPMiddleware) so it doesn't buffer the MCP SSE stream.

    Every route except /health requires a matching X-API-Key header. Fails
    closed: if MARKITDOWN_API_KEY isn't configured, all authenticated routes
    return 503 rather than silently running open, since this service (unlike
    markitdown-mcp) is meant to be reachable over the network.
    """

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http" or scope["path"] in UNAUTHENTICATED_PATHS:
            await self.app(scope, receive, send)
            return

        expected = os.getenv("MARKITDOWN_API_KEY")
        if not expected:
            logger.error(
                "MARKITDOWN_API_KEY is not set; rejecting request. "
                "Set it as a Container App secret before exposing this service."
            )
            response = JSONResponse(
                {"detail": "Service is not configured with an API key."},
                status_code=503,
            )
            await response(scope, receive, send)
            return

        headers = dict(scope["headers"])
        provided = headers.get(API_KEY_HEADER_NAME.encode())
        if provided is None or provided.decode() != expected:
            response = JSONResponse(
                {"detail": "Missing or invalid API key."}, status_code=401
            )
            await response(scope, receive, send)
            return

        await self.app(scope, receive, send)


# --- MCP server -------------------------------------------------------

mcp = FastMCP("markitdown")


@mcp.tool()
async def convert_to_markdown(uri: str) -> str:
    """Convert a resource described by an http:, https:, or data: URI to markdown."""
    return convert_uri_to_markdown(uri)


_mcp_server = mcp._mcp_server
_session_manager = StreamableHTTPSessionManager(
    app=_mcp_server,
    event_store=None,
    json_response=True,
    stateless=True,
)


async def _handle_streamable_http(scope, receive, send) -> None:
    await _session_manager.handle_request(scope, receive, send)


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    async with _session_manager.run():
        logger.info("MarkItDown service started (MCP session manager running).")
        yield
        logger.info("MarkItDown service shutting down.")


# --- REST app -----------------------------------------------------------

app = FastAPI(title="MarkItDown Service", lifespan=lifespan)
app.router.routes.append(Mount("/mcp", app=_handle_streamable_http))
app.add_middleware(ApiKeyAuthMiddleware)


@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}


@app.get("/about", response_class=HTMLResponse)
async def about() -> str:
    return ABOUT_HTML


FormatParam = Query(
    "json",
    pattern="^(json|text)$",
    description="'json' (default) returns {\"markdown\": ...}; 'text' returns the raw markdown as text/plain.",
)


def _format_response(markdown: str, format: str) -> dict | PlainTextResponse:
    if format == "text":
        return PlainTextResponse(markdown)
    return {"markdown": markdown}


@app.post("/convert", response_model=None)
async def convert(body: dict, format: str = FormatParam) -> dict | PlainTextResponse:
    uri = body.get("uri")
    if not uri:
        raise HTTPException(status_code=422, detail="Request body must include 'uri'.")
    try:
        markdown = convert_uri_to_markdown(uri)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        logger.exception("Conversion failed for uri=%s", uri)
        raise HTTPException(status_code=422, detail=f"Conversion failed: {e}")
    return _format_response(markdown, format)


@app.post("/convert/upload", response_model=None)
async def convert_upload(file: UploadFile, format: str = FormatParam) -> dict | PlainTextResponse:
    suffix = Path(file.filename or "").suffix
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
        tmp_path = Path(tmp.name)
        content = await file.read()
        tmp.write(content)
    try:
        markdown = _get_markitdown().convert(str(tmp_path)).markdown
    except Exception as e:
        logger.exception("Conversion failed for upload=%s", file.filename)
        raise HTTPException(status_code=422, detail=f"Conversion failed: {e}")
    finally:
        tmp_path.unlink(missing_ok=True)
    return _format_response(markdown, format)
