import json
import logging
from typing import Dict, Optional

from llm_blocks import block_factory

from . import config
from . import models

logging.basicConfig(level=logging.INFO)


def analyze_code(response: str) -> Optional[Dict]:
    jsonified_data = json.loads(response)
    return models.MaintainabilityMetrics(**jsonified_data)


def analyze_maintainability(repo: Dict[str, str]) -> Dict[str, Dict]:
    model_name = "gpt-3.5-turbo-16k"
    block = block_factory.get(
        "template", template=config.PROMPT, temperature=0.0, model_name=model_name
    )
    result = {}
    for filepath, code in repo.items():
        if len(code.splitlines()) > config["min_num_lines"]:
            logging.info(f"Analyzing {filepath}")
            response = block(filepath=filepath, code=code)
            result[filepath] = analyze_code(response)
    return result
