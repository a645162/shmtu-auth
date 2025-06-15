# -*- coding: utf-8 -*-

from typing import List
import os.path
import datetime

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QTableWidgetItem
from qfluentwidgets import TableWidget, InfoBar, InfoBarIcon, InfoBarPosition

from shmtu_auth.src.gui.view.interface.gallery_interface import GalleryInterface
from shmtu_auth.src.gui.view.components.fluent.widget_push_button import FPushButton

import pickle

from shmtu_auth.src.config.project_directory import get_directory_data_path

from shmtu_auth.src.gui.common.signal_bus import signal_bus

from shmtu_auth.src.utils.logs import get_logger

logger = get_logger()

pickle_log_path = "logs.pickle"
pickle_log_path = os.path.join(get_directory_data_path(), pickle_log_path)


class LogInterface(GalleryInterface):

    def __init__(self, parent=None):
        super().__init__(title="程序日志", subtitle="Author:Haomin Kong", parent=parent)
        self.setObjectName("logInterface")

        info_bar = InfoBar(
            icon=InfoBarIcon.INFORMATION,
            title="提示",
            content="这里是程序的工作日志，仅用于反馈。非专业人员请忽略~",
            orient=Qt.Orientation.Horizontal,
            isClosable=True,
            duration=-1,
            position=InfoBarPosition.NONE,
            parent=self,
        )
        self.vBoxLayout.addWidget(info_bar)

        button_save_log = FPushButton(self, "导出日志")
        button_save_log.setFixedWidth(100)
        button_save_log.clicked.connect(self.export_logs)
        self.vBoxLayout.addWidget(button_save_log)

        self.logTable = LogTableFrame(self)
        self.vBoxLayout.addWidget(self.logTable)

    def add_new_record(self, time: str = "", event: str = "", status: str = ""):
        self.logTable.add_record(time=time, event=event, status=status)

    def export_logs(self):
        pass


class LogTableFrame(TableWidget):
    column_count = 3

    record_count = 0
    record_list: List[List[str]] = []

    def __init__(self, parent=None):
        super().__init__(parent)

        self.verticalHeader().hide()
        self.setBorderRadius(8)
        self.setBorderVisible(True)

        self.setColumnCount(self.column_count)
        self.setHorizontalHeaderLabels(
            [
                "日志时间",
                "事件",
                "状态",
            ]
        )

        # self.add_record("2024年01月01日 12:34:56", "检测到网络断开", "成功")

        self.resizeColumnsToContents()

        # 禁止直接编辑
        self.setEditTriggers(TableWidget.EditTrigger.NoEditTriggers)

        if os.path.exists(pickle_log_path):
            self.read_status()

        signal_bus.signal_log_new.connect(self.add_new_record)

    def add_new_record(self, event: str, status: str):
        now = datetime.datetime.now()
        time = now.strftime("%Y-%m-%d %H:%M:%S")
        self.add_record(time=time, event=event, status=status)

    def read_status(self):
        if not os.path.exists(pickle_log_path):
            return

        try:
            with open(pickle_log_path, "rb") as f:
                self.record_list = pickle.load(f)
        except Exception:
            return

        if self.record_list is not None:
            self.update_by_list()

    def save_status(self):
        with open(pickle_log_path, "wb") as f:
            pickle.dump(self.record_list, f)

    def update_record(self, index: int, current_record: List[str]):
        for j in range(min(current_record.__len__(), self.column_count)):
            current_text = current_record[j]
            self.setItem(index, j, QTableWidgetItem(current_text))

    def update_by_list(self, record_list: List[List[str]] = None):
        if record_list is not None:
            self.record_list = record_list.copy()

        self.record_count = self.record_list.__len__()

        self.setRowCount(self.record_count)

        for i, record_item in enumerate(self.record_list):
            self.update_record(i, record_item)

        self.resizeColumnsToContents()
        self.save_status()

    def add_record(self, time: str = "", event: str = "", status: str = ""):
        self.setRowCount(self.record_count + 1)

        # 生成结构化数据
        current_record = [time, event, status]

        # 添加到记录列表
        self.record_list.append(current_record)
        logger.info(f"添加日志记录：{str(current_record)}")

        # 更新UI
        self.update_record(self.record_count, current_record)

        self.record_count += 1

        self.resizeColumnsToContents()
        self.save_status()

        self.resizeColumnsToContents()
