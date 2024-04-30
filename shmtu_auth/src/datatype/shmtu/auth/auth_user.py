# -*- coding: utf-8 -*-

import datetime
from typing import List

program_support_list = ["校园网", "iSMU"]


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
    def to_string(support_types: List[int]) -> List[str]:
        support_types_str = []

        for support_type in support_types:
            if support_type == NetworkType.ChinaEdu:
                support_types_str.append("校园网")
            elif support_type == NetworkType.iSMU:
                support_types_str.append("iSMU")
            elif support_type == NetworkType.ChinaMobile:
                support_types_str.append("中国移动")
            elif support_type == NetworkType.ChinaUnicom:
                support_types_str.append("中国联通")

        return support_types_str

    @staticmethod
    def to_binary_list_by_name_list(support_types: List[str]) -> List[int]:
        support_types_int = []

        for support_type in support_types:
            if support_type == "校园网":
                support_types_int.append(NetworkType.ChinaEdu)
            elif support_type == "iSMU":
                support_types_int.append(NetworkType.iSMU)
            elif support_type == "中国移动":
                support_types_int.append(NetworkType.ChinaMobile)
            elif support_type == "中国联通":
                support_types_int.append(NetworkType.ChinaUnicom)

        return support_types_int

    @staticmethod
    def to_binary_by_binary_list(support_types: List[int]):
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
    in_use: bool = True

    user_name: str

    user_id: str
    password: str
    is_encrypted: bool = False

    support_type_list: List[int]
    support_type_binary: int
    support_type_str_list: List[str]
    support_type_str: str

    expire_date: datetime.date
    expire_date_int: int
    expire_date_str: str

    def __init__(
            self,
            user_id: str = "",
            user_name: str = "",
            password: str = "",
            support_type_list: List[int] = None,
            expire_date: datetime.date = datetime.date.today(),
    ):
        self.user_id = user_id
        self.user_name = user_name
        self.password = password

        self.support_type_list = support_type_list
        if self.support_type_list is None:
            self.support_type_list = [NetworkType.ChinaEdu]

        self.expire_date = expire_date

        self.update_auto_generate_info()

    def update_auto_generate_info(self) -> None:
        self.expire_date_str = self.expire_date.strftime("%Y-%m-%d")
        self.expire_date_int = (
                self.expire_date.year * (10 ** 4) +
                self.expire_date.month * (10 ** 2) +
                self.expire_date.day
        )

        self.support_type_binary = \
            NetworkType.to_binary_by_binary_list(self.support_type_list)
        self.support_type_str_list = \
            NetworkType.to_string(self.support_type_list)
        self.support_type_str = \
            " ".join(self.support_type_str_list).strip()

    def to_list(self) -> List[str]:
        return [
            self.user_id, self.user_name, self.password,
            self.support_type_str, self.expire_date_str, str(self.is_valid())
        ]

    def __iter__(self):
        return iter(self.to_list())

    # 比较运算符
    def __eq__(self, other) -> bool:
        return self.user_id == other.user_id

    def __ne__(self, other) -> bool:
        return self.user_id != other.user_id

    def __lt__(self, other) -> bool:
        return self.expire_date_int < other.expire_date_int

    def __gt__(self, other) -> bool:
        return self.expire_date_int > other.expire_date_int

    def __le__(self, other) -> bool:
        return self.expire_date_int <= other.expire_date_int

    def __ge__(self, other) -> bool:
        return self.expire_date_int >= other.expire_date_int

    # 检测是否有效
    def is_valid(self) -> bool:
        self.user_id = self.user_id.strip()
        self.user_name = self.user_name.strip()
        self.password = self.password.strip()

        valid = self.in_use

        valid = valid and (
                self.user_id != "" and
                self.user_name != "" and
                self.password != ""
        )

        valid = valid and (
                self.user_id.isdigit() and
                len(self.user_id) == 12
        )

        return valid

    def get_support_type(self):
        pass


def generate_test_user_list(count: int = 10) -> List[UserItem]:
    user_list: List[UserItem] = []

    for i in range(count // 4):
        user = UserItem(
            user_id="2024123{:05d}".format(i),
            user_name=f"User_{i}",
            password=f"password_{i}",
            support_type_list=[
                NetworkType.ChinaEdu,
                NetworkType.iSMU
            ],
            expire_date=datetime.date.today()
        )

        if user not in user_list:
            user_list.append(user)

    for i in range(count // 2):
        user = UserItem(
            user_id="2024123{:05d}".format(i),
            user_name=f"User_{i}",
            password=f"password_{i}",
            support_type_list=[NetworkType.ChinaEdu],
            expire_date=datetime.date.today()
        )

        if user not in user_list:
            user_list.append(user)

    for i in range(count):
        user = UserItem(
            user_id="2024123{:05d}".format(i),
            user_name=f"User_{i}",
            password=f"password_{i}",
            support_type_list=[NetworkType.iSMU],
            expire_date=datetime.date.today()
        )

        if user not in user_list:
            user_list.append(user)

    return user_list


def convert_to_list_list(user_list: List[UserItem]) -> List[List[str]]:
    return [list(user) for user in user_list]
