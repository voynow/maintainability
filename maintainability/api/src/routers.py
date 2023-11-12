from datetime import datetime
from typing import Dict

from fastapi import APIRouter

from . import io_operations, models, llm, github, user, analytics

router = APIRouter()


@router.get("/health")
def read_root():
    """Health check endpoint"""
    return {"status": "ok"}


@router.post("/extract_metrics")
async def extract_metrics(extract_metrics_obj: models.ExtractMetrics):
    """Extract some metrics from a single file of code"""
    return llm.extract_metrics(
        file_id=extract_metrics_obj.file_id,
        filepath=extract_metrics_obj.filepath,
        code=extract_metrics_obj.file_content,
        metric=extract_metrics_obj.metric,
    )


@router.post("/insert_file")
async def insert_file(file: models.File):
    """Database proxy for inserting a file into the file table"""
    return io_operations.write_file(file)


@router.get("/get_user_email")
async def get_user_email(api_key: str):
    """Database proxy for getting user email given api key"""
    return io_operations.get_user_email(api_key)


@router.get("/get_user_projects")
async def get_user_projects(user_email: str):
    """Database proxy for getting user projects given email"""
    return io_operations.get_user_projects(user_email)


@router.post("/generate_key")
async def generate_key(new_key: Dict[str, str]):
    """Allows users to generate new API keys"""
    api_key = user.generate_api_key_helper()

    io_operations.write_api_key(
        api_key=api_key,
        user=new_key["email"],
        name=new_key["name"],
        creation_date=datetime.utcnow().isoformat(),
        status="active",
    )
    return {"api_key": api_key}


@router.get("/api_keys")
async def list_api_keys(email: str):
    """Used for displaying all API keys associated with a user"""
    api_keys = io_operations.list_api_keys(email)
    return {"api_keys": api_keys}


@router.delete("/api_keys/{api_key}")
async def remove_api_key(api_key: str):
    """Allows users to delete API keys"""
    io_operations.delete_api_key(api_key)
    return {"message": "API key deleted successfully"}


@router.get("/get_metrics")
async def get_metrics(user_email: str, project_name: str):
    """DB connector and analytics engine for project metrics"""
    return analytics.get_metrics(user_email, project_name)


@router.get("/fetch_repo_structure")
def fetch_repo_structure(user: str, repo: str, branch: str = "main"):
    return github.fetch_repo_structure(user, repo, branch)


@router.get("/fetch_file_content")
def fetch_file_content(user: str, repo: str, path: str):
    return github.fetch_file_content(user, repo, path)
