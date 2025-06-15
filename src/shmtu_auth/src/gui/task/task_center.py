# -*- coding: utf-8 -*-

from ..common.config import cfg
from .check_update import start_check_update_once_thread


def task_auto_start():
    if cfg.check_update_at_start_up.value:
        start_check_update_once_thread()
