# -*- coding: utf-8 -*-

import threading
from time import sleep as time_sleep

from shmtu_auth.src.core.shmtu_auth import ShmtuNetAuth
from shmtu_auth.src.utils.env import get_env_int
from shmtu_auth.src.utils.program_env_config import (
    convert_password_to_star,
    convert_number_to_star,
)
from shmtu_auth.src.utils.program_env_config import get_user_list

from shmtu_auth.src.utils.logs import get_logger

logger = get_logger()

# 检测时间间隔，单位：秒
time_interval = 60

env_time_interval = get_env_int("SHMTU_AUTH_TIME_INTERVAL", -1)
if env_time_interval > 0:
    time_interval = env_time_interval


def monitor_auth():
    logger.info("Initializing...")
    net_auth = ShmtuNetAuth()

    logger.info("Reading user information...")
    user_list_3 = get_user_list()

    if len(user_list_3) == 0:
        logger.error("No user information found.")
        return

    user_count = len(user_list_3)
    logger.info(f"Found {user_count} user:")
    for i in range(user_count):
        user = user_list_3[i]
        user_name = convert_number_to_star(user[0])
        password = convert_password_to_star(user[1])
        logger.info(f"[{i + 1}]User: {user_name}, Password: {password}")

    logger.info("Auth status monitor started.")

    while True:
        if not net_auth.check_is_online():
            if net_auth.login_by_list(user_list_3):
                logger.info("Login success.")
            else:
                logger.error("Login failed.")

        time_sleep(time_interval)


def start_monitor_auth():
    logger.info("Create Thread")
    t = threading.Thread(target=monitor_auth)
    logger.info("Created Thread")
    logger.info("Start Thread")
    t.start()
    logger.info("Thread Started.")
