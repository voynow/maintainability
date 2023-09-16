from datetime import datetime
import os
from pathlib import Path
from typing import Dict, List

from pathspec import PathSpec
from pathspec.patterns import GitWildMatchPattern
from supabase import Client, create_client

from . import config, models


def get_general_metrics(root_path: Path) -> models.GeneralMetrics:
    project_name = root_path.parents[-1].name
    timestamp = datetime.utcnow().isoformat()
    return models.GeneralMetrics(project_name, timestamp)


def get_file_metrics(filepath: Path) -> models.FileMetrics:
    file_size = os.path.getsize(filepath)
    language = filepath.suffix.lstrip(".")
    loc = len(open(filepath, "r").readlines())
    return models.FileMetrics(file_size, language, loc)


def compose_metrics(
    filepath: Path, maintainability: models.MaintainabilityMetrics
) -> models.CompositeMetrics:
    file_metrics = get_file_metrics(filepath)
    general_metrics = get_general_metrics(filepath)
    return models.CompositeMetrics(maintainability, file_metrics, general_metrics)


def connect_to_supabase() -> Client:
    """Connect to Supabase database"""
    return create_client(
        os.environ.get("SUPABASE_URL"),
        os.environ.get("SUPABASE_KEY"),
    )


def write_metrics(
    maintainability_metrics: Dict[Path, models.MaintainabilityMetrics]
) -> None:
    insert_data = {}  # Needs to be implemented, should be unstructured data

    table = connect_to_supabase().table("maintainability")
    data, count = table.insert(maintainability_metrics).execute()

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
