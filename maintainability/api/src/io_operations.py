import os
from datetime import datetime
from typing import Dict, List, Tuple
from uuid import UUID

from fastapi import HTTPException
from supabase import Client, create_client

from . import models


def connect_to_supabase_table(table_name: str) -> Client:
    return create_client(
        os.environ.get("SUPABASE_URL"),
        os.environ.get("SUPABASE_KEY"),
    ).table(table_name)


def write_metrics(
    file_id: str,
    metric: str,
    metric_quantity: int,
    reasoning: str,
) -> Tuple:
    table = connect_to_supabase_table("metrics")
    return table.insert(
        {
            "file_id": file_id,
            "metric": metric,
            "reasoning": reasoning,
            "score": metric_quantity,
        }
    ).execute()


def write_file(file: models.File) -> Tuple:
    table = connect_to_supabase_table("files")
    return table.insert(file.model_dump()).execute()


def get_user_projects(user_email: str) -> List[Dict]:
    table = connect_to_supabase_table("files")
    response = table.select("project_name").eq("user_email", user_email).execute()
    if not response.data:
        return []
    unique_projects = list(set([obj["project_name"] for obj in response.data]))
    return [{"project_name": name} for name in unique_projects]


def get_files(user_email: str, project_name: str) -> Dict[UUID, models.File]:
    table = connect_to_supabase_table("files")
    rows = (
        table.select("*")
        .eq("user_email", user_email)
        .eq("project_name", project_name)
        .execute()
        .data
    )
    files = [models.File(**row) for row in rows]
    return {file.file_id: file for file in files}


def get_metrics(file_ids: List[UUID]) -> List[models.Metric]:
    table = connect_to_supabase_table("metrics")
    rows = table.select("*").in_("file_id", file_ids).execute().data
    metrics = [models.Metric(**row) for row in rows]
    return metrics


def write_user(email: str, hashed_password: str, role: str = "user") -> Tuple:
    user_data = {"email": email, "password": hashed_password, "role": role}
    table = connect_to_supabase_table("users")
    return table.insert(user_data).execute()


# TODO depricate this function
# def get_user(email: str) -> Dict:
#     table = connect_to_supabase_table("users")
#     response = table.select("email, password, role").eq("email", email).execute()

#     if response.data:
#         return response.data[0]
#     return None


def select_api_key(api_key: str) -> Dict:
    table = connect_to_supabase_table("api_keys")
    response = table.select("api_key").eq('"api_key"', api_key).execute()
    return response.data


def validate_api_key(api_key: str) -> bool:
    if not select_api_key(api_key):
        raise HTTPException(status_code=401, detail="Unauthorized: Invalid API key.")


def write_api_key(
    api_key: str, user: str, name: str, creation_date: datetime, status: str
) -> Tuple:
    api_key_data = {
        "api_key": api_key,
        "user": user,
        "name": name,
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
    validate_api_key(api_key)
    table = connect_to_supabase_table("api_keys")
    return table.update({"status": "deleted"}).eq('"api_key"', api_key).execute()


def write_log(loc: str, text: str, session_id: str) -> Tuple:
    log_data = {"loc": loc, "text": text, "session_id": session_id}
    table = connect_to_supabase_table("logs")
    return table.insert(log_data).execute()


def get_user_email(api_key: str) -> str:
    validate_api_key(api_key)
    table = connect_to_supabase_table("api_keys")
    response = table.select("user").eq('"api_key"', api_key).execute()
    return response.data[0]["user"]
