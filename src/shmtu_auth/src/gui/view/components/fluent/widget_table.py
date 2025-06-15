# -*- coding: utf-8 -*-

from typing import List

from qfluentwidgets import TableWidget


class QFluentTableWidget(TableWidget):
    selected_items_count: int = 0
    selected_index: List[int] = []

    def __init__(self, parent=None):
        super().__init__(parent)

        self.__connect_slot()

    def __connect_slot(self):
        self.itemSelectionChanged.connect(self.__selected_item_changed)

    def __selected_item_changed(self):
        selected_items_obj = self.selectedItems()

        selected_index = []

        for item_obj in selected_items_obj:
            row_index = item_obj.row()
            if row_index not in selected_index:
                selected_index.append(row_index)

        self.selected_items_count = len(selected_index)

        self.selected_index.clear()
        self.selected_index.extend(selected_index)

    def swap_row(self, row1, row2):
        # 交换两行的所有单元格内容
        for col in range(self.columnCount()):
            item1 = self.takeItem(row1, col)
            item2 = self.takeItem(row2, col)
            self.setItem(row1, col, item2)
            self.setItem(row2, col, item1)

    def set_select_index_list(self, index: List[int]):
        self.clearSelection()
        for i in index:
            self.selectRow(i)

    def move_up(self, step: int = 1):
        selection_index = self.selected_index.copy()
        selection_index.sort()

        if self.selected_items_count == 0:
            return

        target_start_index = selection_index[0] - step
        if target_start_index < 0:
            target_start_index = 0

        for i in range(self.selected_items_count):
            ori_index = selection_index[i]

            for j in range(ori_index, target_start_index, -1):
                self.swap_row(j, j - 1)

            target_start_index += 1

        final_selection_index = []
        target_start_index -= self.selected_items_count
        for i in range(self.selected_items_count):
            final_selection_index.append(target_start_index + i)

        self.set_select_index_list(final_selection_index)

    def move_down(self, step: int = 1):
        selection_index = self.selected_index.copy()
        selection_index.sort(reverse=True)

        if self.selected_items_count == 0:
            return

        target_end_index = selection_index[0] + step
        if target_end_index >= self.rowCount():
            target_end_index = self.rowCount() - 1

        for i in range(self.selected_items_count):
            ori_index = selection_index[i]

            for j in range(ori_index, target_end_index, 1):
                self.swap_row(j, j + 1)

            target_end_index -= 1

        final_selection_index = []
        target_end_index += self.selected_items_count
        for i in range(self.selected_items_count):
            final_selection_index.append(target_end_index - i)

        self.set_select_index_list(final_selection_index)
