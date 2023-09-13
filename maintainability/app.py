import json
import logging
from pathlib import Path
from typing import Dict, Optional

from llm_blocks import block_factory

from .models import MaintainabilityMetrics
from .utils import collect_text_from_files, get_ignored_patterns, config

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


def write_output(maintainability_metrics: Dict[str, MaintainabilityMetrics]) -> None:
    aggregated_metrics = {
        filepath: metrics.__dict__
        for filepath, metrics in maintainability_metrics.items()
    }

    with open("metrics.json", "w") as f:
        json.dump(aggregated_metrics, f, indent=4)


def main() -> None:
    pathspec = get_ignored_patterns(Path(".gitignore"))
    repo = collect_text_from_files(Path("."), pathspec)

    maintainability_metrics = analyze_maintainability(repo)
    write_output(maintainability_metrics)


if __name__ == "__main__":
    main()
