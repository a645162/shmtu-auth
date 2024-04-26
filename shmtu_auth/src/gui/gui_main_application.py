# -*- coding: utf-8 -*-

import os
import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication

from .common.config import cfg
from .view.main_window import MainWindow


def gui_main_application():
    # enable dpi scale
    if cfg.get(cfg.dpiScale) != "Auto":
        os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "0"
        os.environ["QT_SCALE_FACTOR"] = str(cfg.get(cfg.dpiScale))

    # create application
    app = QApplication(sys.argv)
    app.setAttribute(Qt.AA_DontCreateNativeWidgetSiblings)

    # create Main Window
    w = MainWindow()
    w.show()

    app.exec()


if __name__ == '__main__':
    gui_main_application()
