import os
import requests
import base64

from . import config


GH_AUTH_TOKEN = os.environ.get("GH_AUTH_TOKEN")


def fetch_repo_structure(user: str, repo: str, branch: str = "main") -> list:
    headers = {"Authorization": f"token {GH_AUTH_TOKEN}"}
    url = f"https://api.github.com/repos/{user}/{repo}/git/trees/{branch}?recursive=1"

    resp = requests.get(url, headers=headers)
    resp.raise_for_status()

    return [
        f["path"]
        for f in resp.json().get("tree", [])
        if f["type"] == "blob"
        and any(f["path"].endswith(ext) for ext in config.EXTENSIONS)
    ]


def fetch_file_content(user: str, repo: str, path: str) -> str:
    headers = {"Authorization": f"token {GH_AUTH_TOKEN}"}
    file_url = f"https://api.github.com/repos/{user}/{repo}/contents/{path}"
    file_resp = requests.get(file_url, headers=headers)
    file_resp.raise_for_status()
    return base64.b64decode(file_resp.json()["content"]).decode("utf-8")


#
# file_paths = fetch_repo_structure(user, repo)

# repodata = {}
# for path in file_paths:
#     file_url = f"https://api.github.com/repos/{user}/{repo}/contents/{path}"
#     file_content = fetch_file_content(file_url, headers)
#     repodata[path] = file_content

# return repodata
