# -*- coding: utf-8 -*-

from src.gui.gui_main_application import gui_main_application

from src.utils.logs import get_logger

logger = get_logger()


def start_backend():
    # 这个方案否决了！
    # 既然做GUI了，那么如果仅仅是一个配置编辑器，那也太没意思了。
    pass


if __name__ == '__main__':
    logger.info("GUI Main program is starting...")

    # Start Backend
    start_backend()

    # Show GUI
    gui_main_application()
