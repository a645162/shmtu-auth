# -*- coding: utf-8 -*-

from PySide6.QtCore import QObject, Signal


class SignalBus(QObject):
    """ Signal bus """

    signal_log_new = Signal(str, str)

    signal_new_version = Signal(str)


signal_bus = SignalBus()


def log_new(event: str, status: str):
    signal_bus.signal_log_new.emit(event, status)
