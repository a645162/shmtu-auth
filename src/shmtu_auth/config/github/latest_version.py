import re

import requests

github_author_name = "a645162"
github_repo_name = "shmtu-auth"


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
    print("main", get_branch_version("main"))
    print("beta", get_branch_version("beta"))
    print("dev", get_branch_version("dev"))
