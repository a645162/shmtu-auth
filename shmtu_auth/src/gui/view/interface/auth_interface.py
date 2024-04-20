# coding:utf-8
from typing import List

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QApplication, QFrame, QVBoxLayout, QLabel, QWidget, QHBoxLayout
from qfluentwidgets import (FluentIcon, IconWidget, FlowLayout, isDarkTheme,
                            Theme, applyThemeColor, SmoothScrollArea, SearchLineEdit, StrongBodyLabel,
                            BodyLabel)

from .gallery_interface import GalleryInterface
from ...common.config import cfg

class AuthInterface(GalleryInterface):
    """ Auth interface """
    def __init__(self, parent=None):
        super().__init__(
            title="上海海事大学校园网自动认证",
            subtitle="Author:Haomin Kong",
            parent=parent
        )
        self.setObjectName('authInterface')

        # self.iconView = IconCardView(self)
        # self.vBoxLayout.addWidget(self.iconView)
