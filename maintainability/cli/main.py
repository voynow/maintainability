import json
import logging
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
        logger.info(f"Sending payload of {len(payload.keys())} files to {endpoint}")
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
    filtered_repo = file_operations.filter_repo_by_paths([Path(path) for path in paths])

    for filepath, content in filtered_repo.items():
        if len(content.splitlines()) < config.MIN_NUM_LINES:
            logger.info(
                f"Skipping {filepath} because it has less than {config.MIN_NUM_LINES} lines of code."
            )
            continue

        if filepath.startswith("test") or Path(filepath).stem.endswith("test"):
            logger.info(f"Skipping {filepath} because it is a test file.")
            continue

        try:
            logger.info(f"Processing {filepath}...")
            response = call_api_wrapper(
                base_url=base_url,
                endpoint="extract_metrics",
                payload={
                    "file_content": content,
                    "filepath": filepath,
                    "session_id": session_id,
                },
                api_key=api_key,
            )
            logger.info(f"Metrics submitted for {filepath}. Session ID: {session_id}")

        except Exception as e:
            logger.error(f"Error processing {filepath}: {e}")


if __name__ == "__main__":
    cli_runner()
