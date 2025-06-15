# -*- coding: utf-8 -*-

from typing import List, Optional

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QTableWidgetItem
from qfluentwidgets import TableWidget

from shmtu_auth.src.datatype.shmtu.auth.auth_user import (
    UserItem,
    convert_to_list_list,
    generate_test_user_list,
)
from shmtu_auth.src.gui.view.components.fluent.widget_table import QFluentTableWidget

table_header = ["学号", "姓名", "密码", "支持类型", "过期时间", "有效"]


class UserListTableWidget(QFluentTableWidget):
    slot_user_list_updated: Signal = Signal()

    column_count: int = len(table_header)

    user_list: Optional[List[UserItem]]

    def __init__(self, parent=None, user_list=None):
        super().__init__(parent)

        self.verticalHeader().hide()
        self.setBorderRadius(8)
        self.setBorderVisible(True)

        self.setColumnCount(self.column_count)
        self.setHorizontalHeaderLabels(table_header)

        self.user_list = user_list
        if self.user_list is None:
            self.user_list = generate_test_user_list(20)

        self.update_user_list()

        self.resizeColumnsToContents()

        # 禁止直接编辑
        self.setEditTriggers(TableWidget.EditTrigger.NoEditTriggers)

    def update_user_list(self):
        user_count = self.user_list.__len__()

        self.setRowCount(user_count)

        user_list: List[List[str]] = convert_to_list_list(self.user_list)

        for i, user_info_str_list in enumerate(user_list):
            for j in range(user_info_str_list.__len__()):
                text = user_info_str_list[j]

                # 密码用星号展示
                if j == 2:
                    text = "*" * len(text)

                self.setItem(i, j, QTableWidgetItem(text))

        self.resizeColumnsToContents()
        self.slot_user_list_updated.emit()
