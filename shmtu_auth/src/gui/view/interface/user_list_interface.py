# coding:utf-8
import datetime
from typing import List

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QApplication, QFrame, QVBoxLayout, QLabel, QWidget, QHBoxLayout, QTreeWidgetItem, \
    QTreeWidgetItemIterator, QTableWidgetItem, QPushButton, QLineEdit
from qfluentwidgets import (FluentIcon, IconWidget, FlowLayout, isDarkTheme,
                            Theme, applyThemeColor, SmoothScrollArea, SearchLineEdit, StrongBodyLabel,
                            BodyLabel, TreeWidget, TableWidget, PasswordLineEdit, LineEdit, DateEdit, ZhDatePicker,
                            PushButton, MessageBoxBase, SubtitleLabel, Dialog)

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

        button_generate_docker_config = PushButton("为服务器生成Docker配置")
        button_generate_docker_config.setFixedWidth(300)
        button_generate_docker_config.clicked.connect(self.generate_docker_config)
        self.vBoxLayout.addWidget(button_generate_docker_config)

    def generate_docker_config(self):
        w = ServerCountMessageBox(self.window())

        if w.exec():
            print(w.countLineEdit.text())

            w = Dialog("提示", "处理完毕！", self.window())
            w.setContentCopyable(True)
            w.exec()


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

        self.user_list = generate_test_user_list(10)

        self.update_user_list()

        self.resizeColumnsToContents()

        # 禁止直接编辑
        self.setEditTriggers(TableWidget.NoEditTriggers)

    def update_user_list(self):
        user_count = self.user_list.__len__()

        self.setRowCount(user_count)

        user_list: List[List[str]] = \
            convert_to_list_list(self.user_list)

        for i, user_info_str_list in enumerate(user_list):
            for j in range(user_info_str_list.__len__()):
                text = user_info_str_list[j]

                # 密码用星号展示
                if j == 2:
                    text = "*" * len(text)

                self.setItem(
                    i, j,
                    QTableWidgetItem(text)
                )


class UserInfoEditWidget(QWidget):
    input_user_name: LineEdit
    input_user_id: LineEdit
    input_password: PasswordLineEdit

    # support_type:

    expire_date: ZhDatePicker

    button_save: QPushButton

    def __init__(self, parent=None):
        super().__init__(parent)

        self.input_user_name = LineEdit(self)
        self.input_user_name.setText(self.tr("请输入姓名"))
        self.input_user_name.setClearButtonEnabled(True)

        self.input_user_id = LineEdit(self)
        self.input_user_id.setText(self.tr("请输入学号"))
        self.input_user_id.setClearButtonEnabled(True)

        self.input_password = PasswordLineEdit(self)
        self.input_password.setFixedWidth(230)
        self.input_password.setPlaceholderText("请输入密码")

        self.expire_date = ZhDatePicker(self)


class ServerCountMessageBox(MessageBoxBase):
    """ Custom message box """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.titleLabel = SubtitleLabel("生成服务器配置", self)
        self.countLineEdit = LineEdit(self)

        self.countLineEdit.setPlaceholderText("请输入服务器的个数")
        self.countLineEdit.setClearButtonEnabled(True)

        # add widget to view layout
        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.countLineEdit)

        # change the text of button
        self.yesButton.setText("生成")
        self.cancelButton.setText("取消")

        self.widget.setMinimumWidth(360)
        self.yesButton.setDisabled(True)

        self.countLineEdit.textChanged.connect(self._validateCount)

    def _validateCount(self, text: str):
        text = text.strip()

        is_valid = text.__len__() > 0
        is_valid = is_valid and text.isdigit()

        self.yesButton.setEnabled(is_valid)
