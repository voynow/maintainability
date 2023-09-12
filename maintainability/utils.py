import json
import logging
from pathlib import Path
from typing import List, Dict
from pathspec import PathSpec
from pathspec.patterns import GitWildMatchPattern
from pkg_resources import resource_stream


def get_config() -> dict:
    with resource_stream(__name__, "config.json") as f:
        return json.load(f)


def read_text(path: Path) -> str:
    try:
        with open(path, "r") as file:
            return file.read()
    except Exception as e:
        logging.error(f"Error reading file {path}: {e}")
        raise e


def get_ignored_patterns(gitignore_path: Path) -> PathSpec:
    try:
        gitignore_content = read_text(gitignore_path)
        return PathSpec.from_lines(GitWildMatchPattern, gitignore_content.splitlines())
    except FileNotFoundError:
        logging.warning(".gitignore not found. No files will be ignored.")
        return PathSpec.from_lines(GitWildMatchPattern, [])


def collect_text_from_files(
    dir_path: Path, pathspec: PathSpec, extensions: List[str]
) -> Dict[Path, str]:
    result = {}
    for path in dir_path.iterdir():
        if pathspec.match_file(str(path)):
            continue
        if path.is_file():
            if path.suffix in extensions:
                result[path.name] = read_text(path)
        elif path.is_dir():
            result.update(collect_text_from_files(path, pathspec, extensions))
    return result
