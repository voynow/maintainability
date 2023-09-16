import logging
import uuid
from pathlib import Path
from typing import List

from . import config, utils


def main(paths: List[Path]) -> None:
    filtered_repo = utils.filter_repo_by_paths(paths)
    session_id = str(uuid.uuid4())

    composite_metrics = {}
    for filepath, code in filtered_repo.items():
        if len(code.splitlines()) > config.MIN_NUM_LINES:
            logging.info(f"Processing {filepath}")
            composite_metrics[filepath] = utils.compose_metrics(
                filepath, code, session_id
            )

    response = utils.write_metrics(composite_metrics)
    logging.info(f"Response: {response}")
