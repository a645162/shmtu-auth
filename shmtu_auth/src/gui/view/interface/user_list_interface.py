# coding:utf-8
import datetime
from typing import List

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QApplication, QFrame, QVBoxLayout, QLabel, QWidget, QHBoxLayout, QTreeWidgetItem, \
    QTreeWidgetItemIterator, QTableWidgetItem
from qfluentwidgets import (FluentIcon, IconWidget, FlowLayout, isDarkTheme,
                            Theme, applyThemeColor, SmoothScrollArea, SearchLineEdit, StrongBodyLabel,
                            BodyLabel, TreeWidget, TableWidget)

from .gallery_interface import GalleryInterface
from ...common.config import cfg


class UserListInterface(GalleryInterface):

    def __init__(self, parent=None):
        super().__init__(
            title="校园网(统一认证平台)账号列表",
            subtitle="Author:Haomin Kong",
            parent=parent
        )
        self.setObjectName('userListInterface')

        table_widget = UserListTableFrame(self)

        self.vBoxLayout.addWidget(table_widget)


class NetworkType:
    # 0001
    ChinaEdu: int = 1 << 0

    # 0010
    ChinaMobile: int = 1 << 1

    # 0100
    ChinaUnicom: int = 1 << 2

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


def gengerate_test_user_list(count: int = 10) -> List[UserItem]:
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


class UserListTableFrame(TableWidget):
    user_list: List[UserItem]

    def __init__(self, parent=None):
        super().__init__(parent)

        self.verticalHeader().hide()
        self.setBorderRadius(8)
        self.setBorderVisible(True)

        self.setColumnCount(5)
        # self.setRowCount(60)
        self.setHorizontalHeaderLabels([
            self.tr("学号"),
            self.tr("姓名"),
            self.tr("密码"),
            self.tr("支持类型"),
            self.tr("过期时间")
        ])

        self.user_list = gengerate_test_user_list(10)

        self.update_user_list()

        self.resizeColumnsToContents()

    def update_user_list(self):
        user_count = self.user_list.__len__()

        self.setRowCount(user_count)

        user_list: List[List[str]] = \
            convert_to_list_list(self.user_list)

        for i, user_info_str_list in enumerate(user_list):
            for j in range(user_info_str_list.__len__()):
                self.setItem(
                    i, j,
                    QTableWidgetItem(user_info_str_list[j])
                )
