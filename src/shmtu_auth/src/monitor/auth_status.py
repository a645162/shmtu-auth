import threading
from time import sleep as time_sleep

from shmtu_auth.src.core.shmtu_auth import ShmtuNetAuth
from shmtu_auth.src.utils.env import get_env_int
from shmtu_auth.src.utils.logs import get_logger
from shmtu_auth.src.utils.program_env_config import (
    convert_number_to_star,
    convert_password_to_star,
    get_user_list,
)

logger = get_logger()

# 检测时间间隔，单位：秒
time_interval = 10

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
        logger.info("Checking network status...")
        is_online = net_auth.check_is_online()
        if not is_online:
            logger.info("Network offline, trying to login...")
            if net_auth.login_by_list(user_list_3):
                logger.info("Login success.")
            else:
                logger.error("Login failed.")
        else:
            logger.info("Network is online, no action needed.")

        logger.info(f"Sleeping for {time_interval} seconds...")
        time_sleep(time_interval)


def start_monitor_auth():
    logger.info("Create Thread")
    t = threading.Thread(target=monitor_auth)
    logger.info("Created Thread")
    logger.info("Start Thread")
    t.start()
    logger.info("Thread Started.")
