import os
import time
import requests
import base64
from dotenv import load_dotenv
import json

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


def fetch_repo_structure(user: str, repo: str, branch: str = "main") -> list:
    start_time = time.perf_counter()
    headers = {"Authorization": f"token {os.environ.get('GITHUB_AUTH_TOKEN')}"}
    tree_api_url = (
        f"https://api.github.com/repos/{user}/{repo}/git/trees/{branch}?recursive=1"
    )

    resp = requests.get(tree_api_url, headers=headers)
    resp.raise_for_status()

    file_paths = [
        f["path"]
        for f in resp.json().get("tree", [])
        if f["type"] == "blob" and any(f["path"].endswith(ext) for ext in EXTENSIONS)
    ]

    elapsed_time = time.perf_counter() - start_time
    print(f"Fetched repo structure in {elapsed_time:0.4f} seconds")
    return file_paths


def fetch_file_content(file_url: str, headers: dict) -> str:
    start_time = time.perf_counter()

    file_resp = requests.get(file_url, headers=headers)
    file_resp.raise_for_status()
    content = base64.b64decode(file_resp.json()["content"]).decode("utf-8")

    elapsed_time = time.perf_counter() - start_time
    print(f"Fetched file content in {elapsed_time:0.4f} seconds")
    return content


# Example usage of the functions
if __name__ == "__main__":
    user = "voynow"
    repo = "maintainability"
    branch = "main"
    headers = {"Authorization": f"token {os.environ.get('GITHUB_AUTH_TOKEN')}"}

    # Fetch the repo structure
    file_paths = fetch_repo_structure(user, repo, branch)

    # Fetch the content of each file
    repodata = {}
    for path in file_paths:
        file_url = f"https://api.github.com/repos/{user}/{repo}/contents/{path}"
        file_content = fetch_file_content(file_url, headers)
        repodata[path] = file_content

    # write the repo to a file
    with open("repo.json", "w") as f:
        f.write(json.dumps(repodata))
