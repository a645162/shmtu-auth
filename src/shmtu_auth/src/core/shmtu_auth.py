# -*- coding: utf-8 -*-

from shmtu_auth.src.core.core import ShmtuNetAuthCore

from shmtu_auth.src.utils.logs import get_logger
from shmtu_auth.src.utils.program_env_config import convert_number_to_star

logger = get_logger()


class ShmtuNetAuth(ShmtuNetAuthCore):
    def __init__(self):
        super().__init__()

    def login_by_list(self, user_list) -> bool:

        for user_3 in user_list:
            user_id = user_3[0]
            user_pwd = user_3[1]
            is_encrypt = user_3[2]

            status = self.login(user_id, user_pwd, is_encrypt)

            if status[0]:
                return True
            else:
                encrypt_id = convert_number_to_star(user_id)
                logger.exception(f"Login failed:{encrypt_id}")
                logger.exception(f"{status[1]}")

        return False

    def check_is_online(self):
        return self.test_net()
