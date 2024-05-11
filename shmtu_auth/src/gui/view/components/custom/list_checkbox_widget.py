# -*- coding: utf-8 -*-

from typing import List

from PySide6.QtWidgets import QWidget, QVBoxLayout
from qfluentwidgets import CheckBox


class ListCheckboxWidgets(QWidget):
    checkbox_data: dict = {}
    layout: QVBoxLayout

    def __init__(self, parent=None, data_list: List = None):
        super().__init__(parent)

        self.__init_data(data_list)
        self.__init_checkbox()

    def __init_data(self, data_list: List = None):
        if data_list is None:
            raise "List Checkbox Widget data must be a list"

        for item in data_list:
            if isinstance(item, str):
                item_name = str(item).strip()

                self.checkbox_data[item_name] = {
                    "default": False,
                    "status": False,
                    "enable": True,
                }
            if isinstance(item, dict):
                item_name = str(item["name"]).strip()

                default_value = False
                if "default" in item:
                    default_value = item["default"]

                enable_value = True
                if "enable" in item and isinstance(item["enable"], bool):
                    enable_value = item["enable"]

                self.checkbox_data[item_name] = {
                    "default": default_value,
                    "status": default_value,
                    "enable": enable_value,
                }

    def __init_checkbox(self):
        self.layout = QVBoxLayout()

        def __update_checkbox_data(state: bool, dict_key: str):
            if isinstance(state, bool):
                self.checkbox_data[dict_key]["status"] = state
            if isinstance(state, int):
                self.checkbox_data[dict_key]["status"] = state == 2

        for key in self.checkbox_data.keys():
            current_checkbox = CheckBox()
            current_checkbox.setText(key)

            default_state = self.checkbox_data[key]["default"]
            current_checkbox.setChecked(default_state)
            current_checkbox.setEnabled(self.checkbox_data[key]["enable"])
            __update_checkbox_data(state=default_state, dict_key=key)

            current_checkbox.stateChanged.connect(
                lambda state: __update_checkbox_data(state=state, dict_key=key)
            )

            self.checkbox_data[key]["widget"] = current_checkbox
            self.layout.addWidget(current_checkbox)

        self.setLayout(self.layout)

    def get_status(self) -> dict:
        return_data = {}

        for key in self.checkbox_data.keys():
            current_checkbox_dict: dict = self.checkbox_data[key]

            if "widget" in current_checkbox_dict:
                current_widget = current_checkbox_dict["widget"]
                state = current_widget.isChecked()
                current_checkbox_dict["status"] = state

                return_data[key] = state

        return return_data

    def set_status(self, key: str, status: bool) -> bool:
        if key in self.checkbox_data:
            if "widget" in self.checkbox_data[key]:
                self.checkbox_data[key]["status"] = status
                self.checkbox_data[key]["widget"].setChecked(status)
                return True
            return False
        else:
            return False

    def get_selected_list(self) -> List[str]:
        checkbox_status = self.get_status()

        return_list = []
        for key in checkbox_status.keys():
            if checkbox_status[key]:
                return_list.append(key)

        return return_list

    def set_selected_list_to_true(self, list_data: List[str]) -> None:
        for key in list_data:
            if key in self.checkbox_data:
                self.set_status(key=key, status=True)
            else:
                print(f"{key} not in checkbox data")
                return

    def set_selected_list(self, list_data: List[str]) -> None:
        for key in list_data:
            if key not in self.checkbox_data.keys():
                print(f"{key} not in checkbox data")

        for key in self.checkbox_data.keys():
            self.set_status(key=key, status=(key in list_data))
