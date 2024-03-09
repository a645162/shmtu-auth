import datetime
import json
import threading
from time import sleep as time_sleep

import requests

from shmtuauth.utils import my_time
from shmtuauth.utils.env import *

ENV_VAR_NAME = "SHMTU_AUTH_WEBHOOK_WEWORK"
WARNING_ENV_NAME = "SHMTU_AUTH_WEBHOOK_WEWORK_WARNING"

machine_name = get_env_str("SHMTU_AUTH_MACHINE_NAME", "")


def get_wework_url(webhook_env: str = ""):
    if len(webhook_env.strip()) == 0:
        wework_env = get_env_str(ENV_VAR_NAME, "")
    else:
        wework_env = webhook_env.strip()

    if not wework_env:
        print(f"{ENV_VAR_NAME} Not Set!")
        return None

    if len(wework_env) == 0:
        print(f"WeWork Key Env!")
        return None

    # Judge is URL
    if wework_env.startswith("http"):
        return wework_env

    webhook_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=" + wework_env
    return webhook_url


webhook_warning_url = get_wework_url(get_env_str(WARNING_ENV_NAME, ""))


def direct_send_text(
    webhook_url: str, msg: str, mentioned_id=None, mentioned_mobile=None
):
    if mentioned_mobile is None:
        mentioned_mobile = []
    if mentioned_id is None:
        mentioned_id = []

    if not webhook_url:
        print(f"URL Not Set!")
        return

    msg = f"{machine_name}\n" f"{msg}"

    headers = {"Content-Type": "application/json"}
    data = {"msgtype": "text", "text": {"content": msg}}

    if mentioned_id:
        data["text"]["mentioned_list"] = mentioned_id
    if mentioned_mobile:
        data["text"]["mentioned_mobile_list"] = mentioned_mobile

    r = requests.post(webhook_url, headers=headers, data=json.dumps(data))
    print("WeWork", "text", r.text)


msg_queue = []
thread_is_start = False

sleep_time_start = get_env_time("WEBHOOK_SLEEP_TIME_START", datetime.time(23, 0))
sleep_time_end = get_env_time("WEBHOOK_SLEEP_TIME_END", datetime.time(7, 30))


def send_text_thread():
    while True:
        if len(msg_queue) == 0:
            time_sleep(5)
            continue

        try:
            if my_time.is_within_time_range(sleep_time_start, sleep_time_end):
                time_sleep(60)
                continue

            current_msg = msg_queue[0]
            direct_send_text(
                current_msg[0], current_msg[1], current_msg[2], current_msg[3]
            )
            msg_queue.pop(0)
        except:
            time_sleep(60)


def send_text(webhook_url: str, msg: str, mentioned_id=None, mentioned_mobile=None):
    msg_queue.append((webhook_url, msg, mentioned_id, mentioned_mobile))
    global thread_is_start
    if not thread_is_start:
        thread_is_start = True
        threading.Thread(target=send_text_thread).start()


if __name__ == "__main__":
    import socket

    # 获取当前机器的名称
    machine_name = socket.gethostname()
    print("当前机器名称:", machine_name)

    formatted_time = my_time.get_now_time()
    print("当前时间:", formatted_time)

    # 发送测试数据
    send_text(
        f"GPU Monitor\n"
        f"\tMachine Name: {machine_name}\n"
        f"\tTime: {formatted_time}\n"
        f"Test Pass!\n",
        mentioned_id=["khm"],
    )

    # direct_send_markdown(
    #     f"# GPU Monitor\n"
    #     f"## Machine Name\n{machine_name}\n"
    #     f"## Time\n{formatted_time}\n"
    #     f"# Test Pass!\n"
    # )
