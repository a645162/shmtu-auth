# -*- coding: utf-8 -*-

from qfluentwidgets import BodyLabel


class FBodyLabel(BodyLabel):
    def __init__(self, text: str, parent=None):
        super().__init__(parent)
        self.setText(text)
