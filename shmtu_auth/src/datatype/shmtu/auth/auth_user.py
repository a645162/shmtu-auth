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
    userId: str
    userName: str
    password: str
    supportType: List[int]
    expireTime: str
    expireDataTime: datetime.datetime

    def __init__(
            self,
            userId: str = "",
            userName: str = "",
            password: str = "",
            supportType=None,
            expireDataTime: datetime.datetime = datetime.datetime.now(),
    ):
        self.userId = userId
        self.userName = userName
        self.password = password

        self.supportType = supportType
        if self.supportType is None:
            self.supportType = [NetworkType.ChinaEdu]

        self.expireDataTime = expireDataTime

        self.convert_datetime_to_str()

    def convert_datetime_to_str(self):
        self.expireTime = self.expireDataTime.strftime("%Y-%m-%d %H:%M:%S")

    def to_list(self) -> List[str]:
        return [self.userId, self.userName, self.password, self.supportType, self.expireTime]

    def __iter__(self):
        return iter(self.to_list())


def generate_test_user_list(count: int = 10) -> List[UserItem]:
    user_list: List[UserItem] = []

    for i in range(count):
        user = UserItem()
        user.userId = "2024123{:05d}".format(i)
        user.userName = f"User_{i}"
        user.password = f"password_{i}"
        user.supportType = "校园网"
        user.expireDataTime = datetime.datetime.now()
        user.convert_datetime_to_str()
        user_list.append(user)

    return user_list


def convert_to_list_list(user_list: List[UserItem]) -> List[List[str]]:
    return [list(user) for user in user_list]
