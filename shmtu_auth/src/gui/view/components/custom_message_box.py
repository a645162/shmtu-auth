# -*- coding: utf-8 -*-

from qfluentwidgets import MessageBoxBase, SubtitleLabel, LineEdit


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
