import os
import uuid
from datetime import datetime
from typing import Dict, Tuple, List

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


def connect_to_supabase_table(table_name: str) -> Client:
    return create_client(
        os.environ.get("SUPABASE_URL"),
        os.environ.get("SUPABASE_KEY"),
    ).table(table_name)


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
    table = connect_to_supabase_table("maintainability")
    return table.insert(insert_data).execute()


def write_user(email: str, hashed_password: str, role: str = "user") -> Tuple:
    user_data = {"email": email, "password": hashed_password, "role": role}
    table = connect_to_supabase_table("users")
    return table.insert(user_data).execute()


def get_user(email: str) -> Dict:
    table = connect_to_supabase_table("users")
    response = table.select("email, password, role").eq("email", email).execute()

    if response.data:
        return response.data[0]
    return None


def api_key_exists(api_key: str) -> bool:
    table = connect_to_supabase_table("api_keys")
    response = table.select("api_key").eq('"api_key"', api_key).execute()

    if response.data:
        return True
    return False


def write_api_key(
    api_key: str, user: str, creation_date: datetime, status: str
) -> Tuple:
    api_key_data = {
        "api_key": api_key,
        "user": user,
        "creation_date": creation_date,
        "status": status,
    }
    table = connect_to_supabase_table("api_keys")
    return table.insert(api_key_data).execute()


def list_api_keys(email: str) -> List[Dict]:
    table = connect_to_supabase_table("api_keys")
    response = table.select("*").eq("user", email).eq("status", "active").execute()

    return response.data if response.data else []


def delete_api_key(api_key: str) -> None:
    table = connect_to_supabase_table("api_keys")
    return table.update({"status": "deleted"}).eq('"api_key"', api_key).execute()
