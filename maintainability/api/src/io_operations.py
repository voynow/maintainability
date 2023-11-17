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


def insert_file(file: models.File) -> Tuple:
    table = connect_to_supabase_table("files")
    return table.insert(file.model_dump()).execute()


def check_duplicate_project(user: str, github_username: str, github_repo: str) -> bool:
    table = connect_to_supabase_table("projects")
    response = (
        table.select("*")
        .eq("user", user)
        .eq("github_username", github_username)
        .eq("github_repo", github_repo)
        .execute()
    )
    return True if response.data else False


def insert_project(project: models.Project) -> Tuple:
    table = connect_to_supabase_table("projects")
    return table.insert(project.model_dump()).execute()


def list_projects(user_email: str) -> models.ProjectList:
    table = connect_to_supabase_table("projects")
    response = table.select("*").eq("user", user_email).execute()
    if not response.data:
        return {"projects": None}
    return models.ProjectList(projects=[models.Project(**row) for row in response.data])


def get_project(user_email: str, project_name: str) -> models.Project:
    table = connect_to_supabase_table("projects")
    response = (
        table.select("*").eq("user", user_email).eq("name", project_name).execute()
    )
    # centralized error handling will catch missing projects
    return models.Project(**response.data[0])


def set_favorite_project(user_email: str, project_name: str) -> Dict:
    table = connect_to_supabase_table("projects")

    # Set all projects to non-favorite
    resp = table.update({"favorite": False}).eq("user", user_email).execute()

    # Set the specified project as favorit
    resp = (
        table.update({"favorite": True})
        .eq("user", user_email)
        .eq("name", project_name)
        .execute()
    )

    return {"message": f"{project_name} set as favorite project"}


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
