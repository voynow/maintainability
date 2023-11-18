import os
from dotenv import load_dotenv

import json
import jwt
from fastapi import HTTPException, Request
from jose import jwt, JWTError

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
    auth_map = {
        "/insert_file": api_key_middleware,
        "/extract_metrics": api_key_middleware,
        "/get_user_email": api_key_or_jwt_middleware,
    }
    middleware = auth_map.get(path, jwt_middleware)
    middleware(request)


async def mixed_auth_middleware(request: Request, call_next):
    # Log URL and method
    logger.logger(f"Request URL: {request.url.path}")
    logger.logger(f"Request method: {request.method}")
    logger.logger(f"Request headers: {request.headers}")

    # Read and log the body
    body = await request.body()
    if body:
        logger.logger(f"Request body: {body.decode('utf-8')}")

    # Set the body back to the request
    request._body = body

    # Call the next middleware or route handler
    response = await call_next(request)

    # Optionally, log the response status and headers
    logger.logger(f"Response status: {response.status_code}")
    logger.logger(f"Response headers: {response.headers}")

    # If you want to log the response body, it's a bit more complex because
    # you need to take care of not changing the original response.
    # If you need to log the response body, additional code will be required.

    return response
