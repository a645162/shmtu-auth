# coding:utf-8
from typing import List

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QApplication, QFrame, QVBoxLayout, QLabel, QWidget, QHBoxLayout, QTableWidgetItem, \
    QTableWidget
from qfluentwidgets import (FluentIcon, IconWidget, FlowLayout, isDarkTheme,
                            Theme, applyThemeColor, SmoothScrollArea, SearchLineEdit, StrongBodyLabel,
                            BodyLabel, TableWidget, InfoBar, InfoBarIcon, InfoBarPosition, PushButton)

from .gallery_interface import GalleryInterface
from ...common.config import cfg

import pickle


class LogInterface(GalleryInterface):

    def __init__(self, parent=None):
        super().__init__(
            title="程序日志",
            subtitle="Author:Haomin Kong",
            parent=parent
        )
        self.setObjectName('logInterface')

        infoBar = InfoBar(
            icon=InfoBarIcon.INFORMATION,
            title="提示",
            content="这里是程序的工作日志，仅用于反馈。非专业人员请忽略~",
            orient=Qt.Horizontal,
            isClosable=True,
            duration=-1,
            position=InfoBarPosition.NONE,
            parent=self
        )
        self.vBoxLayout.addWidget(infoBar)

        button_save_log = PushButton("导出日志")
        button_save_log.setFixedWidth(100)
        self.vBoxLayout.addWidget(button_save_log)

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

        # 禁止直接编辑
        self.setEditTriggers(TableWidget.NoEditTriggers)

    def add_record(self, time: str = "", event: str = "", status: str = ""):
        self.setRowCount(self.record_count + 1)

        current_record = [time, event, status]

        for j in range(current_record.__len__()):
            self.setItem(
                self.record_count, j,
                QTableWidgetItem(current_record[j])
            )

        self.record_count += 1
