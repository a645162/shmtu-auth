# -*- coding: utf-8 -*-

import requests

github_author_name = "a645162"
github_repo_name = "shmtu-auth"


def get_branch_version(branch: str = "main") -> str:
    url = f"https://raw.githubusercontent.com/{github_author_name}/{github_repo_name}/{branch}/version.txt"

    try:
        response = requests.get(url)
        version_str = response.text.strip()
        if len(version_str) == 0:
            return ""

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
