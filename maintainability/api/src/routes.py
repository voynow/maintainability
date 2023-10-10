import os
from datetime import datetime
from typing import Dict

import jwt
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from jose import jwt

from . import io_operations, models, routes_helper

router = APIRouter()


async def api_key_middleware(request: Request, call_next):
    if request.url.path in ["/submit_metrics", "/extract_metrics"]:
        api_key = request.headers.get("X-API-KEY", None)
        if api_key is None:
            return JSONResponse(
                status_code=400, content={"detail": "API key header missing"}
            )
        if not io_operations.api_key_exists(api_key):
            return JSONResponse(status_code=401, content={"detail": "Invalid API Key"})

    response = await call_next(request)
    return response


@router.get("/health")
def read_root():
    return {"status": "ok"}


@router.post("/submit_metrics")
async def submit_metrics(metrics: Dict[str, models.CompositeMetrics]):
    io_operations.write_metrics(metrics)
    return {"status": "ok", "message": "Metrics submitted successfully."}


@router.post("/extract_metrics")
async def extract_metrics(repo: Dict[str, str]):
    try:
        return routes_helper.compose_repo_metrics(repo)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/register", response_model=models.User)
def register(user: models.User):
    hashed_password = routes_helper.pwd_context.hash(user.password)
    io_operations.write_user(user.email, hashed_password)
    return {"email": user.email, "password": hashed_password, "role": user.role}


@router.post("/token", response_model=models.Token)
async def login_for_access_token(token_request: models.TokenRequest):
    email = token_request.email
    password = token_request.password
    routes_helper.validate_user(email, password)

    # TODO add secret key
    access_token = jwt.encode(
        {"sub": email}, os.getenv("JWT_SECRET", "your-secret-key"), algorithm="HS256"
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/generate_key")
async def generate_key(email_obj: Dict[str, str]):
    api_key = routes_helper.generate_new_api_key()
    while io_operations.api_key_exists(api_key):
        api_key = routes_helper.generate_new_api_key()

    io_operations.write_api_key(
        api_key=api_key,
        user=email_obj["email"],
        creation_date=datetime.utcnow().isoformat(),
        status="active",
    )
    return {"api_key": api_key}


@router.get("/api_keys")
async def list_api_keys(email: str):
    api_keys = io_operations.list_api_keys(email)
    return {"api_keys": api_keys}


@router.delete("/api_keys/{api_key}")
async def remove_api_key(api_key: str):
    if io_operations.api_key_exists(api_key):
        io_operations.delete_api_key(api_key)
        return {"message": "API key deleted successfully"}
    else:
        return {"message": "API key not found"}, 404
