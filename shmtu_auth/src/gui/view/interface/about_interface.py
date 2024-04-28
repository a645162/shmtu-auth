# -*- coding: utf-8 -*-

from qfluentwidgets import (HorizontalFlipView)

from .gallery_interface import GalleryInterface
from ...common.config import cfg

from ....utils.logs import get_logger

logger = get_logger()


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
