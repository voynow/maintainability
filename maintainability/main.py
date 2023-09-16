from pathlib import Path
from typing import List

from . import analytics
from . import utils


def main(paths: List[Path]) -> None:
    filtered_repo = utils.filter_repo_by_paths(paths)
    maintainability_metrics = analytics.analyze_maintainability(filtered_repo)

    composite_metrics = {
        filepath: utils.compose_metrics(filepath, metrics)
        for filepath, metrics in maintainability_metrics.items()
    }

    utils.write_metrics(composite_metrics)
