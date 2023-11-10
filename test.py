import requests
import base64
import json
import os
from dotenv import load_dotenv

load_dotenv()


EXTENSIONS = [
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


def extract_repo_from_github(user, repo, branch="main"):
    """
    Fetch the contents of a GitHub repository, filtered by file extension, with authentication.

    :param user: Username of the repository owner.
    :param repo: Repository name.
    :param branch: Branch name, default is 'main'.
    :param extensions: List of file extensions to include (e.g., ['.py', '.md']).
    :param token: Personal access token for GitHub authentication.
    :return: Dictionary with file paths as keys and their content as values.
    """

    headers = {"Authorization": f"token {os.environ.get('GITHUB_AUTH_TOKEN')}"}
    api_url = (
        f"https://api.github.com/repos/{user}/{repo}/git/trees/{branch}?recursive=1"
    )
    response = requests.get(api_url, headers=headers)
    response.raise_for_status()

    repo_files = {}
    for file in response.json()["tree"]:
        valid_extension = file["path"].endswith(tuple(EXTENSIONS))
        if file["type"] == "blob" and valid_extension:
            file_url = file["url"]
            file_response = requests.get(file_url, headers=headers)
            file_response.raise_for_status()
            try:
                file_content = base64.b64decode(file_response.json()["content"])
                repo_files[file["path"]] = file_content.decode("utf-8")
            except UnicodeDecodeError:
                print(f"Could not decode file {file['path']}")
                repo_files[file["path"]] = None

    return repo_files


repo_files = extract_repo_from_github("voynow", "maintainability")

# write to json file
with open("repo_files.json", "w") as outfile:
    json.dump(repo_files, outfile)
