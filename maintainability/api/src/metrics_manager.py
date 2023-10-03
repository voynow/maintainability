import json
from datetime import datetime
from pathlib import Path

from llm_blocks import block_factory

from . import config, io_operations, models


def get_maintainability_metrics(
    filepath: Path, code: str
) -> models.MaintainabilityMetrics:
    llm = block_factory.get(
        "template",
        template=config.PROMPT,
        temperature=config.TEMPERATURE,
        model_name=config.MODEL_NAME,
    )
    io_operations.logger(f"LLM request: filepath={filepath}, code={code}")
    response = llm(filepath=filepath, code=code)
    io_operations.logger(f"LLM response: {response}")
    return models.MaintainabilityMetrics(**json.loads(response))


def get_file_metrics(filepath: Path, content: str) -> models.FileMetrics:
    file_size = len(content.encode("utf-8"))
    language = filepath.suffix.lstrip(".")
    loc = len(content.splitlines())
    return models.FileMetrics(
        file_size=file_size, loc=loc, language=language, content=content
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
