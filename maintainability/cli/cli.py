import logging
from pathlib import Path
from typing import Dict, Optional

import click
import requests

from maintainability.api.src import utils

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
options = {
    "multiple": True,
    "type": click.Path(exists=True),
    "help": "List of paths to analyze",
    "default": ["."],
}


def call_api(endpoint: str, payload: Optional[Dict] = None):
    response = requests.post(
        f"https://maintainability.vercel.app/{endpoint}",
        json=payload,
        headers={"Content-Type": "application/json"},
    )
    response.raise_for_status()
    return response.json()


def call_api_wrapper(endpoint: str, payload: Optional[Dict] = None):
    try:
        logger.info(f"Initiating API call to {endpoint} with payload: {payload}")
        response = call_api(endpoint, payload)
        logger.info(f"Received successful response from {endpoint}")
    except requests.HTTPError as e:
        logger.error(
            f"HTTPError when calling {endpoint}. Status code: {e.response.status_code}, Response: {e.response.content}"
        )
        raise
    except Exception as e:
        logger.error(f"Unexpected error when calling {endpoint}: {e}")
        raise
    return response


@click.command()
@click.option("--paths", **options)
def cli(paths):
    try:
        logger.info(f"CLI started with paths: {paths}")
        filtered_repo = utils.filter_repo_by_paths([Path(path) for path in paths])
        extracted_metrics = call_api_wrapper(
            endpoint="extract_metrics", payload=filtered_repo
        )
        submit_metrics = call_api_wrapper(
            endpoint="submit_metrics", payload=extracted_metrics
        )
        logger.info(f"Metrics submitted successfully: {submit_metrics}")
    except Exception as e:
        logger.error(f"CLI execution failed: {e}")
        raise


if __name__ == "__main__":
    cli()
