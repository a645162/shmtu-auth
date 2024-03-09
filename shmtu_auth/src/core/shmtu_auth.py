from shmtuauth.src.core.core import ShmtuNetAuthCore


class ShmtuNetAuth(ShmtuNetAuthCore):
    def __init__(self):
        super().__init__()

    def login_by_list(self, user_list):
        for user_3 in user_list:
            id = user_3[0]
            pwd = user_3[1]
            is_encrypt = user_3[2]

            self.login(id, pwd, is_encrypt)

    def check_is_online(self):
        return self.test_net()
