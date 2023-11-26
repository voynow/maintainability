import os
from dotenv import load_dotenv
import traceback

import json
import jwt
from fastapi import HTTPException, Request
from jose import jwt, JWTError
from fastapi.responses import JSONResponse

from . import logger

load_dotenv()
SUPABASE_JWT_SECRET = os.environ["SUPABASE_JWT_SECRET"]


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


async def mixed_auth_middleware(request: Request, call_next):
    log_data = {
        "path": request.url.path,
        "method": request.method,
        "headers": str(request.headers),
        "client_ip": request.client.host,
    }
    try:
        jwt_middleware(request)
        response = await call_next(request)
        log_data["status_code"] = response.status_code
    except Exception as exc:
        log_data["error"] = str(exc)
        log_data["traceback"] = traceback.format_exc()
        response = JSONResponse(status_code=500, content={"detail": str(exc)})
    finally:
        logger.logger(json.dumps(log_data))
    return response
