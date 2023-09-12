import io
import logging
from pathlib import Path
from typing import Dict

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
    try:
        gitignore_content = read_text(gitignore_path)
        return PathSpec.from_lines(GitWildMatchPattern, gitignore_content.splitlines())
    except FileNotFoundError:
        logging.warning(".gitignore not found. No files will be ignored.")
        return PathSpec.from_lines(GitWildMatchPattern, [])


def collect_text_from_files(dir_path: Path, pathspec: PathSpec) -> Dict[Path, str]:
    result = {}
    for path in dir_path.iterdir():
        if pathspec.match_file(str(path)):
            continue
        if path.is_file():
            if path.suffix in config["extensions"]:
                result[path.name] = read_text(path)
        elif path.is_dir():
            result.update(collect_text_from_files(path, pathspec))
    return result


config = load_toml()
