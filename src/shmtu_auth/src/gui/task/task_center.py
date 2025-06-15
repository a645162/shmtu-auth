# -*- coding: utf-8 -*-

from shmtu_auth.src.gui.common.config import cfg
from shmtu_auth.src.gui.task.check_update import start_check_update_once_thread


def task_auto_start():
    if cfg.check_update_at_start_up.value:
        start_check_update_once_thread()
