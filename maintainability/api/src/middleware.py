from fastapi import Request
from fastapi.responses import JSONResponse
from . import io_operations


async def api_key_middleware(request: Request, call_next):
    api_key = request.headers.get("X-API-KEY", None)
    if api_key is None:
        return JSONResponse(
            status_code=400, content={"detail": "API key header missing"}
        )
    if not io_operations.api_key_exists(api_key):
        return JSONResponse(status_code=401, content={"detail": "Invalid API Key"})
    response = await call_next(request)
    return response
