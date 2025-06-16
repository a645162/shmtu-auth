import re

import requests

github_author_name = "a645162"
github_repo_name = "shmtu-auth"


def get_github_branches() -> list[str]:
    """获取GitHub仓库的分支列表，排除gh-pages分支"""
    url = f"https://api.github.com/repos/{github_author_name}/{github_repo_name}/branches"

    try:
        response = requests.get(url)
        if response.status_code != 200:
            return ["main"]  # 如果API请求失败，返回默认分支

        branches_data = response.json()
        branches = []

        for branch_info in branches_data:
            branch_name = branch_info.get("name", "")
            # 排除gh-pages分支
            if branch_name and branch_name != "gh-pages":
                branches.append(branch_name)

        # 确保main分支在列表中，如果不在则添加
        if "main" not in branches and len(branches) > 0:
            branches.insert(0, "main")
        elif len(branches) == 0:
            branches = ["main"]

        # 将main分支排到第一位
        if "main" in branches:
            branches.remove("main")
            branches.insert(0, "main")

        return branches
    except Exception:
        return ["main"]  # 异常情况下返回默认分支


def get_branch_version(branch: str = "main") -> str:
    url = f"https://raw.githubusercontent.com/{github_author_name}/{github_repo_name}"
    url += f"/refs/heads/{branch}/"
    url += "src/shmtu_auth/version.py"

    try:
        response = requests.get(url)
        content = response.text.strip()
        if len(content) == 0:
            return ""

        # 使用正则表达式匹配 __version__ 变量
        version_pattern = r'__version__\s*=\s*["\']([^"\']+)["\']'
        match = re.search(version_pattern, content)

        if not match:
            return ""

        version_str = match.group(1)

        spilt_list = version_str.split(".")
        if len(spilt_list) != 3:
            return ""
        for i in spilt_list:
            if not i.isdigit():
                return ""

        return version_str
    except Exception:
        return ""


if __name__ == "__main__":
    print("Available branches:", get_github_branches())
    print("main", get_branch_version("main"))
    print("beta", get_branch_version("beta"))
    print("dev", get_branch_version("dev"))
