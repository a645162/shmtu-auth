from typing import List

from PySide6.QtWidgets import QTableWidgetItem
from qfluentwidgets import TableWidget

from ....datatype.shmtu.auth.auth_user import (
    UserItem,
    convert_to_list_list,
    generate_test_user_list
)


class UserListTableFrame(TableWidget):
    column_count: int = 5

    user_list: List[UserItem]

    def __init__(self, parent=None):
        super().__init__(parent)

        self.verticalHeader().hide()
        self.setBorderRadius(8)
        self.setBorderVisible(True)

        self.setColumnCount(self.column_count)
        # self.setRowCount(60)
        self.setHorizontalHeaderLabels([
            "学号",
            "姓名",
            "密码",
            "支持类型",
            "过期时间"
        ])

        self.user_list = generate_test_user_list(20)

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
