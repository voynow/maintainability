import logging
import uuid
from pathlib import Path
from typing import Dict

from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext

from . import config, io_operations, metrics_manager, models

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
app = FastAPI()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


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


@app.post("/register", response_model=models.UserCreate)
def register(user: models.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    try:
        io_operations.write_user(user.email, hashed_password)
    except Exception as e:
        logger.exception("An error occurred in /register")
        raise HTTPException(status_code=500, detail=str(e))

    return {
        "email": user.email,
        "hashed_password": hashed_password,
        "role": user.role,
    }


@app.post("/token", response_model=models.Token)
def login_for_access_token(email: str, password: str):
    # Replace this with your actual user authentication logic
    user = {"email": email, "password": pwd_context.hash(password)}

    if not pwd_context.verify(password, user["password"]):
        raise HTTPException(status_code=401, detail="Incorrect email or password")

    access_token = jwt.encode({"sub": email}, "your-secret-key", algorithm="HS256")
    return {"access_token": access_token, "token_type": "bearer"}
