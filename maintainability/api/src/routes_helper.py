import base64
import json
import secrets
from pathlib import Path
from typing import Dict

from fastapi import HTTPException
from llm_blocks import block_factory
from passlib.context import CryptContext
from pydantic import ValidationError

from . import config, io_operations, logger, models

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_llm() -> callable:
    return block_factory.get(
        "template",
        template=config.PROMPT,
        temperature=config.TEMPERATURE,
        model_name=config.MODEL_NAME,
    )


def validate_response(response: str) -> Dict:
    try:
        data = json.loads(response)
        models.ValidModelResponse(**data)
        return data
    except (json.JSONDecodeError, ValidationError) as e:
        logger.logger(f"Invalid LLM response: {e}")
        return None


def get_maintainability_metrics(filepath: Path, code: str) -> models.ValidModelResponse:
    llm = get_llm()
    for _ in range(config.LLM_MAX_RETRIES):
        response = llm(filepath=filepath, code=code)
        validated_response = validate_response(response)
        if validated_response:
            return validated_response
    # else return default values
    return config.ValidModelResponse()


def extract_metrics(
    filepath: str, content: str, session_id: str
) -> models.Maintainability:
    file_size = len(content.encode("utf-8"))
    extension = filepath.split(".")[-1] if "." in filepath else ""
    loc = len(content.splitlines())
    maintainability_metrics = get_maintainability_metrics(filepath, content)
    io_operations.write_metrics(
        {
            "file_path": filepath,
            **maintainability_metrics,
            "file_size": file_size,
            "loc": loc,
            "extension": extension,
            "content": content,
            "session_id": session_id,
        }
    )
    return maintainability_metrics


def validate_user(email: str, password: str) -> None:
    user = io_operations.get_user(email)

    if not user or not pwd_context.verify(password, user["password"]):
        logger.logger(f"Unauthorized login attempt: email={email}")
        raise HTTPException(status_code=401, detail="Incorrect email or password")


def generate_new_api_key():
    random_bytes = secrets.token_bytes(32)
    return base64.urlsafe_b64encode(random_bytes).decode("utf-8").rstrip("=")
