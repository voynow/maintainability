import os
from datetime import datetime
from typing import Dict

import jwt
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from . import io_operations, logger, models, routes_helper

router = APIRouter()


@router.get("/health")
def read_root():
    return {"status": "ok"}


@router.post("/extract_metrics")
async def extract_metrics(extract_metrics_obj: models.ExtractMetrics):
    return routes_helper.extract_metrics(
        file_id=extract_metrics_obj.file_id,
        filepath=extract_metrics_obj.filepath,
        code=extract_metrics_obj.file_content,
        metric=extract_metrics_obj.metric,
    )


@router.post("/insert_file")
async def insert_metrics(file: models.FileTransaction):
    return io_operations.write_file(file)


@router.get("/get_user_email")
async def get_user_email(api_key: str):
    response = io_operations.get_user_email(api_key)
    if response is None:
        raise HTTPException(status_code=404, detail="User not found")
    return response


@router.get("/get_user_projects")
async def get_user_projects(user_email: str):
    projects = io_operations.get_user_projects(user_email)
    if not projects:
        return JSONResponse(status_code=404, content={"detail": "Projects not found"})
    return projects


@router.get("/get_metrics")
async def get_metrics(user_email: str, project_name: str):
    files_metrics = routes_helper.join_files_metrics(user_email, project_name)
    weighted_metrics = routes_helper.calculate_weighted_metrics(files_metrics)
    plot_json = routes_helper.generate_plotly_figs(weighted_metrics)
    return plot_json


@router.post("/generate_key")
async def generate_key(new_key: Dict[str, str]):
    api_key = routes_helper.generate_new_api_key()
    while io_operations.api_key_exists(api_key):
        api_key = routes_helper.generate_new_api_key()

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
    api_keys = io_operations.list_api_keys(email)
    return {"api_keys": api_keys}


@router.delete("/api_keys/{api_key}")
async def remove_api_key(api_key: str):
    if io_operations.api_key_exists(api_key):
        io_operations.delete_api_key(api_key)
        return {"message": "API key deleted successfully"}
    else:
        logger.logger("Error 404: API key not found")
        return {"message": "API key not found"}, 404
