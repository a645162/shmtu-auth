# -*- coding: utf-8 -*-

from typing import List

import threading
from time import sleep as time_sleep

from shmtu_auth.src.datatype.shmtu.auth.auth_user import UserItem, get_valid_user_list

from shmtu_auth.src.core.core_exp import check_is_connected
from shmtu_auth.src.core.shmtu_auth import ShmtuNetAuth

from shmtu_auth.src.gui.common.signal_bus import (
    log_new,
    auth_status_changed,
    auth_attempt,
    auth_success,
    auth_failed,
    auth_thread_started,
    auth_thread_stopped,
)


class AuthThread(threading.Thread):
    need_work = True

    user_list: List[UserItem]

    check_internet_interval: int

    check_internet_retry_times: int
    check_internet_retry_wait_time: int

    shmtu_auth_obj: ShmtuNetAuth

    def __init__(
        self,
        user_list: List[UserItem] = None,
        check_internet_interval: int = 60,
        check_internet_retry_times: int = 3,
        check_internet_retry_wait_time: int = 30,
    ):
        super().__init__()

        self.user_list = user_list
        if self.user_list is None:
            self.user_list = []
        self.user_list = get_valid_user_list(self.user_list)

        self.check_internet_interval = check_internet_interval

        self.check_internet_retry_times = check_internet_retry_times
        self.check_internet_retry_wait_time = check_internet_retry_wait_time

        self.shmtu_auth_obj = ShmtuNetAuth()

    def check_is_connected_retry(self):
        for i in range(self.check_internet_retry_times):
            if check_is_connected():
                return True
            else:
                for _ in range(self.check_internet_retry_wait_time):
                    if not self.need_work:
                        return False
                    time_sleep(1)
        return False

    def main_loop(self):
        # 检查状态
        network_status = self.check_is_connected_retry()
        # 阻塞任务后必须检查是否需要继续工作
        if not self.need_work:
            return

        # 更新状态
        if self.shmtu_auth_obj.isLogin != network_status:
            if network_status:
                log_new("Auth", "检测到网络已连接(状态变动)")
                auth_status_changed(True)
            else:
                log_new("Auth", "检测到网络未连接(状态变动)")
                auth_status_changed(False)

        self.shmtu_auth_obj.isLogin = network_status

        # 如果已经认证，直接跳过后续操作
        if network_status:
            return

        # 这里没有认证，因此要进行认证
        for user in self.user_list:
            # 实例化时已经过滤过了，按理来说这句话没啥用~
            if not user.is_valid():
                continue

            # 发送认证尝试信号
            auth_attempt(user.user_id)

            login_result = self.shmtu_auth_obj.login(
                user.user_id, user.password, user.is_encrypted
            )

            if login_result[0]:  # 登录成功
                auth_success(user.user_id)
                break
            else:  # 登录失败
                error_msg = login_result[1] if len(login_result) > 1 else "未知错误"
                auth_failed(user.user_id, error_msg)

    def run(self):
        if self.user_list is None or len(self.user_list) == 0:
            return

        # 发送线程启动信号
        auth_thread_started()

        while self.need_work:
            self.main_loop()

            for _ in range(self.check_internet_interval):
                if not self.need_work:
                    break
                time_sleep(1)

        # 发送线程停止信号
        auth_thread_stopped()

    def stop(self):
        self.need_work = False

    def check_is_stop(self):
        return self.is_alive()
