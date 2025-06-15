# -*- coding: utf-8 -*-

import os
import subprocess
import sys


def navigate_to_file(file_path: str):
    if sys.platform == "win32":
        os.startfile(file_path)
    elif sys.platform == "darwin":
        # 显示在最前方(需要授权)
        subprocess.Popen(
            [
                "osascript",
                "-e",
                'tell application "Finder" to set frontmost of process "Finder" to true',
            ]
        )

        # 使用 osascript 命令来调用 AppleScript 脚本，在 Finder 中导航到文件
        subprocess.Popen(
            [
                "osascript",
                "-e",
                f'tell application "Finder" to reveal POSIX file "{file_path}"',
            ]
        )
    else:
        subprocess.Popen(["xdg-open", file_path])


if __name__ == "__main__":
    print("Platform:", sys.platform)

    # Windows
    # navigate_to_file("/home/konghaomin/MOTRv2.7z")

    # macOS
    # navigate_to_file("/Users/konghaomin/MOTRv2.7z")

    # Linux
    # navigate_to_file("/home/konghaomin/MOTRv2.7z")
