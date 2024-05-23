# -*- coding: utf-8 -*-

import os
import datetime
import argparse
import pytz

build_dir = os.path.dirname(__file__)
base_dir = os.path.dirname(build_dir)

now_utc = datetime.datetime.now(pytz.utc)
print("Current Time:", now_utc.strftime("%Y-%m-%d %H:%M:%S"))

beijing_timezone = pytz.timezone('Asia/Shanghai')
beijing_time = now_utc.astimezone(beijing_timezone)

beijing_time_str = beijing_time.strftime("%Y-%m-%d %H:%M:%S")
print("Beijing Time:", beijing_time_str)

formatted_now = beijing_time_str
print("Current Time:", formatted_now)


def set_build_info_variable(
        src: str,
        key: str, value: str
) -> str:
    """Set the value of a variable in a file"""
    spilt_list = src.strip().split("\n")
    index = -1
    for i in range(len(spilt_list)):
        if key in spilt_list[i]:
            index = i
            break
    if index == -1:
        exit(1)

    spilt_list[index] = f"{key} = \"{value}\""
    return "\n".join(spilt_list) + "\n"


def set_build_config(src: str, variable: dict) -> str:
    for key in variable:
        src = set_build_info_variable(src, key, variable[key])
    return src


def get_version() -> str:
    with open(os.path.join(base_dir, "version.txt"), "r", encoding="utf-8") as f:
        content = f.read().strip()

    return content


def check_is_docker() -> bool:
    env_docker = os.environ.get("DOCKER_MODE")
    return env_docker and len(env_docker.strip()) > 0


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description='Build Info',
    )

    parser.add_argument(
        '-d', '--docker',
        help='Docker build',
        action="store_true"
    )
    parser.add_argument(
        '-e', '--exe',
        help='Binary build',
        action="store_true"
    )
    parser.add_argument(
        '-g', '--gui',
        help='Binary GUI Build',
        action="store_true"
    )
    parser.add_argument(
        '-w', '--wheel',
        help='Wheel build',
        action="store_true"
    )

    args = parser.parse_args()

    # Read Py File
    py_path = os.path.join(
        base_dir,
        "shmtu_auth", "src", "config", "build_info.py"
    )

    with open(py_path, "r", encoding="utf-8") as f:
        src = f.read()

    # Set Version
    version = get_version()

    src = set_build_config(src, {
        "program_version": version
    })

    if check_is_docker() or (hasattr(args, 'docker') and args.docker):
        src = set_build_config(src, {
            "docker_build_time": formatted_now
        })

    if hasattr(args, 'exe') and args.exe:
        src = set_build_config(src, {
            "exe_build_time": formatted_now
        })
    if hasattr(args, 'gui') and args.exe:
        file_path = os.path.join(
            base_dir, "shmtu_auth", "src",
            "utils", "logs.py"
        )

        if not os.path.exists(file_path):
            print("logs.py is not found:", file_path)
            exit(1)

        with open(
                file_path,"w+", encoding="utf-8"
        ) as f:
            text = f.read()
            text = text.replace("shmtu_auth_", "shmtu_auth_gui_")
            f.write(text)

    if hasattr(args, 'wheel') and args.wheel:
        src = set_build_config(src, {
            "wheel_build_time": formatted_now
        })

    # Write Py File
    with open(py_path, "w", encoding="utf-8") as f:
        f.write(src)
