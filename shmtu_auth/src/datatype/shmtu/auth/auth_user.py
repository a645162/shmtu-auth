import datetime
from typing import List


class NetworkType:
    # One Hot Coded Network Type

    # 0001
    ChinaEdu: int = \
        1 << 0

    # 0010
    iSMU: int = \
        1 << 1

    # 0100
    ChinaMobile: int = \
        1 << 2

    # 1000
    ChinaUnicom: int = \
        1 << 3

    @staticmethod
    def to_binary(support_types: List[int]):
        return sum(support_type for support_type in support_types)

    @staticmethod
    def from_binary(binary_code) -> List[int]:
        selected_types = []
        if binary_code & NetworkType.ChinaEdu:
            selected_types.append(NetworkType.ChinaEdu)
        if binary_code & NetworkType.ChinaMobile:
            selected_types.append(NetworkType.ChinaMobile)
        if binary_code & NetworkType.ChinaUnicom:
            selected_types.append(NetworkType.ChinaUnicom)
        return selected_types


class UserItem:
    user_id: str
    user_name: str
    password: str
    support_type: List[int]
    expire_date_str: str
    expire_data_time: datetime.datetime

    def __init__(
            self,
            userId: str = "",
            userName: str = "",
            password: str = "",
            supportType=None,
            expireDataTime: datetime.datetime = datetime.datetime.now(),
    ):
        self.user_id = userId
        self.user_name = userName
        self.password = password

        self.support_type = supportType
        if self.support_type is None:
            self.support_type = [NetworkType.ChinaEdu]

        self.expire_data_time = expireDataTime

        self.convert_datetime_to_str()

    def convert_datetime_to_str(self):
        self.expire_date_str = self.expire_data_time.strftime("%Y-%m-%d %H:%M:%S")

    def to_list(self) -> List[str]:
        return [
            self.user_id, self.user_name, self.password,
            self.support_type, self.expire_date_str, str(self.is_valid())
        ]

    def __iter__(self):
        return iter(self.to_list())

    def is_valid(self) -> bool:
        self.user_id = self.user_id.strip()
        self.user_name = self.user_name.strip()
        self.password = self.password.strip()

        valid = self.user_id != "" and self.user_name != "" and self.password != ""

        valid = valid and self.user_id.isdigit() and len(self.user_id) == 12

        return valid


def generate_test_user_list(count: int = 10) -> List[UserItem]:
    user_list: List[UserItem] = []

    for i in range(count):
        user = UserItem()
        user.user_id = "2024123{:05d}".format(i)
        user.user_name = f"User_{i}"
        user.password = f"password_{i}"
        user.support_type = "校园网"
        user.expire_data_time = datetime.datetime.now()
        user.convert_datetime_to_str()
        user_list.append(user)

    return user_list


def convert_to_list_list(user_list: List[UserItem]) -> List[List[str]]:
    return [list(user) for user in user_list]
