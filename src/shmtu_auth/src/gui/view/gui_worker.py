import threading
from typing import List, Optional
from time import sleep as time_sleep

from shmtu_auth.src.core.shmtu_auth import ShmtuNetAuth
from shmtu_auth.src.utils.program_env_config import (
    convert_number_to_star,
    convert_password_to_star,
)

from shmtu_auth.src.utils.logs import get_logger

logger = get_logger()


class GuiWorker:
    need_work: bool = False
    work_thread: Optional[threading.Thread] = None

    time_interval: int = 60
    user_list_3: List

    def __init__(self):
        pass

    def set_user_list_3(self, user_list_3: List):
        self.user_list_3 = user_list_3

    def create_thread(self):
        def monitor_auth():
            logger.info("Initializing...")
            net_auth = ShmtuNetAuth()

            user_list_3 = self.user_list_3

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

            while self.need_work:
                if not net_auth.check_is_online():
                    if net_auth.login_by_list(user_list_3):
                        logger.info("Login success.")
                    else:
                        logger.error("Login failed.")

                count = 0
                while self.need_work and count < self.time_interval:
                    count += 1
                    time_sleep(1)

        logger.info("Create Thread")
        self.work_thread = threading.Thread(target=monitor_auth)
        logger.info("Created Thread")

    def start_work(self):
        logger.info("Start Thread")
        self.need_work = True
        self.work_thread.start()
        logger.info("Thread Started.")

    def stop_work(self):
        self.need_work = False
        self.work_thread.join()
        self.work_thread = None

    def is_work(self):
        if self.work_thread is None:
            return False

        return self.work_thread.is_alive()
