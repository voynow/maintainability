import base64
import secrets
import uuid
from pathlib import Path
from typing import Dict

from fastapi.responses import JSONResponse
from passlib.context import CryptContext

from . import config, io_operations, metrics_manager, models

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


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


def validate_user(email: str, password: str) -> None:
    user = io_operations.get_user(email)

    if not user or not pwd_context.verify(password, user["password"]):
        io_operations.logger.warning(f"Unauthorized login attempt: email={email}")
        return JSONResponse(
            status_code=401, content={"detail": "Incorrect email or password"}
        )


def generate_new_api_key():
    random_bytes = secrets.token_bytes(32)
    return base64.urlsafe_b64encode(random_bytes).decode("utf-8").rstrip("=")
