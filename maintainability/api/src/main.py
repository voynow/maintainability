import logging
import os
from pathlib import Path
from typing import Dict
import uuid

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import JSONResponse
from jose import jwt
from passlib.context import CryptContext

from . import config, io_operations, metrics_manager, models

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
app = FastAPI()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def read_root():
    return {"status": "ok"}


@app.post("/submit_metrics")
async def submit_metrics(metrics: Dict[str, models.CompositeMetrics]):
    io_operations.write_metrics(metrics)
    return {"status": "ok", "message": "Metrics submitted successfully."}


def compose_repo_metrics(repo: Dict[str, str]):
    session_id = str(uuid.uuid4())
    composite_metrics: Dict[str, models.CompositeMetrics] = {}

    for filepath, code in repo.items():
        if len(code.splitlines()) < config.MIN_NUM_LINES:
            io_operations.logger(
                f"Skipping {filepath} because it has less than {config.MIN_NUM_LINES} lines of code."
            )
        else:
            if filepath.startswith("test") or Path(filepath).stem.endswith("test"):
                io_operations.logger(f"Skipping {filepath} because it is a test file.")
            else:
                io_operations.logger(f"Processing {filepath}...")
                composite_metrics[filepath] = metrics_manager.compose_metrics(
                    filepath, code, session_id
                )
    return composite_metrics


@app.post("/extract_metrics")
async def extract_metrics(repo: Dict[str, str]):
    try:
        return compose_repo_metrics(repo)
    except Exception as e:
        logger.exception("An error occurred in /extract_metrics")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/register", response_model=models.User)
def register(user: models.User):
    hashed_password = pwd_context.hash(user.password)
    try:
        io_operations.write_user(user.email, hashed_password)
    except Exception as e:
        logger.exception("An error occurred in /register")
        raise HTTPException(status_code=500, detail=str(e))

    return {
        "email": user.email,
        "password": hashed_password,
        "role": user.role,
    }


@app.post("/token", response_model=models.Token)
async def login_for_access_token(token_request: models.TokenRequest):
    email = token_request.email
    password = token_request.password

    # Fetch user from DB
    user = io_operations.get_user(email)

    if not user or not pwd_context.verify(password, user["password"]):
        logger.warning(f"Unauthorized login attempt: email={email}")
        return JSONResponse(
            status_code=401, content={"detail": "Incorrect email or password"}
        )

    access_token = jwt.encode(
        {"sub": email}, os.getenv("JWT_SECRET", "your-secret-key"), algorithm="HS256"
    )
    return {"access_token": access_token, "token_type": "bearer"}
