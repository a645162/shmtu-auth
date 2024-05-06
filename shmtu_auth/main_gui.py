# -*- coding: utf-8 -*-

from shmtu_auth.src.utils.logs import get_logger

logger = get_logger()

logger.info("Initializing libraries...")

from shmtu_auth.src.gui.gui_main_application import gui_main_application

if __name__ == '__main__':
    logger.info("GUI Main program is starting...")

    # Show GUI
    gui_main_application()
