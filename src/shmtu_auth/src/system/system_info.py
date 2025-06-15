# -*- coding: utf-8 -*-

import sys
import platform


class SystemType:
    @staticmethod
    def is_windows() -> bool:
        """
        判断当前系统是否为Windows
        :return:
        """
        return platform.system() == "Windows"

    @staticmethod
    def is_windows11():
        return sys.platform == "win32" and sys.getwindowsversion().build >= 22000

    @staticmethod
    def is_macos() -> bool:
        """
        判断当前系统是否为MacOS
        :return:
        """
        return platform.system() == "Darwin"

    @staticmethod
    def is_mac():
        return SystemType.is_macos()
