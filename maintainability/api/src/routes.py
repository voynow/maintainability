import os
from datetime import datetime
from typing import Dict

import jwt
from fastapi import APIRouter, HTTPException
from jose import jwt

from . import io_operations, models, routes_helper

router = APIRouter()


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

    access_token = jwt.encode(
        {"sub": email}, os.getenv("JWT_SECRET", "your-secret-key"), algorithm="HS256"
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/generate_key")
async def generate_key(user: models.User):
    api_key = routes_helper.generate_new_api_key()
    while io_operations.api_key_exists(api_key):
        api_key = routes_helper.generate_new_api_key()

    io_operations.write_api_key(
        api_key=api_key,
        user=user["email"],
        creation_date=datetime.utcnow().isoformat(),
        status="active",
    )
    return {"api_key": api_key}
