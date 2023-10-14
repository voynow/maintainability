import json
import logging
import os
from pathlib import Path
from typing import Dict, Optional
import uuid

import click
import requests

from . import file_operations

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
options = {
    "paths": {
        "multiple": True,
        "type": click.Path(exists=True),
        "help": "List of relative filepaths",
        "default": ["."],
    },
    "base_url": {
        "type": str,
        "help": "Base API URL",
        "default": "https://maintainabilityapi.vercel.app",
    },
    "api_key": {
        "type": str,
        "help": "Registered API key for authentication",
        "required": True,
    },
}


def call_api_wrapper(
    base_url: str,
    endpoint: str,
    payload: Optional[Dict] = None,
    api_key: Optional[str] = None,
):
    """
    Wrapper for calling the API. Handles errors and logging

    :param endpoint: API endpoint to call
    :param payload: Payload to send to the API
    :return: Response from the API
    """
    url = f"{base_url}/{endpoint}"
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["X-API-KEY"] = api_key
    try:
        response = requests.post(
            url=url,
            json=payload,
            headers=headers,
        )
        response.raise_for_status()

    except requests.HTTPError as e:
        status_code = e.response.status_code
        response_content = e.response.content.decode("utf-8")

        try:
            detail = json.loads(response_content)["detail"]
        except json.JSONDecodeError:
            detail = response_content

        logger.error(
            f"HTTPError on {endpoint} with code={status_code}, Detail: {detail}"
        )
        raise requests.HTTPError(detail, response=e.response)

    except Exception as e:
        logger.error(f"Unexpected error when calling {endpoint}: {e}")
        raise e

    return response.json()


def extract_metrics(
    project_name: str,
    session_id: str,
    filepath: str,
    content: str,
    base_url: str,
    api_key: str,
) -> None:
    logger.info(f"{session_id} sending {filepath} to extract_metrics")
    response = call_api_wrapper(
        base_url=base_url,
        endpoint="extract_metrics",
        payload={
            "project_name": project_name,
            "session_id": session_id,
            "filepath": filepath,
            "file_content": content,
        },
        api_key=api_key,
    )
    logger.info(f"{session_id} extract_metrics response: {response}")


@click.command()
@click.option("--paths", **options["paths"])
@click.option("--base_url", **options["base_url"])
@click.option("--api_key", **options["api_key"])
def cli_runner(paths, base_url, api_key):
    session_id = str(uuid.uuid4())

    repo = file_operations.load_files()
    target_paths = [Path(path) for path in paths]
    filtered_repo = file_operations.filter_repo(repo, target_paths)
    project_name = os.path.basename(os.getcwd())

    logger.info(f"{session_id} starting extraction for {project_name}")
    for filepath, content in filtered_repo.items():
        extract_metrics(project_name, session_id, filepath, content, base_url, api_key)


if __name__ == "__main__":
    cli_runner()
