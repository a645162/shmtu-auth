import threading
from time import sleep as time_sleep

from shmtuauth.src.core.shmtu_auth import ShmtuNetAuth
from shmtuauth.utils import get_env_int, get_user_list

# 检测时间间隔，单位：秒
time_interval = 60

env_time_interval = get_env_int("SHMTU_AUTH_MONITOR_AUTH_TIME_INTERVAL", -1)
if env_time_interval > 0:
    time_interval = env_time_interval


def monitor_auth():
    print("Auth status monitor started.")

    net_auth = ShmtuNetAuth()

    user_list_3 = get_user_list()

    if len(user_list_3) == 0:
        print("No user information found.")
        return

    while True:
        if not net_auth.check_is_online():
            net_auth.login_by_list(user_list_3)

        time_sleep(time_interval)


def start_monitor_auth():
    t = threading.Thread(target=monitor_auth)
    t.start()
