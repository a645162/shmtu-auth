# encoding: utf-8

from PySide6.QtGui import QAction, QIcon, QKeySequence, QShortcut
from PySide6.QtWidgets import QApplication, QMainWindow, QMenu, QSystemTrayIcon


class SystemTray:
    def __init__(self, window):
        super().__init__()

        self.window: QMainWindow = window

        # 初始化系统托盘相关的对象和菜单项
        self._restore_action = QAction()
        self._quit_action = QAction()
        self._tray_icon_menu = QMenu()

        self.tray_icon = QSystemTrayIcon(self.window)
        self.tray_icon.setIcon(QIcon(":/gui/Logo32"))
        self.tray_icon.setToolTip("shmtu-auth")

        self.create_menu_action()
        self.create_tray_icon()
        self.tray_icon.show()

        # 连接系统托盘图标的激活事件
        self.tray_icon.activated.connect(self.tray_icon_activated)

        # 应用程序键盘监听
        self.listen_keyboard()

    def minimize_to_tray(self):
        # 最小化窗口到系统托盘
        self.window.hide()

    def restore_from_tray(self):
        # 还原窗口
        if self.window.isMinimized():
            self.window.showNormal()
        elif self.window.isMaximized():
            self.window.showMaximized()
        else:
            self.window.show()

    def change_status(self):
        if self.window.isVisible():
            self.minimize_to_tray()
            return

        self.restore_from_tray()

    def tray_icon_activated(self, reason):
        # 当系统托盘图标被点击时的处理
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            # 如果点击的是触发事件（比如左键单击），则还原窗口
            self.restore_from_tray()
            # self.change_status()

    def create_menu_action(self):
        self._restore_action = QAction("显示", self.window)
        self._restore_action.triggered.connect(self.restore_from_tray)

        self._quit_action = QAction("退出", self.window)
        self._quit_action.triggered.connect(QApplication.quit)

    def create_tray_icon(self):
        # 创建系统托盘图标和上下文菜单
        self._tray_icon_menu = QMenu(self.window)
        self._tray_icon_menu.addAction(self._restore_action)
        self._tray_icon_menu.addSeparator()
        self._tray_icon_menu.addAction(self._quit_action)

        self.tray_icon.setContextMenu(self._tray_icon_menu)
        self.tray_icon.show()

    def listen_keyboard(self):
        # 键盘监听
        shortcut = QShortcut(QKeySequence("Esc"), self.window)
        # 当按下 Esc 键时隐藏窗口
        shortcut.activated.connect(self.window.hide)
