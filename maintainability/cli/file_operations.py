import logging
from pathlib import Path
from typing import Dict, List, Optional

from pathspec import PathSpec
from pathspec.patterns import GitWildMatchPattern

from . import config

logging.basicConfig(level=logging.INFO)


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


def should_include_file(
    filepath: Path, content: str, target_path: Path
) -> Optional[str]:
    # Check if file is under the target path
    if target_path not in filepath.parents and filepath != target_path:
        return f"not found under the target path {target_path}."

    # Check line count
    if len(content.splitlines()) < config.MIN_NUM_LINES:
        return f"insufficient lines len()={config.MIN_NUM_LINES}."

    # Check if it's a test file
    if filepath.name.startswith("test") or filepath.stem.endswith("test"):
        return f"identified as test file."

    # Check if it's a config file
    if filepath.name.startswith("config."):
        return f"identified as config file."

    return None


def filter_repo(repo: Dict[Path, str], target_paths: List[Path]) -> Dict[str, str]:
    filtered_repo = {}
    for target_path in target_paths:
        for filepath, content in repo.items():
            reason = should_include_file(filepath, content, target_path)

            if reason:
                logging.info(f"Excluding {filepath}: {reason}")
                continue

            filtered_repo[filepath.as_posix()] = content

    return filtered_repo


pathspec = get_ignored_patterns(Path(".gitignore"))
