# -*- coding: utf-8 -*-

import os
import sys


def is_dir_path_valid(dir_path: str) -> bool:
    try:
        os.makedirs(dir_path, exist_ok=True)

        return True
    except Exception:
        return False


def is_path_valid(path: str) -> bool:
    dir_path = os.path.dirname(path)

    try:
        os.makedirs(dir_path, exist_ok=True)
    except Exception:
        return False

    if sys.platform == "win32":
        # 在 Windows 上，路径可以包含反斜杠，但不能以反斜杠开头
        if path.startswith("\\"):
            return False
    elif sys.platform == "darwin":
        # 在 macOS 上，路径可以包含冒号和斜杠，但不能以冒号开头
        if path.startswith(":"):
            return False
    else:
        # 在 Linux 上，路径可以包含斜杠，但不能以斜杠开头
        if path.startswith("/"):
            return False

    if not os.path.isdir(dir_path):
        return False

    return True


def try_to_write_path(path: str) -> bool:
    dir_path = os.path.dirname(path)

    try:
        os.makedirs(dir_path, exist_ok=True)

        with open(path, "w") as f:
            f.write("test")
        os.remove(path)

        return True
    except Exception:
        return False


if __name__ == "__main__":
    # 使用示例
    path = "/Users/konghaomin/file.txt"
    if is_path_valid(path):
        print(f"Path '{path}' is valid.")
    else:
        print(f"Path '{path}' is not valid.")

    if try_to_write_path(path):
        print(f"Path '{path}' can write.")
    else:
        print(f"Path '{path}' can not write.")
