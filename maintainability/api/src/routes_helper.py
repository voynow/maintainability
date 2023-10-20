import base64
import secrets
from collections import defaultdict
import re

from dateutil.parser import parse
from fastapi import HTTPException
from llm_blocks import block_factory
from passlib.context import CryptContext

from . import config, io_operations, logger, models

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_llm() -> callable:
    return block_factory.get(
        "template",
        template=config.PROMPT,
        temperature=config.TEMPERATURE,
        model_name=config.MODEL_NAME,
    )


def parse_response(text: str) -> float:
    try:
        match = re.search(r"(\d{1,2})/10", text)
        response = int(match.group(1))
    except AttributeError as e:
        logger.logger(f"Error parsing LLM response={text} with error={e}")
        response = -1
    return response


def get_maintainability_metrics(
    filepath: str, code: str
) -> models.MaintainabilityMetrics:
    metric_collection = {}
    gpt_interface = get_llm()
    for metric, description in config.METRIC_DESCRIPTIONS.items():
        response = gpt_interface(
            filepath=filepath, code=code, metric_description=description
        )
        metric_collection[metric] = parse_response(response)
    return metric_collection


def extract_metrics(
    user_email: str, project_name: str, session_id: str, filepath: str, content: str
) -> models.ExtractMetricsTransaction:
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
            filter(
                lambda obj: all(obj[col] != -1 for col in config.METRIC_DESCRIPTIONS),
                objs,
            )
        )
        total_loc = sum(obj["loc"] for obj in filtered_objs)

        if total_loc == 0:
            return {col: -1 for col in config.METRIC_DESCRIPTIONS}

        return {
            col: sum(obj[col] * (obj["loc"] / total_loc) for obj in filtered_objs)
            for col in config.METRIC_DESCRIPTIONS
        }

    dates = defaultdict(list)

    for obj in response_data:
        date_str = parse(obj["timestamp"]).strftime("%Y-%m-%d")
        dates[date_str].append(obj)

    return {date: aggregate_scores(objs) for date, objs in dates.items()}
