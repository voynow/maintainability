import logging
from pathlib import Path
from llm_blocks import block_factory, blocks
from pathspec import PathSpec
from pathspec.patterns import GitWildMatchPattern

logging.basicConfig(level=logging.INFO)

ACCEPTED_EXTENSIONS = [
    ".py",
    ".js",
    ".java",
    ".c",
    ".cpp",
    ".h",
    ".cs",
    ".go",
    ".rb",
    ".php",
    ".swift",
    ".ts",
    ".kt",
    ".rs",
    ".scala",
    ".m",
    ".sh",
    ".sql",
    ".html",
    ".css",
]

PROMPT_TEMPLATE = (
    """Calculate the maintainability of the following code\n\n{filename}:\n{code}"""
)


def read_text(path: Path) -> str:
    try:
        with open(path, "r") as file:
            return file.read()
    except UnicodeDecodeError:
        with open(path, "r", encoding="utf-8", errors="replace") as file:
            return file.read()
    except Exception as e:
        logging.error(f"Error reading file {path}: {e}")
        raise e


def get_ignored_patterns(gitignore_path: Path) -> PathSpec:
    try:
        gitignore_content = read_text(gitignore_path)
        return PathSpec.from_lines(GitWildMatchPattern, gitignore_content.splitlines())
    except FileNotFoundError:
        logging.warning(".gitignore not found. No files will be ignored based on it.")
        return PathSpec.from_lines(GitWildMatchPattern, [])


def collect_text_from_files(dir_path: Path, pathspec: PathSpec) -> dict[Path, str]:
    result = {}
    for path in dir_path.iterdir():
        if pathspec.match_file(str(path)):
            continue
        if path.is_file():
            if path.suffix in ACCEPTED_EXTENSIONS:
                result[path.name] = read_text(path)
        elif path.is_dir():
            result.update(collect_text_from_files(path, pathspec))
    return result


def analyze_maintainability(
    block: blocks.TemplateBlock, repo: dict[Path, str]
) -> dict[Path, str]:
    result = {}
    for path, text in repo.items():
        logging.info(f"Evaluating {path}")
        result[path] = block(filename=path, code=text)
    return result


def generate_output(maintainability_metrics: dict) -> None:
    with open("output.txt", "w") as file:
        file.write(str(maintainability_metrics))


def main() -> None:
    logging.info("Starting maintainability analysis")
    pathspec = get_ignored_patterns(Path(".gitignore"))
    repo = collect_text_from_files(Path("."), pathspec)

    block = block_factory.get("template", template=PROMPT_TEMPLATE)
    maintainability_metrics = analyze_maintainability(block, repo)

    generate_output(maintainability_metrics)
    logging.info("Completed maintainability analysis")


if __name__ == "__main__":
    main()
