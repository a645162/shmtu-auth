# -*- coding: utf-8 -*-

import threading

from shmtu_auth.src.gui.software import program_update

from shmtu_auth.src.gui.common.signal_bus import signal_bus, log_new


class CheckUpdateOnceThread(threading.Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        latest_version = program_update.get_latest_version()

        if len(latest_version) == 0:
            log_new("Update", "Get Latest Version Failed.")

        signal_bus.signal_new_version.emit(latest_version)


def start_check_update_once_thread():
    check_update_thread = CheckUpdateOnceThread()
    check_update_thread.start()
