# -*- coding: utf-8 -*-

import requests


def get_latest_release_version(repo_owner, repo_name):
    api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest"
    response = requests.get(api_url)

    if response.status_code == 200:
        release_info = response.json()
        return release_info["tag_name"]
    else:
        print(
            f"Failed to fetch release information. Status code: {response.status_code}"
        )
        return None


if __name__ == "__main__":
    owner = "mozilla"  # 替换为你要查询的 GitHub 仓库的所有者
    repo = "geckodriver"  # 替换为你要查询的 GitHub 仓库的名称

    latest_version = get_latest_release_version(owner, repo)

    if latest_version:
        print(f"Latest version of {repo}: {latest_version}")
    else:
        print("Failed to retrieve the latest version.")
