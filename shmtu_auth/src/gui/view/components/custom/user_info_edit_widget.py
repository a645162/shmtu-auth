# -*- coding: utf-8 -*-

from typing import List
import datetime

from PySide6.QtCore import Signal, Qt, QDate
from PySide6.QtWidgets import QWidget, QVBoxLayout
from qfluentwidgets import (
    PushButton, LineEdit, PasswordLineEdit,
    ZhDatePicker,
    TeachingTip, TeachingTipTailPosition, InfoBarIcon,
)

from shmtu_auth.src.datatype.shmtu.auth.auth_user import UserItem, NetworkType
from shmtu_auth.src.gui.common.components.list_checkbox_widget import ListCheckboxWidgets


# Convert datetime.date to QDate
def convert_date_to_qdate(date: datetime.date) -> QDate:
    return QDate(date.year, date.month, date.day)


# Convert QDate to datetime.date
def convert_qdate_to_date(qdate: QDate) -> datetime.date:
    return datetime.date(qdate.year(), qdate.month(), qdate.day())


class UserInfoEditWidget(QWidget):
    # Signal Slot
    # Send
    onModifyButtonClick = Signal()
    # Receive
    onSelectedItemChanged = Signal()

    layout: QVBoxLayout

    input_user_id: LineEdit
    input_user_name: LineEdit
    input_password: PasswordLineEdit

    checkbox_support_type: ListCheckboxWidgets

    widget_expire_date: ZhDatePicker

    button_save: PushButton

    # Data
    user_list: List[UserItem]
    selected_index: List[int]

    def __init__(
            self, parent=None,
            user_list: List[UserItem] = None,
            selected_index: List[int] = None
    ):
        super().__init__(parent)

        self.user_list = user_list
        self.selected_index = selected_index

        self.setFixedWidth(250)

        self._init_widget()
        self._init_layout()

    def _init_widget(self):
        self.input_user_id = LineEdit(self)
        self.input_user_id.setText("")
        self.input_user_id.setPlaceholderText("请输入学号")
        self.input_user_id.setClearButtonEnabled(True)

        self.input_user_name = LineEdit(self)
        self.input_user_name.setText("")
        self.input_user_name.setPlaceholderText("请输入姓名")
        self.input_user_name.setClearButtonEnabled(True)

        self.input_password = PasswordLineEdit(self)
        self.input_password.setFixedWidth(230)
        self.input_password.setPlaceholderText("请输入密码")

        self.checkbox_support_type = \
            ListCheckboxWidgets(
                self,
                [
                    {"name": "校园网", "default": True},
                    {"name": "iSMU", "default": False},
                ]
            )

        self.widget_expire_date = ZhDatePicker(self)

        self.button_save = PushButton("保存修改")
        self.button_save.clicked.connect(self._button_save)

        # 连接接收的信号槽
        self.onSelectedItemChanged.connect(self._selection_changed)
        self._selection_changed()

    def _init_layout(self):
        self.layout = QVBoxLayout(self)

        self.layout.addWidget(self.input_user_id)
        self.layout.addWidget(self.input_user_name)
        self.layout.addWidget(self.input_password)

        self.layout.addWidget(self.checkbox_support_type)

        self.layout.addWidget(self.widget_expire_date)

        self.layout.addWidget(self.button_save)

        self.layout.setAlignment(Qt.AlignTop)
        self.layout.setContentsMargins(2, 0, 0, 0)

        self.setLayout(self.layout)

    def _selection_changed(self):
        print(self.selected_index)

        selection_count = len(self.selected_index)

        self.setEnabled(selection_count == 1)

        if selection_count == 0:
            return

        index = self.selected_index[0]
        self._update_input_box_data(index=index)

    def _before_save_blocker(self) -> bool:
        self.input_user_id.setText(self.input_user_id.text().strip())
        self.input_user_name.setText(self.input_user_name.text().strip())
        self.input_password.setText(self.input_password.text().strip())

        if (
                not self.input_user_id.text().isdigit() or
                len(self.input_user_id.text()) != 12
        ):
            TeachingTip.create(
                target=self.input_user_id,
                icon=InfoBarIcon.ERROR,
                title="错误",
                content="学号应该为12位！",
                isClosable=True,
                tailPosition=TeachingTipTailPosition.BOTTOM,
                duration=-1,
                parent=self
            )
            return False

        return True

    def _button_save(self):
        if not self._before_save_blocker():
            return

        support_type = \
            self.checkbox_support_type.get_selected_list()
        print(support_type)

        print(self.selected_index)

        self._modify_user_data(index=self.selected_index[0])

        self.onModifyButtonClick.emit()

    def _modify_user_data(self, index: int = 0):
        if index >= len(self.user_list):
            return

        current_item: UserItem = self.user_list[index]

        current_item.user_id = self.input_user_id.text()
        current_item.user_name = self.input_user_name.text()
        current_item.password = self.input_password.text()

        current_item.support_type_list = \
            NetworkType.to_binary_list_by_name_list(
                self.checkbox_support_type.get_selected_list()
            )

        current_item.expire_date = \
            convert_qdate_to_date(self.widget_expire_date.getDate())
        current_item.update_auto_generate_info()

    def _update_input_box_data(self, index: int = 0):
        if index >= len(self.user_list):
            return

        current_item: UserItem = self.user_list[index]

        self.input_user_id.setText(current_item.user_id)
        self.input_user_name.setText(current_item.user_name)
        self.input_password.setText(current_item.password)

        self.checkbox_support_type.set_selected_list(
            current_item.support_type_str_list
        )

        qDate = convert_date_to_qdate(current_item.expire_date)
        self.widget_expire_date.setDate(qDate)
