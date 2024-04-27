# -*- coding: utf-8 -*-

import datetime
import os.path
from typing import List

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QApplication, QFrame, QVBoxLayout, QLabel, QWidget, QHBoxLayout, QTreeWidgetItem, \
    QTreeWidgetItemIterator, QTableWidgetItem, QPushButton, QLineEdit, QSizePolicy
from qfluentwidgets import (FluentIcon, IconWidget, FlowLayout, isDarkTheme,
                            Theme, applyThemeColor, SmoothScrollArea, SearchLineEdit, StrongBodyLabel,
                            BodyLabel, TreeWidget, TableWidget, PasswordLineEdit, LineEdit, DateEdit, ZhDatePicker,
                            PushButton, MessageBoxBase, SubtitleLabel, Dialog, RoundMenu, Action)
from qfluentwidgets import FluentIcon as FIF

from .gallery_interface import GalleryInterface
from ...common.config import cfg

import pickle

from ...components.list_checkbox_widget import ListCheckboxWidgets
from ....config.project_directory import (
    get_directory_config_path,
    get_directory_data_path
)
from ....datatype.shmtu.auth.auth_user import UserItem, generate_test_user_list, convert_to_list_list

pickle_user_list_path = "user_list.pickle"
pickle_user_list_path = os.path.join(
    get_directory_data_path(),
    pickle_user_list_path
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
    # Signal Slot
    onModifyButtonClick = Signal()

    layout: QVBoxLayout

    input_user_id: LineEdit
    input_user_name: LineEdit
    input_password: PasswordLineEdit

    checkbox_support_type: ListCheckboxWidgets

    expire_date: ZhDatePicker

    button_save: PushButton

    def __init__(self, parent=None):
        super().__init__(parent)

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

        self.expire_date = ZhDatePicker(self)

        self.button_save = PushButton("保存")
        self.button_save.clicked.connect(self._button_save)

    def _button_save(self):
        support_type = self.checkbox_support_type.get_selected_list()
        print(support_type)

        self.onModifyButtonClick.emit()

    def _init_layout(self):
        self.layout = QVBoxLayout(self)

        self.layout.addWidget(self.input_user_id)
        self.layout.addWidget(self.input_user_name)
        self.layout.addWidget(self.input_password)

        self.layout.addWidget(self.checkbox_support_type)

        self.layout.addWidget(self.expire_date)

        self.layout.addWidget(self.button_save)

        self.layout.setAlignment(Qt.AlignTop)
        self.layout.setContentsMargins(2, 0, 0, 0)

        self.setLayout(self.layout)


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

        self.countLineEdit.textChanged.connect(self._validate_count)

    def _validate_count(self, text: str):
        text = text.strip()

        is_valid = text.__len__() > 0
        is_valid = is_valid and text.isdigit()

        self.yesButton.setEnabled(is_valid)


class UserListInterface(GalleryInterface):
    table_widget: UserListTableFrame
    user_info_edit_widget: UserInfoEditWidget

    def __init__(self, parent=None):
        super().__init__(
            title="校园网(统一认证平台)账号列表",
            subtitle="Author:Haomin Kong",
            parent=parent
        )
        self.setObjectName('userListInterface')

        user_info_widget = QWidget(self)
        user_info_layout = QHBoxLayout()

        self.table_widget = UserListTableFrame(self)
        self.table_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table_widget.customContextMenuRequested.connect(self._show_context_menu)
        user_info_layout.addWidget(self.table_widget)

        self.user_info_edit_widget = UserInfoEditWidget(self)
        user_info_layout.addWidget(self.user_info_edit_widget)

        user_info_widget.setLayout(user_info_layout)
        self.vBoxLayout.addWidget(user_info_widget)

        button_generate_docker_config = PushButton("为服务器生成Docker配置")
        button_generate_docker_config.setFixedWidth(300)
        button_generate_docker_config.clicked.connect(self.generate_docker_config)
        self.vBoxLayout.addWidget(button_generate_docker_config)

        self.table_widget.itemSelectionChanged.connect(self._table_item_selected)
        self._table_item_selected()

    def _table_item_selected(self):
        selected_items = self.table_widget.selectedItems()
        column_count: int = self.table_widget.column_count
        # 因为有5列，因此len为5的倍数
        selected_items_count: int = \
            int(selected_items.__len__() / column_count)

        self.user_info_edit_widget.setEnabled(selected_items_count == 1)

        if selected_items_count == 0:
            return

        if selected_items_count > 1:
            return

        # 此时仅有一行被选中
        # index=0即该行的第一个单元格
        selected_item = selected_items[0]
        row_index = selected_item.row()

        print(row_index)

    def _show_context_menu(self, pos):
        # 获取选中的行数
        selected_items = self.table_widget.selectedItems()
        column_count: int = self.table_widget.column_count
        # 因为有5列，因此len为5的倍数
        selected_items_count: int = \
            int(selected_items.__len__() / column_count)

        # 生成右键菜单
        menu = RoundMenu(parent=self)

        menu.addAction(Action(FIF.ADD, "新建"))

        menu.addSeparator()

        action_clone = Action(FIF.COPY, "克隆")
        menu.addAction(action_clone)
        action_del = Action(FIF.CLOSE, "删除")
        menu.addAction(action_del)

        menu.addSeparator()

        action_move_up = Action(FIF.UP, "上移")
        menu.addAction(action_move_up)
        action_move_down = Action(FIF.DOWN, "下移")
        menu.addAction(action_move_down)

        menu.addSeparator()

        action_select_all = Action(FIF.ACCEPT, "全选")
        action_select_all.setEnabled(
            selected_items_count != self.table_widget.rowCount()
        )
        # action_select_all.triggered.connect(lambda: self.table_widget.selectAll())
        menu.addAction(action_select_all)

        action_select_cancel = Action(FIF.CANCEL, "取消选择")
        menu.addAction(action_select_cancel)

        menu.addSeparator()

        action_export_docker = Action(FIF.SEND_FILL, "导出Docker配置")
        menu.addAction(action_export_docker)

        # 设置是否可用
        action_export_docker.setEnabled(self.table_widget.rowCount() > 0)

        have_selected_item = selected_items_count != 0

        action_clone.setEnabled(have_selected_item)
        action_del.setEnabled(have_selected_item)

        action_move_up.setEnabled(have_selected_item)
        action_move_down.setEnabled(have_selected_item)

        action_select_cancel.setEnabled(have_selected_item)

        # pos.setX(pos.x() - int(menu.width() / 2))
        # pos.setY(pos.y() - int(menu.height() / 2))

        # 显示右键菜单
        menu.exec(self.mapToGlobal(pos), ani=True)

    def generate_docker_config(self):
        w = ServerCountMessageBox(self.window())

        if w.exec():
            print(w.countLineEdit.text())

            w = Dialog("提示", "生成成功，您是否需要打开目录？", self.window())
            w.setContentCopyable(True)
            if w.exec():
                pass
