import json
import logging
import os
from pathlib import Path
from typing import Dict, Optional

import click
import requests

from . import file_operations

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
options = {
    "multiple": True,
    "type": click.Path(exists=True),
    "help": "List of paths to analyze",
    "default": ["."],
}

API_URL = os.environ.get("API_URL", "https://maintainability.vercel.app/")


def call_api(endpoint: str, payload: Optional[Dict] = None):
    response = requests.post(
        f"https://maintainability.vercel.app/{endpoint}",
        json=payload,
        headers={"Content-Type": "application/json"},
    )
    response.raise_for_status()
    return response.json()


def call_api_wrapper(endpoint: str, payload: Optional[Dict] = None):
    """
    Wrapper for calling the API. Handles errors and logging

    :param endpoint: API endpoint to call
    :param payload: Payload to send to the API
    :return: Response from the API
    """
    try:
        response = call_api(endpoint, payload)

    except requests.HTTPError as e:
        logger.error(
            f"HTTPError on {endpoint} with code={e.response.status_code}, Response: {e.response.content}"
        )
        raise requests.HTTPError(json.loads(e.response.content)["detail"])

    except Exception as e:
        logger.error(f"Unexpected error when calling {endpoint}: {e}")
        raise e

    return response


@click.command()
@click.option("--paths", **options)
def cli_runner(paths):
    filtered_repo = file_operations.filter_repo_by_paths([Path(path) for path in paths])
    extracted_metrics = call_api_wrapper(
        endpoint="extract_metrics", payload=filtered_repo
    )
    submit_metrics = call_api_wrapper(
        endpoint="submit_metrics", payload=extracted_metrics
    )
    logger.info(f"SUCCESS: {submit_metrics}")


if __name__ == "__main__":
    cli_runner()
