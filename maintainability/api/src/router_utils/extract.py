import base64
from datetime import datetime
import os
import re
import uuid

import requests
from fastapi import HTTPException
from llm_blocks import block_factory

from .. import config, io_operations, logger, models

GH_AUTH_TOKEN = os.environ.get("GH_AUTH_TOKEN")


def get_llm() -> callable:
    return block_factory.get(
        "template",
        template=config.PROMPT,
        temperature=config.TEMPERATURE,
        model_name=config.MODEL_NAME,
    )


def parse_response(text: str) -> float:
    try:
        match = re.search(r"(\d{1,2})/10", text)
        response = int(match.group(1))
    except AttributeError as e:
        logger.logger(f"Error parsing LLM response={text} with error={e}")
        response = -1
    return response


def extract_metrics(file_id: str, filepath: str, code: str, metric: str) -> int:
    gpt_interface = get_llm()
    description = config.METRIC_DESCRIPTIONS[metric]
    response = gpt_interface(
        filepath=filepath,
        code=code,
        metric=metric.replace("_", " "),
        description=description,
    )
    metric_quantity = int(parse_response(response))
    io_operations.write_metrics(
        file_id=file_id,
        metric=metric,
        metric_quantity=metric_quantity,
        reasoning=response,
    )
    return metric_quantity


def validate_github_project(
    user: str, github_username: str, github_repo: str
) -> models.ProjectStatus:
    url = f"https://api.github.com/repos/{github_username}/{github_repo}"
    response = requests.get(url)

    # Check that project exists on GitHub
    if response.status_code != 200:
        raise HTTPException(status_code=404, detail="GitHub project not found")

    # Check for active project in the database
    project_status: models.ProjectStatus = io_operations.get_project_status(
        user, github_username, github_repo
    )

    # raise error if project is active
    if project_status == models.ProjectStatus.ACTIVE:
        raise HTTPException(
            status_code=400, detail="Project already exists in the database"
        )

    return project_status


def insert_project(user, github_username, github_repo):
    project_status: models.ProjectStatus = validate_github_project(
        user, github_username, github_repo
    )
    if project_status == models.ProjectStatus.INACTIVE:
        return io_operations.mark_project_active(user, github_username, github_repo)
    elif project_status == models.ProjectStatus.NOT_FOUND:
        return io_operations.insert_project(
            models.Project(
                primary_id=uuid.uuid4(),
                name=github_repo,
                user=user,
                created_at=datetime.now(),
                github_username=github_username,
                is_active=True,
            )
        )
    else:
        raise HTTPException(
            status_code=400, detail="Invalid project status in the database"
        )


def delete_project(user, github_username, github_repo):
    """Mark project as inactive in the database"""
    project_status: models.ProjectStatus = io_operations.get_project_status(
        user, github_username, github_repo
    )
    if project_status == models.ProjectStatus.NOT_FOUND:
        raise HTTPException(status_code=404, detail="Project not found in the database")
    return io_operations.mark_project_inactive(user, github_username, github_repo)


def fetch_default_branch(user: str, repo: str) -> str:
    headers = {"Authorization": f"token {GH_AUTH_TOKEN}"}
    repo_info_url = f"https://api.github.com/repos/{user}/{repo}"

    resp = requests.get(repo_info_url, headers=headers)
    resp.raise_for_status()

    return resp.json().get("default_branch", "main")


def fetch_repo_structure(user: str, repo: str) -> list:
    default_branch = fetch_default_branch(user, repo)

    headers = {"Authorization": f"token {GH_AUTH_TOKEN}"}
    url = f"https://api.github.com/repos/{user}/{repo}/git/trees/{default_branch}?recursive=1"

    resp = requests.get(url, headers=headers)
    resp.raise_for_status()

    return [
        f["path"]
        for f in resp.json().get("tree", [])
        if f["type"] == "blob"
        and any(f["path"].endswith(ext) for ext in config.EXTENSIONS)
    ]


def fetch_file_content(user: str, repo: str, path: str) -> str:
    headers = {"Authorization": f"token {GH_AUTH_TOKEN}"}
    file_url = f"https://api.github.com/repos/{user}/{repo}/contents/{path}"
    file_resp = requests.get(file_url, headers=headers)
    file_resp.raise_for_status()
    return base64.b64decode(file_resp.json()["content"]).decode("utf-8")


#
# file_paths = fetch_repo_structure(user, repo)

# repodata = {}
# for path in file_paths:
#     file_url = f"https://api.github.com/repos/{user}/{repo}/contents/{path}"
#     file_content = fetch_file_content(file_url, headers)
#     repodata[path] = file_content

# return repodata
