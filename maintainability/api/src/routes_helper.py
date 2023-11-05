import base64
import re
import secrets
from typing import Any, Callable, List

import plotly.graph_objects as go
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from llm_blocks import block_factory
from passlib.context import CryptContext

from . import analytics, config, io_operations, logger

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


def extract_metrics(file_id: str, filepath: str, code: str, metric: str) -> int:
    gpt_interface = get_llm()
    description = config.METRIC_DESCRIPTIONS[metric]
    response = gpt_interface(
        filepath=filepath,
        code=code,
        metric=metric.replace("_", " "),
        description=description,
    )
    metric_quantity = int(parse_response(response))
    io_operations.write_metrics(
        file_id=file_id,
        metric=metric,
        metric_quantity=metric_quantity,
        reasoning=response,
    )
    return metric_quantity


def validate_user(email: str, password: str) -> None:
    user = io_operations.get_user(email)

    if not user or not pwd_context.verify(password, user["password"]):
        logger.logger(f"Unauthorized login attempt: email={email}")
        raise HTTPException(status_code=401, detail="Incorrect email or password")


def generate_new_api_key():
    random_bytes = secrets.token_bytes(32)
    return base64.urlsafe_b64encode(random_bytes).decode("utf-8").rstrip("=")


def generate_api_key_helper():
    api_key = generate_new_api_key()
    while io_operations.select_api_key(api_key):
        api_key = generate_new_api_key()
    return api_key


def batch_process(
    items: List[Any],
    proccess_function: Callable,
    batch_size: int = 100,
    *args,
    **kwargs,
):
    """Generically applies a function to a list of items in batches"""
    results = []
    for i in range(0, len(items), batch_size):
        batch = items[i : i + batch_size]
        result = proccess_function(batch, *args, **kwargs)
        results.extend(result)
    return results


def get_metrics(user_email: str, project_name: str):
    """
    query database for all files associated with the project, join data between
    files and metrics tables, calculate weighted metrics, and generate plotly
    """
    files = io_operations.get_files(user_email, project_name)
    metrics = batch_process(list(files), io_operations.get_metrics)

    files_metrics = analytics.join_files_metrics(metrics, files)
    grouped_metrics = analytics.group_metrics(files_metrics)
    weighted_metrics = analytics.calculate_weighted_metrics(grouped_metrics)
    plot_json = analytics.generate_plotly_figs(weighted_metrics)
    enriched_plot = analytics.enrich_description(plot_json)

    return enriched_plot
