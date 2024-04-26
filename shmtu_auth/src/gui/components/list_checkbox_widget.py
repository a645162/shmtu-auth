# -*- coding: utf-8 -*-
from typing import List

from PySide6.QtWidgets import QWidget, QVBoxLayout


class ListCheckboxWidgets(QWidget):
    checkbox_data: dict = {}

    def __init__(self, parent=None, data_list: List = None):
        super().__init__(parent)
        self.init_data(data_list)

        layout = QVBoxLayout()

        self.setLayout(layout)

    def init_data(self, data_list: List = None):
        if data_list is None:
            raise "List Checkbox Widget data must be a list"

        for item in data_list:
            if isinstance(item, str):
                item_name = str(item).strip()

                self.checkbox_data[item_name] = {
                    "default": False,
                    "status": False,
                }
            if isinstance(item, dict):
                item_name = str(item["name"]).strip()

                default_value = False
                if "default" in item:
                    default_value = item["default"]

                self.checkbox_data[item_name] = {
                    "default": default_value,
                    "status": default_value,
                }

    def create_checkbox(self):
        for key in self.checkbox_data.keys():
            pass
            # current_checkbox= self.checkbox_data[key]

    def get_status(self) -> dict:
        return_data = {}

        for key in self.checkbox_data.keys():
            current_checkbox = self.checkbox_data[key]

            if "status" in current_checkbox:
                current_value = current_checkbox["status"]
                return_data[key] = current_value

        return return_data

    def get_selected_list(self) -> List[str]:
        checkbox_status = self.get_status()
        return_list = []
        for key in checkbox_status.keys():
            if checkbox_status[key]:
                return_list.append(key)

        return return_list
