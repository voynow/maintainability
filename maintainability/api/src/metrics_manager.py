import json
from datetime import datetime
from pathlib import Path
from typing import Dict
from pydantic import ValidationError

from llm_blocks import block_factory

from . import config, io_operations, models

MAX_RETRIES = 3  # Maximum number of retries for LLM interaction


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
        return data
    except (json.JSONDecodeError, ValidationError) as e:
        io_operations.logger(f"Invalid LLM response: {e}", level="ERROR")
        return None


def get_maintainability_metrics(
    filepath: Path, code: str
) -> models.MaintainabilityMetrics:
    llm = get_llm()
    for attempt in range(MAX_RETRIES):
        io_operations.logger(f"LLM request: filepath={filepath}, code={code}")
        response = llm(filepath=filepath, code=code)
        io_operations.logger(f"LLM response: {response}")

        validated_response = validate_response(response)
        if validated_response:
            return models.MaintainabilityMetrics(**validated_response)

        io_operations.logger(f"Retry attempt {attempt+1} failed", level="WARNING")
    io_operations.logger("Max retries reached. Returning default metrics.")
    return models.MaintainabilityMetrics()


def get_file_metrics(filepath: Path, content: str) -> models.FileMetrics:
    file_size = len(content.encode("utf-8"))
    extension = filepath.split(".")[-1] if "." in filepath else ""
    loc = len(content.splitlines())
    return models.FileMetrics(
        file_size=file_size, loc=loc, extension=extension, content=content
    )


def compose_metrics(
    filepath: Path, code: str, session_id: str
) -> models.CompositeMetrics:
    maintainability_metrics = get_maintainability_metrics(filepath, code)
    file_metrics = get_file_metrics(filepath, code)
    return models.CompositeMetrics(
        maintainability=maintainability_metrics,
        file_info=file_metrics,
        timestamp=datetime.utcnow().isoformat(),
        session_id=session_id,
    )
