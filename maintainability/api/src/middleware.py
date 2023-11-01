import os

import json
import jwt
from fastapi import HTTPException, Request
from jose import jwt, JWTError

from . import io_operations, logger

SUPABASE_JWT_SECRET = os.environ.get("SUPABASE_JWT_SECRET")


def api_key_middleware(request: Request):
    """some functions are exposed via API key for data ingestion"""
    api_key = request.headers.get("X-API-KEY", None)
    if api_key is None or not io_operations.select_api_key(api_key):
        raise HTTPException(status_code=401, detail="Invalid API Key")


def jwt_middleware(request: Request):
    """most functions are exposed via JWT for webapp access"""
    token = request.headers.get("authorization", None)
    if token is None:
        raise HTTPException(status_code=401, detail="Token missing")
    try:
        jwt.decode(
            token.replace("Bearer ", "", 1),
            SUPABASE_JWT_SECRET,
            algorithms=["HS256"],
            options={"verify_aud": False},
        )
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


def api_key_or_jwt_middleware(request: Request):
    """some functions are used in API key workflows and in the webapp"""
    auth_methods = [api_key_middleware, jwt_middleware]

    errors = []
    for method in auth_methods:
        try:
            method(request)
            return  # Exit if any method succeeds
        except HTTPException as e:
            errors.append(str(e.detail))

    raise HTTPException(status_code=401, detail=f"Failures: {', '.join(errors)}")


def auth_strategy_dispatcher(request: Request):
    """dispatches to the correct auth strategy based on the request path"""
    path = request.url.path
    auth_map = {
        "/insert_file": api_key_middleware,
        "/extract_metrics": api_key_middleware,
        "/get_user_email": api_key_or_jwt_middleware,
    }
    middleware = auth_map.get(path, jwt_middleware)
    middleware(request)


async def mixed_auth_middleware(request: Request, call_next):
    """middleware for handling auth"""
    log_data = {
        "path": request.url.path,
        "method": request.method,
        "client_ip": request.client.host,
        "user_agent": request.headers.get("User-Agent", "Unknown"),
    }
    logger.logger(f"Received Request: {json.dumps(log_data)}")

    if request.method != "OPTIONS":
        auth_strategy_dispatcher(request)
    response = await call_next(request)
    return response
