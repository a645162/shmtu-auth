# -*- coding: utf-8 -*-

from typing import List

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QApplication, QFrame, QVBoxLayout, QLabel, QWidget, QHBoxLayout
from qfluentwidgets import (FluentIcon, IconWidget, FlowLayout, isDarkTheme,
                            Theme, applyThemeColor, SmoothScrollArea, SearchLineEdit, StrongBodyLabel,
                            BodyLabel, HorizontalFlipView)

from .gallery_interface import GalleryInterface
from ...common.config import cfg


class AboutInterface(GalleryInterface):

    def __init__(self, parent=None):
        super().__init__(
            title="关于本程序",
            subtitle="Author:Haomin Kong",
            parent=parent
        )
        self.setObjectName('aboutInterface')

        horizontal_flip_view = HorizontalFlipView(self)
        horizontal_flip_view.addImages([
            ":/about/flip/current/1",
            ":/about/flip/current/2",
        ])
        self.addExampleCard(
            title="本项目",
            widget=horizontal_flip_view,
            sourcePath=""
        )

        # self.iconView = IconCardView(self)
        # self.vBoxLayout.addWidget(self.iconView)
