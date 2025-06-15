# -*- coding: utf-8 -*-

import os
import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication

from shmtu_auth.src.gui.common.config import cfg
from shmtu_auth.src.gui.view.main_window import MainWindow

from shmtu_auth.src.utils.logs import get_logger

logger = get_logger()


def gui_main_application():
    logger.info("GUI Main Application is initializing...")

    # enable dpi scale
    if cfg.get(cfg.dpi_scale) != "Auto":
        os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "0"
        os.environ["QT_SCALE_FACTOR"] = str(cfg.get(cfg.dpi_scale))

    # create application
    app = QApplication(sys.argv)
    app.setAttribute(Qt.AA_DontCreateNativeWidgetSiblings)

    # create Main Window
    w = MainWindow()
    w.try_to_show()

    app.exec()


if __name__ == "__main__":
    gui_main_application()
