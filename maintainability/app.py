import json
import logging
from pathlib import Path
from typing import Dict

from llm_blocks import block_factory

from .models import MaintainabilityMetrics
from .utils import collect_text_from_files, get_config, get_ignored_patterns

logging.basicConfig(level=logging.INFO)


def validate_metrics(data: Dict) -> MaintainabilityMetrics:
    try:
        return MaintainabilityMetrics(**data)
    except TypeError:
        logging.error("Invalid metrics schema.")
        raise ValueError("Invalid schema")


def analyze_code(
    path: Path, text: str, llm_block, retries: int, max_retries: int
) -> Dict:
    logging.info(f"Evaluating {path}")
    response = llm_block(filename=path, code=text)
    parsed_response = json.loads(response)

    try:
        return validate_metrics(parsed_response)
    except ValueError:
        logging.warning(f"Retry {retries + 1} for {path}.")
        if retries >= max_retries:
            logging.error(f"Max retries reached for {path}. Aborting.")
            return None
        return analyze_code(path, text, llm_block, retries + 1, max_retries)


def analyze_maintainability(
    llm_block, repo: Dict[Path, str], max_retries: int = 3
) -> Dict[Path, Dict]:
    result = {}
    for path, text in repo.items():
        metrics = analyze_code(path, text, llm_block, 0, max_retries)
        if metrics is not None:
            result[path] = metrics
    return result


def generate_output(maintainability_metrics: Dict[Path, Dict]) -> None:
    with open("output.json", "w") as file:
        json.dump(maintainability_metrics, file, indent=4)


def main() -> None:
    logging.info("Starting maintainability analysis")

    config = get_config()
    llm_block = block_factory.get(
        "template", template=config["prompt"], temperature=0.0
    )

    pathspec = get_ignored_patterns(Path(".gitignore"))
    repo = collect_text_from_files(Path("."), pathspec, config["extensions"])

    maintainability_metrics = analyze_maintainability(llm_block, repo)

    generate_output(maintainability_metrics)
    logging.info("Completed maintainability analysis")


if __name__ == "__main__":
    main()
