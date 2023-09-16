import os
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, List

from pathspec import PathSpec
from pathspec.patterns import GitWildMatchPattern
from supabase import Client, create_client

from . import config, models


def get_general_metrics(root_path: Path, session_id: str) -> models.GeneralMetrics:
    project_name = root_path.parents[-1].name
    timestamp = datetime.utcnow().isoformat()
    return models.GeneralMetrics(project_name, timestamp, session_id)


def get_file_metrics(filepath: Path) -> models.FileMetrics:
    file_size = os.path.getsize(filepath)
    language = filepath.suffix.lstrip(".")
    loc = len(open(filepath, "r").readlines())
    return models.FileMetrics(file_size, language, loc)


def compose_metrics(
    filepath: Path, maintainability: models.MaintainabilityMetrics, session_id: str
) -> models.CompositeMetrics:
    file_metrics = get_file_metrics(filepath)
    general_metrics = get_general_metrics(filepath, session_id)
    return models.CompositeMetrics(maintainability, file_metrics, general_metrics)


def connect_to_supabase() -> Client:
    """Connect to Supabase database"""
    return create_client(
        os.environ.get("SUPABASE_URL"),
        os.environ.get("SUPABASE_KEY"),
    )


def write_metrics(metrics: Dict[Path, models.CompositeMetrics]) -> None:
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
            "project_name": metrics.general_info.project_name,
            "timestamp": metrics.general_info.timestamp,
            "session_id": metrics.general_info.session_id,
        }
        for filepath, metrics in metrics.items()
    ]

    table = connect_to_supabase().table("maintainability")
    data, count = table.insert(insert_data).execute()
    print(data, count)


def read_text(path: Path) -> str:
    with open(path, "r") as file:
        return file.read()


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


pathspec = get_ignored_patterns(Path(".gitignore"))
