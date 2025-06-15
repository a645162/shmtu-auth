# -*- coding: utf-8 -*-

import os
import sys

# Ensure the src directory is in the Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from shmtu_auth.src.utils.logs import get_logger

logger = get_logger()

logger.info("Initializing libraries...")

from shmtu_auth.src.gui.gui_main_application import gui_main_application

if __name__ == "__main__":
    logger.info("GUI Main program is starting...")

    # Show GUI
    gui_main_application()
