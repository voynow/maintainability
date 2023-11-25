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


def write_metric(metric: models.Metric) -> Tuple:
    table = connect_to_supabase_table("metrics")
    return table.insert(metric.model_dump()).execute()


def insert_file(file: models.File) -> Tuple:
    table = connect_to_supabase_table("files")
    return table.insert(file.model_dump()).execute()


def get_project_status(
    user: str, github_username: str, github_repo: str
) -> models.ProjectStatus:
    """
    Check for duplicates in the database, return True if project exists and is
    active, False otherwise
    """
    table = connect_to_supabase_table("projects")
    response = (
        table.select("is_active")
        .eq("user", user)
        .eq("github_username", github_username)
        .eq("name", github_repo)
        .execute()
    )

    if response.data:
        active_status_map = {
            True: models.ProjectStatus.ACTIVE,
            False: models.ProjectStatus.INACTIVE,
        }
        is_active = response.data[0]["is_active"]
        return active_status_map[is_active]
    else:
        return models.ProjectStatus.NOT_FOUND


def insert_project(project: models.Project) -> Tuple:
    table = connect_to_supabase_table("projects")
    project.primary_id = str(project.primary_id)
    project.created_at = project.created_at.isoformat()
    return table.insert(project.model_dump()).execute()


def mark_project_active(user: str, github_username: str, github_repo: str):
    table = connect_to_supabase_table("projects")
    return (
        table.update({"is_active": True})
        .eq("user", user)
        .eq("github_username", github_username)
        .eq("name", github_repo)
        .execute()
    )


def mark_project_inactive(user: str, github_username: str, github_repo: str):
    table = connect_to_supabase_table("projects")
    return (
        table.update({"is_active": False})
        .eq("user", user)
        .eq("github_username", github_username)
        .eq("name", github_repo)
        .execute()
    )


def delete_project_for_testing(user: str, github_username: str, github_repo: str):
    table = connect_to_supabase_table("projects")
    return (
        table.delete()
        .match({"user": user, "github_username": github_username, "name": github_repo})
        .execute()
    )


def list_projects(user_email: str) -> models.ProjectList:
    """Select all projects for some user where is_active is True"""
    table = connect_to_supabase_table("projects")
    response = table.select("*").eq("user", user_email).eq("is_active", True).execute()
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
