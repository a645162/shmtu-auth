# -*- coding: utf-8 -*-

from qfluentwidgets import PushButton


class FPushButton(PushButton):

    def __init__(self, parent=None, text: str = ""):
        super().__init__(parent)
        self.setText(text)
