import json
import logging
import os
from pathlib import Path
from typing import Dict, Optional
import uuid

import click
import requests

from . import file_operations, config

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
    method: str = "POST",
    payload: Optional[Dict] = None,
    api_key: Optional[str] = None,
):
    """
    Wrapper for calling the API. Handles errors and logging.

    :param base_url: The base URL for the API
    :param endpoint: The API endpoint to call
    :param method: The HTTP method to use (GET or POST)
    :param payload: The payload sent to the API
    :param api_key: The API key for authentication
    :return: The response from the API
    """
    url = f"{base_url}/{endpoint}"
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["X-API-KEY"] = api_key

    try:
        if method == "POST":
            response = requests.post(url, json=payload, headers=headers)
        elif method == "GET":
            response = requests.get(url, params=payload, headers=headers)
        else:
            raise ValueError(f"Unsupported method: {method}")

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


def extract_metrics_wrapper(
    base_url: str, file_id: str, filepath: str, content: str, api_key: str
) -> Dict:
    maintainability_metrics = {}
    for metric in config.METRICS:
        logger.info(f"Extracting {filepath}:{metric}")
        response = call_api_wrapper(
            base_url=base_url,
            endpoint="extract_metrics",
            payload={
                "file_id": file_id,
                "filepath": filepath,
                "file_content": content,
                "metric": metric,
            },
            api_key=api_key,
        )
        maintainability_metrics[metric] = response
    return maintainability_metrics


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

    user_email = call_api_wrapper(
        base_url=base_url,
        endpoint="get_user_email",
        payload={"api_key": api_key},
        api_key=api_key,
        method="GET",
    )

    logger.info(f"Starting extraction for {user_email}:{project_name}")
    for filepath, content in filtered_repo.items():
        file_id = str(uuid.uuid4())

        # insert file into file table
        call_api_wrapper(
            base_url=base_url,
            endpoint="insert_file",
            payload={
                "file_id": file_id,
                "user_email": user_email,
                "project_name": project_name,
                "session_id": session_id,
                "file_path": filepath,
                "file_size": len(content.encode("utf-8")),
                "loc": len(content.splitlines()),
                "extension": filepath.split(".")[-1] if "." in filepath else "",
                "content": content,
            },
            api_key=api_key,
        )

        # extract metrics from file and insert into metrics table
        maintainability_metrics = extract_metrics_wrapper(
            base_url=base_url,
            file_id=file_id,
            filepath=filepath,
            content=content,
            api_key=api_key,
        )

        logger.info(f"Inserted {filepath}, metrics={maintainability_metrics}")


if __name__ == "__main__":
    cli_runner()
