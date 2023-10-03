import json
import logging
from pathlib import Path
from typing import Dict, Optional

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
        "default": "https://maintainability.vercel.app",
    },
}


def call_api_wrapper(base_url: str, endpoint: str, payload: Optional[Dict] = None):
    """
    Wrapper for calling the API. Handles errors and logging

    :param endpoint: API endpoint to call
    :param payload: Payload to send to the API
    :return: Response from the API
    """
    url = f"{base_url}/{endpoint}"
    try:
        logger.info(f"Sending payload of {len(payload.keys())} files to {endpoint}")
        response = requests.post(
            url=url,
            json=payload,
            headers={"Content-Type": "application/json"},
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
def cli_runner(paths, base_url):
    filtered_repo = file_operations.filter_repo_by_paths([Path(path) for path in paths])
    extracted_metrics = call_api_wrapper(
        base_url=base_url, endpoint="extract_metrics", payload=filtered_repo
    )
    submit_metrics = call_api_wrapper(
        base_url=base_url, endpoint="submit_metrics", payload=extracted_metrics
    )
    logger.info(f"SUCCESS: {submit_metrics}")


if __name__ == "__main__":
    cli_runner()
