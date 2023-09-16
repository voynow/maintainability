from dataclasses import dataclass
from typing import Dict
import json


@dataclass
class MaintainabilityMetrics:
    readability: int
    design_quality: int
    testability: int
    consistency: int
    debug_error_handling: int


def write_metrics(maintainability_metrics: Dict[str, MaintainabilityMetrics]) -> None:
    """write to json file"""

    aggregated_metrics = {
        filepath.as_posix(): metrics.__dict__
        for filepath, metrics in maintainability_metrics.items()
    }

    json.dump(aggregated_metrics, open("output.json", "w"))
