# -*- coding: utf-8 -*-

import os

from shmtu_auth.src.config import build_info

from shmtu_auth.src.monitor import auth_status
from shmtu_auth.src.parse_args import parse_run_args

from shmtu_auth.src.utils.logs import get_logger

logger = get_logger()


def print_info():
    # SHMTU Auth
    url = "https://github.com/a645162/shmtu-auth"
    star_len = len(url) + 3

    print("=" * star_len)
    print("SHMTU Auth Monitor")
    print(url)
    print("Author: Haomin Kong")
    print("E-Mail: a645162@gmail.com")
    print("=" * star_len)


def check_is_docker() -> bool:
    env_docker = os.environ.get("DOCKER_MODE")
    return env_docker and len(env_docker.strip()) > 0


def print_build_info():
    print("Program Version:", build_info.program_version)
    if check_is_docker():
        print("Docker Build Time:", build_info.docker_build_time)

    if len(build_info.exe_build_time) > 0:
        print("Exe Build Time:", build_info.exe_build_time)

    if len(build_info.wheel_build_time) > 0:
        print("Wheel Build Time:", build_info.wheel_build_time)


def entry():
    print_info()
    print_build_info()

    logger.info("Parse args...")

    parse_run_args()

    logger.info("Program Start.")

    auth_status.start_monitor_auth()


if __name__ == "__main__":
    entry()
