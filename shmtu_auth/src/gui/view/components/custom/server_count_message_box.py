# -*- coding: utf-8 -*-

from PySide6.QtWidgets import QHBoxLayout
from qfluentwidgets import MessageBoxBase, SubtitleLabel, LineEdit, PushButton

from shmtu_auth.src.utils.system import is_dir_path_valid


class ServerCountMessageBox(MessageBoxBase):
    is_valid: dict = {}

    def __init__(self, parent=None):
        super().__init__(parent)

        self._init_widget()

    def _init_widget(self):
        ##############################################################
        self.titleLabel = SubtitleLabel("生成服务器配置", self)
        self.viewLayout.addWidget(self.titleLabel)
        ##############################################################
        horizontal_layout = QHBoxLayout()
        horizontal_layout.addStretch(1)

        self.pathLineEdit = LineEdit(self)
        self.pathLineEdit.setPlaceholderText("请输入保存目录的路径")
        self.pathLineEdit.setClearButtonEnabled(True)
        self.pathLineEdit.textChanged.connect(self._validate_path)
        self._validate_path(self.pathLineEdit.text())
        horizontal_layout.addWidget(self.pathLineEdit)

        select_path_button = PushButton("选择目录")
        select_path_button.clicked.connect(self._select_path)
        horizontal_layout.addWidget(select_path_button)

        self.viewLayout.addLayout(horizontal_layout)
        ##############################################################
        self.countLineEdit = LineEdit(self)
        self.countLineEdit.setPlaceholderText("请输入服务器的个数")
        self.countLineEdit.setText("1")
        self.countLineEdit.setClearButtonEnabled(True)
        self.countLineEdit.textChanged.connect(self._validate_count)
        self._validate_count(self.countLineEdit.text())
        self.viewLayout.addWidget(self.countLineEdit)
        ##############################################################
        self.yesButton.setText("生成")
        self.cancelButton.setText("取消")

        self.widget.setMinimumWidth(360)
        self.yesButton.setDisabled(True)

    def get_count(self) -> int:
        count_text = self.countLineEdit.text().strip()

        if count_text.isdigit():
            return int(count_text)

        return 1

    def _select_path(self):
        pass

    def _validate_path(self, text_path: str):
        text_path = text_path.strip()

        is_valid = text_path.__len__() > 0
        is_valid = is_valid and is_dir_path_valid(text_path)

        self.is_valid["path"] = is_valid

        self._update_button_status()

    def _validate_count(self, text_count: str):
        text_count = text_count.strip()

        is_valid = text_count.__len__() > 0
        is_valid = is_valid and text_count.isdigit()

        self.is_valid["count"] = is_valid

        self._update_button_status()

    def _update_button_status(self):
        is_valid = True

        for key in self.is_valid:
            is_valid = is_valid and self.is_valid[key]

        self.yesButton.setEnabled(is_valid)
