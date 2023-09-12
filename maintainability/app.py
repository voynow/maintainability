import json
import logging
from pathlib import Path
from typing import Dict, Optional

from llm_blocks import block_factory

from .models import MaintainabilityMetrics
from .utils import collect_text_from_files, get_ignored_patterns, config

logging.basicConfig(level=logging.INFO)


def analyze_code(response: str) -> Optional[Dict]:
    print(response)
    jsonified_data = json.loads(response)
    return MaintainabilityMetrics(**jsonified_data)


def analyze_maintainability(repo: Dict[Path, str]) -> Dict[Path, Dict]:
    model_name = "gpt-3.5-turbo-16k"
    block = block_factory.get(
        "template", template=config["prompt"], temperature=0.0, model_name=model_name
    )

    result = {}
    for filepath, code in repo.items():
        if len(code):
            logging.info(f"Analyzing {filepath}")
            response = block(filepath=filepath, code=code)
            result[filepath] = analyze_code(response)

    return result


def generate_output(maintainability_metrics: Dict[Path, Dict]) -> None:
    with open("output.json", "w") as file:
        json.dump(maintainability_metrics, file, indent=4)


def main() -> None:
    pathspec = get_ignored_patterns(Path(".gitignore"))
    repo = collect_text_from_files(Path("."), pathspec)

    maintainability_metrics = analyze_maintainability(repo)
    generate_output(maintainability_metrics)


if __name__ == "__main__":
    main()
