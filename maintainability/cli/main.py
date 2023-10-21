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

    # TODO needs to be implemented
    # user_email = io_operations.get_email_via_api_key(
    #     request.headers.get("X-API-KEY", None)
    # )

    logger.info(f"{session_id} starting extraction for {project_name}")
    for filepath, content in filtered_repo.items():
        for metric in config.METRICS:
            response = call_api_wrapper(
                base_url=base_url,
                endpoint="extract_metrics",
                payload={
                    "filepath": filepath,
                    "file_content": content,
                    "metric": metric,
                },
                api_key=api_key,
            )

    # TODO
    # collect responses/aggregate scores
    # send to write_metrics endpoint

    # {
    #     "user_email": user_email,
    #     "project_name": project_name,
    #     "session_id": session_id,
    #     "file_path": filepath,
    #     "file_size": len(content.encode("utf-8")),
    #     "loc": len(content.splitlines()),
    #     "extension": filepath.split(".")[-1] if "." in filepath else "",
    #     "content": content,
    #     **maintainability_metrics,
    # }


if __name__ == "__main__":
    cli_runner()
