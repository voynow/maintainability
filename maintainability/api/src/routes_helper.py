import base64
import json
import secrets
from collections import defaultdict
from pathlib import Path
from typing import Dict

from dateutil.parser import parse
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


def get_maintainability_metrics(filepath: Path, code: str) -> models.ValidModelResponse:
    metric_collection = {}
    gpt_3_5_turbo = get_llm()
    for metric, description in config.METRIC_DESCRIPTIONS.items():
        metric_collection[metric] = gpt_3_5_turbo(
            filepath=filepath, code=code, metric_description=description
        )
        print(metric_collection[metric])
    return metric_collection


def extract_metrics(
    user_email: str, project_name: str, session_id: str, filepath: str, content: str
) -> models.Maintainability:
    maintainability_metrics = get_maintainability_metrics(filepath, content)
    io_operations.write_metrics(
        {
            "user_email": user_email,
            "project_name": project_name,
            "session_id": session_id,
            "file_path": filepath,
            "file_size": len(content.encode("utf-8")),
            "loc": len(content.splitlines()),
            "extension": filepath.split(".")[-1] if "." in filepath else "",
            "content": content,
            **maintainability_metrics,
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


def calculate_weighted_metrics(response_data):
    def aggregate_scores(objs):
        filtered_objs = list(
            filter(lambda obj: all(obj[col] != -1 for col in config.METRIC_COLS), objs)
        )
        total_loc = sum(obj["loc"] for obj in filtered_objs)

        if total_loc == 0:
            return {col: -1 for col in config.METRIC_COLS}

        return {
            col: sum(obj[col] * (obj["loc"] / total_loc) for obj in filtered_objs)
            for col in config.METRIC_COLS
        }

    dates = defaultdict(list)

    for obj in response_data:
        date_str = parse(obj["timestamp"]).strftime("%Y-%m-%d")
        dates[date_str].append(obj)

    return {date: aggregate_scores(objs) for date, objs in dates.items()}
