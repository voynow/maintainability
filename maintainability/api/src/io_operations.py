import os
import uuid
from datetime import datetime
from typing import Dict, Tuple

from pytz import utc
from supabase import Client, create_client

from . import models


def logger(log: str, level: str = "INFO", max_length: int = 250) -> None:
    """Vercel serverless does not support logging, here we use print instead"""
    truncated_log = log if len(log) <= max_length else log[:max_length] + "..."
    timestamp = datetime.now(utc).isoformat()
    print(f"{timestamp} [{level}]: {truncated_log}")  # noqa: T001


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
            "extension": metrics.file_info.extension,
            "loc": metrics.file_info.loc,
            "content": metrics.file_info.content,
            "timestamp": metrics.timestamp,
            "session_id": metrics.session_id,
        }
        for filepath, metrics in metrics.items()
    ]
    table = connect_to_supabase().table("maintainability")
    return table.insert(insert_data).execute()
