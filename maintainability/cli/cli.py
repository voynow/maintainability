import logging
import uuid
from pathlib import Path
from typing import List, Dict

import click

from maintainability.api import config, utils

options = {
    "multiple": True,
    "type": click.Path(exists=True),
    "help": "List of paths to analyze",
    "default": ["."],
}


def main(paths: List[Path]) -> None:
    filtered_repo = utils.filter_repo_by_paths(paths)
    session_id = str(uuid.uuid4())

    composite_metrics: Dict[str, utils.CompositeMetrics] = {}
    for filepath, code in filtered_repo.items():
        if len(code.splitlines()) > config.MIN_NUM_LINES:
            logging.info(f"Processing {filepath}")
            composite_metrics[filepath.as_posix()] = utils.compose_metrics(
                filepath, code, session_id
            )

    response = utils.write_metrics(composite_metrics)
    logging.info(f"Response: {response}")


@click.command()
@click.option("--paths", **options)
def cli(paths):
    main([Path(path) for path in paths])


if __name__ == "__main__":
    cli()
