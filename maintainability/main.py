from pathlib import Path
from typing import List

from . import analytics
from . import models
from . import utils


def main(paths: List[Path]) -> None:
    filtered_repo = utils.filter_repo_by_paths(paths)
    maintainability_metrics = analytics.analyze_maintainability(filtered_repo)
    models.write_metrics(maintainability_metrics)
