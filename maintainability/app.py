import json
import logging
from pathlib import Path
from typing import Dict, Optional, List

from llm_blocks import block_factory

from .models import MaintainabilityMetrics
from .utils import filter_repo_by_paths, config

logging.basicConfig(level=logging.INFO)


def analyze_code(response: str) -> Optional[Dict]:
    jsonified_data = json.loads(response)
    return MaintainabilityMetrics(**jsonified_data)


def analyze_maintainability(repo: Dict[str, str]) -> Dict[str, Dict]:
    model_name = "gpt-3.5-turbo-16k"
    block = block_factory.get(
        "template", template=config["prompt"], temperature=0.0, model_name=model_name
    )

    result = {}
    for filepath, code in repo.items():
        if len(code.splitlines()) > config["min_num_lines"]:
            logging.info(f"Analyzing {filepath}")
            response = block(filepath=filepath, code=code)
            result[filepath] = analyze_code(response)

    return result


def write_output(
    maintainability_metrics: Dict[str, MaintainabilityMetrics],
) -> None:
    aggregated_metrics = {
        filepath.as_posix(): metrics.__dict__
        for filepath, metrics in maintainability_metrics.items()
    }

    json.dump(aggregated_metrics, open(config["output_file"], "w"))


def main(paths: List[Path]) -> None:
    filtered_repo = filter_repo_by_paths(paths)
    maintainability_metrics = analyze_maintainability(filtered_repo)
    write_output(maintainability_metrics)


if __name__ == "__main__":
    main()
