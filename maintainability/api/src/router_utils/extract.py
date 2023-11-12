import base64
import os
import re

import requests
from llm_blocks import block_factory

from . import config, io_operations, logger

GH_AUTH_TOKEN = os.environ.get("GH_AUTH_TOKEN")


def get_llm() -> callable:
    return block_factory.get(
        "template",
        template=config.PROMPT,
        temperature=config.TEMPERATURE,
        model_name=config.MODEL_NAME,
    )


def parse_response(text: str) -> float:
    try:
        match = re.search(r"(\d{1,2})/10", text)
        response = int(match.group(1))
    except AttributeError as e:
        logger.logger(f"Error parsing LLM response={text} with error={e}")
        response = -1
    return response


def extract_metrics(file_id: str, filepath: str, code: str, metric: str) -> int:
    gpt_interface = get_llm()
    description = config.METRIC_DESCRIPTIONS[metric]
    response = gpt_interface(
        filepath=filepath,
        code=code,
        metric=metric.replace("_", " "),
        description=description,
    )
    metric_quantity = int(parse_response(response))
    io_operations.write_metrics(
        file_id=file_id,
        metric=metric,
        metric_quantity=metric_quantity,
        reasoning=response,
    )
    return metric_quantity


def fetch_repo_structure(user: str, repo: str, branch: str = "main") -> list:
    headers = {"Authorization": f"token {GH_AUTH_TOKEN}"}
    url = f"https://api.github.com/repos/{user}/{repo}/git/trees/{branch}?recursive=1"

    resp = requests.get(url, headers=headers)
    resp.raise_for_status()

    return [
        f["path"]
        for f in resp.json().get("tree", [])
        if f["type"] == "blob"
        and any(f["path"].endswith(ext) for ext in config.EXTENSIONS)
    ]


def fetch_file_content(user: str, repo: str, path: str) -> str:
    headers = {"Authorization": f"token {GH_AUTH_TOKEN}"}
    file_url = f"https://api.github.com/repos/{user}/{repo}/contents/{path}"
    file_resp = requests.get(file_url, headers=headers)
    file_resp.raise_for_status()
    return base64.b64decode(file_resp.json()["content"]).decode("utf-8")


#
# file_paths = fetch_repo_structure(user, repo)

# repodata = {}
# for path in file_paths:
#     file_url = f"https://api.github.com/repos/{user}/{repo}/contents/{path}"
#     file_content = fetch_file_content(file_url, headers)
#     repodata[path] = file_content

# return repodata
