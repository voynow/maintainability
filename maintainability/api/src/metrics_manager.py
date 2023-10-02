import json
import os
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, Tuple

from llm_blocks import block_factory
from supabase import Client, create_client

from . import config, models


def get_maintainability_metrics(
    filepath: Path, code: str
) -> models.MaintainabilityMetrics:
    print("metrics_manager.py: get_maintainability_metrics()")
    llm = block_factory.get(
        "template",
        template=config.PROMPT,
        temperature=config.TEMPERATURE,
        model_name=config.MODEL_NAME,
    )
    print("metrics_manager.py: get_maintainability_metrics() Calling llm()")
    response = llm(filepath=filepath, code=code)
    print("metrics_manager.py: get_maintainability_metrics() llm() returned")
    return models.MaintainabilityMetrics(**json.loads(response))


def get_file_metrics(filepath: Path, content: str) -> models.FileMetrics:
    print("metrics_manager.py: get_file_metrics()")
    file_size = len(content.encode("utf-8"))
    language = filepath.suffix.lstrip(".")
    loc = len(content.splitlines())
    print("metrics_manager.py: get_file_metrics() returning")
    return models.FileMetrics(
        file_size=file_size, loc=loc, language=language, content=content
    )


def compose_metrics(
    filepath: Path, code: str, session_id: str
) -> models.CompositeMetrics:
    print("metrics_manager.py: compose_metrics()")
    maintainability_metrics = get_maintainability_metrics(filepath, code)
    file_metrics = get_file_metrics(filepath, code)
    print("metrics_manager.py: compose_metrics() returning")
    return models.CompositeMetrics(
        maintainability=maintainability_metrics,
        file_info=file_metrics,
        timestamp=datetime.utcnow().isoformat(),
        session_id=session_id,
    )


def connect_to_supabase() -> Client:
    """Connect to Supabase database"""
    return create_client(
        os.environ.get("SUPABASE_URL"),
        os.environ.get("SUPABASE_KEY"),
    )


def write_metrics(metrics: Dict[str, models.CompositeMetrics]) -> Tuple:
    insert_data = [
        {
            "primary_id": str(uuid.uuid4()),
            "file_path": filepath,
            "readability": metrics.maintainability.readability,
            "design_quality": metrics.maintainability.design_quality,
            "testability": metrics.maintainability.testability,
            "consistency": metrics.maintainability.consistency,
            "debug_error_handling": metrics.maintainability.debug_error_handling,
            "file_size": metrics.file_info.file_size,
            "language": metrics.file_info.language,
            "loc": metrics.file_info.loc,
            "content": metrics.file_info.content,
            "timestamp": metrics.timestamp,
            "session_id": metrics.session_id,
        }
        for filepath, metrics in metrics.items()
    ]
    table = connect_to_supabase().table("maintainability")
    return table.insert(insert_data).execute()
