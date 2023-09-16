import json
import os
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple

from llm_blocks import block_factory
from pathspec import PathSpec
from pathspec.patterns import GitWildMatchPattern
from supabase import Client, create_client

from . import config, models


def get_file_metrics(filepath: Path) -> models.FileMetrics:
    file_size = os.path.getsize(filepath)
    language = filepath.suffix.lstrip(".")
    content = read_text(filepath)
    loc = len(content.splitlines())
    return models.FileMetrics(
        file_size=file_size, loc=loc, language=language, content=content
    )


def get_maintainability_metrics(
    filepath: Path, code: str
) -> models.MaintainabilityMetrics:
    llm = block_factory.get(
        "template",
        template=config.PROMPT,
        temperature=config.TEMPERATURE,
        model_name=config.MODEL_NAME,
    )
    response = llm(filepath=filepath, code=code)
    return models.MaintainabilityMetrics(**json.loads(response))


def compose_metrics(
    filepath: Path, code: str, session_id: str
) -> models.CompositeMetrics:
    maintainability_metrics = get_maintainability_metrics(filepath, code)
    file_metrics = get_file_metrics(filepath)
    return models.CompositeMetrics(
        maintainability=maintainability_metrics,
        file_info=file_metrics,
        timestamp=datetime.utcnow().isoformat(),
        session_id=session_id,
    )


def connect_to_supabase() -> Client:
    """Connect to Supabase database"""
    return create_client(
        os.environ.get("SUPABASE_URL"),
        os.environ.get("SUPABASE_KEY"),
    )


def write_metrics(metrics: Dict[Path, models.CompositeMetrics]) -> Tuple:
    insert_data = [
        {
            "primary_id": str(uuid.uuid4()),
            "file_path": str(filepath),
            "readability": metrics.maintainability.readability,
            "design_quality": metrics.maintainability.design_quality,
            "testability": metrics.maintainability.testability,
            "consistency": metrics.maintainability.consistency,
            "debug_error_handling": metrics.maintainability.debug_error_handling,
            "file_size": metrics.file_info.file_size,
            "language": metrics.file_info.language,
            "loc": metrics.file_info.loc,
            "content": metrics.file_info.content,
            "timestamp": metrics.timestamp,
            "session_id": metrics.session_id,
        }
        for filepath, metrics in metrics.items()
    ]
    table = connect_to_supabase().table("maintainability")
    return table.insert(insert_data).execute()


def read_text(path: Path) -> str:
    if path in file_cache:
        return file_cache[path]

    with open(path, "r") as file:
        content = file.read()
        file_cache[path] = content
        return content


def get_ignored_patterns(gitignore_path: Path) -> PathSpec:
    if gitignore_path.exists():
        gitignore_content = read_text(gitignore_path)
        return PathSpec.from_lines(GitWildMatchPattern, gitignore_content.splitlines())
    return PathSpec.from_lines(GitWildMatchPattern, [])


def load_files(basepath: Path = Path(".")) -> Dict[Path, str]:
    result = {}
    for path in basepath.iterdir():
        if pathspec.match_file(str(path)):
            continue
        if path.is_file():
            if path.suffix in config.EXTENSIONS:
                result[path] = read_text(path)
        elif path.is_dir():
            result.update(load_files(path))
    return result


def filter_repo_by_paths(paths: List[Path]) -> Dict[Path, str]:
    repo = load_files()
    filtered_repo = {}
    for p in paths:
        filtered_repo.update(
            {k: v for k, v in repo.items() if p in k.parents or p == k}
        )
    return filtered_repo


file_cache = {}
pathspec = get_ignored_patterns(Path(".gitignore"))
