# -*- coding: utf-8 -*-

from PySide6.QtGui import QAction, QIcon, QKeySequence, QShortcut
from PySide6.QtWidgets import QApplication, QMainWindow, QSystemTrayIcon

from qfluentwidgets import (RoundMenu, Action)
from qfluentwidgets import FluentIcon as FIF

from shmtu_auth.src..utils.logs import get_logger

logger = get_logger()


class SystemTray:
    window: QMainWindow

    def __init__(self, window: QMainWindow):
        super().__init__()

        self.window = window

        # 菜单
        self._tray_icon_menu = RoundMenu(parent=self.window)
        # 菜单项
        self._restore_action = QAction()
        self._quit_action = QAction()

        # 托盘图标
        self.tray_icon = QSystemTrayIcon(self.window)
        # 设置托盘的属性
        self.tray_icon.setIcon(QIcon(":/gui/Logo32"))
        self.tray_icon.setToolTip("shmtu-auth")

        # 连接系统托盘图标的激活事件
        self.tray_icon.activated.connect(
            lambda reason: self.__on_tray_icon_activated(reason)
        )

        self.__create_menu_action()
        self.tray_icon.setContextMenu(self._tray_icon_menu)

        self.tray_icon.show()

        # 应用程序键盘监听
        self.__listen_keyboard()

    def __restore_from_tray(self):
        logger.info("restore_from_tray")

        # 还原窗口
        if self.window.isMinimized():
            self.window.showNormal()
        elif self.window.isMaximized():
            self.window.showMaximized()
        else:
            self.window.show()

    def __on_tray_icon_activated(self, reason):
        # 当系统托盘图标被点击时的处理
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            # Handle left-click event
            logger.debug("Left-clicked on system tray icon")
        elif reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            # Handle double-click event
            logger.debug("Double-clicked on system tray icon")

            # 如果点击的是触发事件（比如左键单击），则还原窗口
            self.__show_or_hide_window()
        elif reason == QSystemTrayIcon.ActivationReason.MiddleClick:
            # Handle middle-click event
            logger.debug("Middle-clicked on system tray icon")
        elif reason == QSystemTrayIcon.ActivationReason.Context:
            # Handle right-click event
            logger.debug("Right-clicked on system tray icon")

    def __create_menu_action(self):
        self._restore_action = Action(FIF.LINK, "显示")
        self._restore_action.triggered.connect(
            lambda: self.__restore_from_tray()
        )

        self._quit_action = Action(FIF.CLOSE, "退出程序")
        self._quit_action.triggered.connect(QApplication.quit)

        self._tray_icon_menu.addAction(self._restore_action)
        self._tray_icon_menu.addSeparator()
        self._tray_icon_menu.addAction(self._quit_action)

    def __listen_keyboard(self):
        # 键盘监听
        shortcut = QShortcut(QKeySequence("Esc"), self.window)
        # 当按下 Esc 键时隐藏窗口
        shortcut.activated.connect(self.window.hide)

    def __show_or_hide_window(self):
        logger.debug("show_or_hide_window")
        if self.window.isVisible():
            logger.debug("hide_window")
            self.window.hide()
        else:
            logger.debug("show_window")
            self.window.show()
