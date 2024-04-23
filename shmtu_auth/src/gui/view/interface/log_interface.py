# coding:utf-8
from typing import List

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QApplication, QFrame, QVBoxLayout, QLabel, QWidget, QHBoxLayout, QTableWidgetItem
from qfluentwidgets import (FluentIcon, IconWidget, FlowLayout, isDarkTheme,
                            Theme, applyThemeColor, SmoothScrollArea, SearchLineEdit, StrongBodyLabel,
                            BodyLabel, TableWidget)

from .gallery_interface import GalleryInterface
from ...common.config import cfg


class LogInterface(GalleryInterface):

    def __init__(self, parent=None):
        super().__init__(
            title="程序日志",
            subtitle="Author:Haomin Kong",
            parent=parent
        )
        self.setObjectName('logInterface')

        self.logTable = LogTableFrame(self)

        self.vBoxLayout.addWidget(self.logTable)


class LogTableFrame(TableWidget):
    record_count = 0

    def __init__(self, parent=None):
        super().__init__(parent)

        self.verticalHeader().hide()
        self.setBorderRadius(8)
        self.setBorderVisible(True)

        self.setColumnCount(3)
        self.setHorizontalHeaderLabels([
            self.tr("日志时间"),
            self.tr("事件"),
            self.tr("状态"),
        ])

        self.add_record("2024年01月01日 12:34:56", "检测到网络断开", "成功")

        self.resizeColumnsToContents()

    def add_record(self, time: str = "", event: str = "", status: str = ""):
        self.setRowCount(self.record_count + 1)

        current_record = [time, event, status]

        for j in range(current_record.__len__()):
            self.setItem(
                self.record_count, j,
                QTableWidgetItem(current_record[j])
            )

        self.record_count += 1
