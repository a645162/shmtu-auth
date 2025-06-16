import argparse
import datetime
import os
import re

import pytz

build_dir = os.path.dirname(__file__)
base_dir = os.path.dirname(build_dir)

now_utc = datetime.datetime.now(pytz.utc)
print("Current Time:", now_utc.strftime("%Y-%m-%d %H:%M:%S"))

beijing_timezone = pytz.timezone("Asia/Shanghai")
beijing_time = now_utc.astimezone(beijing_timezone)

beijing_time_str = beijing_time.strftime("%Y-%m-%d %H:%M:%S")
print("Beijing Time:", beijing_time_str)

formatted_now = beijing_time_str
print("Current Time:", formatted_now)


def set_build_info_variable(src: str, key: str, value: str) -> str:
    """Set the value of a variable in a file"""
    spilt_list = src.strip().split("\n")
    index = -1
    for i in range(len(spilt_list)):
        if key in spilt_list[i]:
            index = i
            break
    if index == -1:
        exit(1)

    spilt_list[index] = f'{key} = "{value}"'
    return "\n".join(spilt_list) + "\n"


def set_build_config(src: str, variable: dict) -> str:
    for key in variable:
        src = set_build_info_variable(src, key, variable[key])
    return src


def read_version_from_init():
    """从 src/shmtu_auth/__init__.py 中读取 __version__ 变量"""
    # 获取当前文件所在目录作为base_dir
    # base_dir = os.path.dirname(os.path.abspath(__file__))
    init_file_path = os.path.join(base_dir, "src", "shmtu_auth", "version.py")

    try:
        with open(init_file_path, encoding="utf-8") as f:
            content = f.read()

        # 使用正则表达式匹配 __version__ 变量
        version_pattern = r'__version__\s*=\s*["\']([^"\']+)["\']'
        match = re.search(version_pattern, content)

        if match:
            version = match.group(1)
            return version
        else:
            return None

    except FileNotFoundError:
        return None
    except Exception:
        return None


def check_is_docker() -> bool:
    env_docker = os.environ.get("DOCKER_MODE")
    return env_docker and len(env_docker.strip()) > 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Build Info",
    )

    parser.add_argument("-d", "--docker", help="Docker build", action="store_true")
    parser.add_argument("-e", "--exe", help="Binary build", action="store_true")
    parser.add_argument("-g", "--gui", help="Binary GUI Build", action="store_true")
    parser.add_argument("-w", "--wheel", help="Wheel build", action="store_true")

    args = parser.parse_args()

    # Read Py File
    py_path = os.path.join(base_dir, "src", "shmtu_auth", "src", "config", "build_info.py")

    with open(py_path, encoding="utf-8") as f:
        src = f.read()

    # Set Version
    version = read_version_from_init()
    if not version:
        print("Version not found in __init__.py")
        exit(1)
    print("Version:", version)

    src = set_build_config(src, {"program_version": version})

    if check_is_docker() or (hasattr(args, "docker") and args.docker):
        src = set_build_config(src, {"docker_build_time": formatted_now})

    if hasattr(args, "exe") and args.exe:
        src = set_build_config(src, {"exe_build_time": formatted_now})
    if hasattr(args, "gui") and args.exe:
        file_path = os.path.join(base_dir, "src", "shmtu_auth", "src", "utils", "logs.py")

        if not os.path.exists(file_path):
            print("logs.py is not found:", file_path)
            exit(1)

        with open(file_path, "w+", encoding="utf-8") as f:
            text = f.read()
            text = text.replace("shmtu_auth_", "shmtu_auth_gui_")
            f.write(text)

    if hasattr(args, "wheel") and args.wheel:
        src = set_build_config(src, {"wheel_build_time": formatted_now})

    # Write Py File
    with open(py_path, "w", encoding="utf-8") as f:
        f.write(src)
