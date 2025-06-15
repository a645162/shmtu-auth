# -*- coding: utf-8 -*-

from PySide6.QtWidgets import QHBoxLayout, QLabel
from qfluentwidgets import MessageBoxBase, SubtitleLabel, LineEdit, SpinBox

from shmtu_auth.src.gui.view.components.fluent.widget_push_button import FPushButton
from shmtu_auth.src.utils.system import is_dir_path_valid


class QLabelInDialog(QLabel):
    def __init__(self, text: str, parent=None):
        super().__init__(parent)
        self.setText(text)
        self.setStyleSheet(
            """
            QLabel {
                font-size: 14px;
                color: #333333;
            }
        """
        )


class ServerCountMessageBox(MessageBoxBase):
    is_valid: dict = {}

    def __init__(self, parent=None):
        super().__init__(parent)

        self.__init_widget()

    def __init_widget(self):
        ##############################################################
        self.titleLabel = SubtitleLabel("生成服务器配置", self)
        self.viewLayout.addWidget(self.titleLabel)
        ##############################################################
        horizontal_layout = QHBoxLayout()
        horizontal_layout.addStretch(1)

        horizontal_layout.addWidget(QLabelInDialog("请输入保存目录的路径", self))

        select_path_button = FPushButton(self, "选择目录")
        select_path_button.clicked.connect(self.__select_path)
        horizontal_layout.addWidget(select_path_button)

        self.path_line_edit = LineEdit(self)
        self.path_line_edit.setPlaceholderText("请输入保存目录的路径")
        self.path_line_edit.setClearButtonEnabled(True)
        self.path_line_edit.textChanged.connect(self.__validate_path)
        self.__validate_path(self.path_line_edit.text())

        self.viewLayout.addLayout(horizontal_layout)
        self.viewLayout.addWidget(self.path_line_edit)
        ##############################################################
        self.viewLayout.addWidget(QLabelInDialog("请输入服务器的个数", self))
        self.count_spin_box = SpinBox(self)
        self.count_spin_box.setRange(1, 100)
        self.count_spin_box.setValue(1)
        self.viewLayout.addWidget(self.count_spin_box)
        ##############################################################
        self.viewLayout.addWidget(QLabelInDialog("请输入每个服务器的用户个数", self))
        self.user_count_per_server_spin_box = SpinBox(self)
        self.user_count_per_server_spin_box.setRange(1, 100)
        self.user_count_per_server_spin_box.setValue(3)
        self.viewLayout.addWidget(self.user_count_per_server_spin_box)
        ##############################################################
        self.yesButton.setText("生成")
        self.cancelButton.setText("取消")

        self.widget.setMinimumWidth(360)
        self.yesButton.setDisabled(True)

    def get_count(self) -> int:
        return self.count_spin_box.value()

    def __select_path(self):
        self.path_line_edit.setText("")

    def __validate_path(self, text_path: str):
        text_path = text_path.strip()

        is_valid = text_path.__len__() > 0
        is_valid = is_valid and is_dir_path_valid(text_path)

        self.is_valid["path"] = is_valid

        self.__update_button_status()

    def __update_button_status(self):
        is_valid = True

        for key in self.is_valid:
            is_valid = is_valid and self.is_valid[key]

        self.yesButton.setEnabled(is_valid)
