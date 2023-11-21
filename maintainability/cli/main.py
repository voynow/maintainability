import json
import logging
import os
import uuid
from datetime import datetime
from functools import partial
from pathlib import Path
from typing import Dict, Optional

import click
import requests
from retrying import retry

from . import config, file_operations

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


def build_headers(api_key: Optional[str] = None) -> Dict[str, str]:
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["X-API-KEY"] = api_key
    return headers


def handle_http_error(endpoint: str, err: requests.HTTPError):
    status_code = err.response.status_code
    response_content = err.response.content.decode("utf-8")
    if status_code == 504:
        logger.error(f"Timeout when calling {endpoint}, retrying...")
        raise err
    else:
        try:
            detail = json.loads(response_content)["detail"]
        except json.JSONDecodeError:
            detail = response_content
        logger.error(f"HTTPError with code={status_code}, Detail: {detail}")
        raise requests.HTTPError(detail, response=err.response)


def response_validator(response: requests.Response, endpoint: str) -> requests.Response:
    try:
        response.raise_for_status()
        response.json()
    except requests.HTTPError as err:
        handle_http_error(endpoint, err)
    except json.JSONDecodeError:
        logger.error(f"Response is not valid JSON: {response.content}")
        raise json.JSONDecodeError
    except Exception as e:
        logger.error(f"Unexpected error when calling {endpoint}: {e}")
        raise err

    return response


@retry(stop_max_attempt_number=3, wait_fixed=2000)
def call_api_wrapper(
    base_url: str,
    endpoint: str,
    method: str = "POST",
    payload: Optional[Dict] = None,
    api_key: Optional[str] = None,
):
    url = f"{base_url}/{endpoint}"
    headers = build_headers(api_key)
    request_map = {
        "POST": partial(requests.post, url=url, json=payload, headers=headers),
        "GET": partial(requests.get, url=url, params=payload, headers=headers),
    }
    send_request = request_map[method]
    response = response_validator(send_request(), endpoint)
    return response.json()


def extract_metrics_wrapper(
    base_url: str,
    file_id: str,
    session_id: str,
    file_path: str,
    content: str,
    api_key: str,
) -> Dict:
    maintainability_metrics = {}
    for metric_name in config.METRICS:
        logger.info(f"Extracting {file_path}:{metric_name}")
        response = call_api_wrapper(
            base_url=base_url,
            endpoint="extract_metrics",
            payload={
                "file_id": file_id,
                "session_id": session_id,
                "file_path": file_path,
                "content": content,
                "metric_name": metric_name,
            },
            api_key=api_key,
        )
        maintainability_metrics[metric_name] = response
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
    for file_path, content in filtered_repo.items():
        file_id = str(uuid.uuid4())
        timestamp = datetime.now().isoformat()

        # insert file into file table
        call_api_wrapper(
            base_url=base_url,
            endpoint="insert_file",
            payload={
                "file_id": file_id,
                "user_email": user_email,
                "project_name": project_name,
                "session_id": session_id,
                "file_path": file_path,
                "file_size": len(content.encode("utf-8")),
                "loc": len(content.splitlines()),
                "extension": file_path.split(".")[-1] if "." in file_path else "",
                "content": content,
                "timestamp": timestamp,
            },
            api_key=api_key,
        )

        # extract metrics from file and insert into metrics table
        maintainability_metrics = extract_metrics_wrapper(
            base_url=base_url,
            file_id=file_id,
            session_id=session_id,
            file_path=file_path,
            content=content,
            api_key=api_key,
        )

        logger.info(f"Inserted {file_path}")


if __name__ == "__main__":
    cli_runner()
