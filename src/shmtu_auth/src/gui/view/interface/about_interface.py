# -*- coding: utf-8 -*-

from qfluentwidgets import HorizontalFlipView

from shmtu_auth.src.gui.view.interface.gallery_interface import GalleryInterface

from shmtu_auth.src.utils.logs import get_logger

logger = get_logger()


class AboutInterface(GalleryInterface):

    def __init__(self, parent=None):
        super().__init__(
            title="关于本程序", subtitle="Author:Haomin Kong", parent=parent
        )
        self.setObjectName("aboutInterface")

        horizontal_flip_view = HorizontalFlipView(self)
        horizontal_flip_view.setFixedSize(500, 500)
        horizontal_flip_view.addImages(
            [
                ":/about/flip/current/1",
                ":/about/flip/current/2",
            ]
        )

        self.vBoxLayout.addWidget(horizontal_flip_view)
