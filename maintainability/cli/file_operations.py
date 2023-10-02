from pathlib import Path
from typing import Dict, List

from pathspec import PathSpec
from pathspec.patterns import GitWildMatchPattern

from . import config


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
            {k.as_posix(): v for k, v in repo.items() if p in k.parents or p == k}
        )
    return filtered_repo


pathspec = get_ignored_patterns(Path(".gitignore"))
