# -*- coding: utf-8 -*-

from typing import List

from qfluentwidgets import TableWidget


class QFluentTableWidget(TableWidget):
    selected_items_count: int = 0
    selected_index: List[int] = []

    def __init__(self, parent=None):
        super().__init__(parent)

        self._connect_slot()

    def _connect_slot(self):
        self.itemSelectionChanged.connect(self._selected_item_changed)

    def _selected_item_changed(self):
        selected_items_obj = self.selectedItems()

        selected_index = []
        for item_obj in selected_items_obj:
            row_index = item_obj.row()
            if row_index not in selected_index:
                selected_index.append(row_index)

        self.selected_items_count = len(selected_index)
        self.selected_index = selected_index
