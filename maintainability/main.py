from pathlib import Path
from typing import List
import uuid
from . import analytics
from . import utils


def main(paths: List[Path]) -> None:
    filtered_repo = utils.filter_repo_by_paths(paths)
    maintainability_metrics = analytics.analyze_maintainability(filtered_repo)

    session_id = str(uuid.uuid4())
    composite_metrics = {
        filepath: utils.compose_metrics(filepath, metrics, session_id)
        for filepath, metrics in maintainability_metrics.items()
    }

    utils.write_metrics(composite_metrics)
