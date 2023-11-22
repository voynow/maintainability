import os
from dotenv import load_dotenv
import traceback

import json
import jwt
from fastapi import HTTPException, Request
from jose import jwt, JWTError
from fastapi.responses import JSONResponse

from . import io_operations, logger

load_dotenv()
SUPABASE_JWT_SECRET = os.environ["SUPABASE_JWT_SECRET"]


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
    optional_auth = ["/insert_file", "/extract_metrics", "/get_user_email"]
    middleware = api_key_or_jwt_middleware if path in optional_auth else jwt_middleware
    middleware(request)


async def mixed_auth_middleware(request: Request, call_next):
    log_data = {
        "path": request.url.path,
        "method": request.method,
        "headers": str(request.headers),
        "client_ip": request.client.host,
    }
    try:
        response = await call_next(request)
        log_data["status_code"] = response.status_code
    except Exception as exc:
        log_data["error"] = str(exc)
        log_data["traceback"] = traceback.format_exc()
        response = JSONResponse(status_code=500, content={"detail": str(exc)})
    finally:
        logger.logger(json.dumps(log_data))
    return response
