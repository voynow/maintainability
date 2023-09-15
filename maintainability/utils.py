import io
import logging
from pathlib import Path
from typing import Dict, List

import toml
from pathspec import PathSpec
from pathspec.patterns import GitWildMatchPattern
from pkg_resources import resource_stream


def load_toml():
    with resource_stream(__name__, "appconfig.toml") as f:
        text_stream = io.TextIOWrapper(f, encoding="utf-8")
        config = toml.load(text_stream)
    return config


def read_text(path: Path) -> str:
    try:
        with open(path, "r") as file:
            return file.read()
    except Exception as e:
        logging.error(f"Error reading file {path}: {e}")
        raise e


def get_ignored_patterns(gitignore_path: Path) -> PathSpec:
    if gitignore_path.exists():
        gitignore_content = read_text(gitignore_path)
        return PathSpec.from_lines(GitWildMatchPattern, gitignore_content.splitlines())
    else:
        logging.warning(".gitignore not found. No files will be ignored.")
        return PathSpec.from_lines(GitWildMatchPattern, [])


def load_files(basepath: Path = Path(".")) -> Dict[Path, str]:
    """Recursively collect all text from files under basepath"""
    result = {}
    for path in basepath.iterdir():
        if pathspec.match_file(str(path)):
            continue
        if path.is_file():
            if path.suffix in config["extensions"]:
                result[path] = read_text(path)
        elif path.is_dir():
            result.update(load_files(path))
    return result


def filter_repo_by_paths(paths: List[Path]) -> Dict[Path, str]:
    """Filter the repo dictionary to only include files under the directories in paths"""
    filtered_repo = {}
    for p in paths:
        filtered_repo.update(
            {k: v for k, v in repo.items() if p in k.parents or p == k}
        )
    return filtered_repo


config = load_toml()
pathspec = get_ignored_patterns(Path(".gitignore"))
repo = load_files()
