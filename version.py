# -*- coding: utf-8 -*-

path = "version.txt"


def get_version() -> str:
    with open(path, "r", encoding="utf-8") as f:
        content = f.read().strip()

    version_list = content.split(".")

    if len(version_list) != 3:
        exit(1)

    for i in version_list:
        if not i.isdigit():
            exit(1)

    return content


if __name__ == "__main__":
    print(get_version(), end="")
