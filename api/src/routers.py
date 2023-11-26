from datetime import datetime
from pathlib import Path
from typing import Dict

from fastapi import APIRouter
from .router_utils import analytics, extract

from . import io_operations, models, logger

router = APIRouter()


@router.get("/health")
def read_root():
    """Health check endpoint"""
    return {"status": "ok"}


@router.post("/insert_project")
async def insert_project(user: str, github_username: str, github_repo: str):
    """Insert project into database"""
    return extract.insert_project(user, github_username, github_repo)


@router.post("/delete_project")
async def delete_project(user: str, github_username: str, github_repo: str):
    """Mark project as inactive"""
    return extract.delete_project(user, github_username, github_repo)


@router.get("/fetch_repo_structure")
async def fetch_repo_structure(user: str, repo: str):
    return extract.fetch_repo_structure(user, repo)


@router.get("/fetch_file_content")
async def fetch_file_content(user: str, repo: str, path: str):
    return extract.fetch_file_content(user, repo, path)


@router.post("/check_file_criteria")
async def check_file_criteria(file_path: str, extension: str, line_count: int):
    """Check if a file meets the criteria for analysis"""
    return extract.check_file_criteria(file_path, extension, line_count)


@router.post("/insert_file")
async def insert_file(file: models.File):
    """Database proxy for inserting a file into the file table"""
    return io_operations.insert_file(file)


@router.get("/get_metrics_config")
async def get_metrics_config():
    """Interface to retirve metrics configuration"""
    return extract.get_metrics_config()


@router.post("/extract_metrics")
async def extract_metrics(transaction: models.ExtractMetricsTransaction):
    """Extract some metrics from a single file of code"""
    return extract.extract_metrics(transaction)


@router.get("/list_projects", response_model=models.ProjectList)
async def list_projects(user_email: str):
    """Database proxy for listing all active projects for a user"""
    return io_operations.list_projects(user_email)


@router.post("/set_favorite_project")
async def set_favorite_project(request: models.FavoriteProjectRequest):
    return io_operations.set_favorite_project(request.user_email, request.project_name)


@router.get("/get_metrics")
async def get_metrics(user_email: str, project_name: str):
    """DB connector and analytics engine for project metrics"""
    return analytics.get_metrics(user_email, project_name)
