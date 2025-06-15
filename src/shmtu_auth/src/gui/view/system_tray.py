# -*- coding: utf-8 -*-

from PySide6.QtGui import QAction, QIcon, QKeySequence, QShortcut
from PySide6.QtWidgets import QApplication, QMainWindow, QSystemTrayIcon

from qfluentwidgets import RoundMenu, Action
from qfluentwidgets import FluentIcon as FIF

from shmtu_auth.src.gui.common.config import cfg
from shmtu_auth.src.utils.logs import get_logger

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
        self._auth_status_action = QAction()

        # 托盘图标
        self.tray_icon = QSystemTrayIcon(self.window)
        # 设置托盘的属性
        self.tray_icon.setIcon(QIcon(":/gui/Logo32"))
        self.tray_icon.setToolTip("SHMTU Auth - 校园网认证助手")

        # 连接系统托盘图标的激活事件
        self.tray_icon.activated.connect(
            lambda reason: self.__on_tray_icon_activated(reason)
        )

        self.__create_menu_action()
        self.tray_icon.setContextMenu(self._tray_icon_menu)

        self.tray_icon.show()

        # 应用程序键盘监听
        self.__listen_keyboard()

        logger.info("系统托盘初始化完成")

    def show_notification(self, title: str, message: str, duration: int = 3000):
        """显示托盘通知"""
        if cfg.show_tray_notifications.value and self.tray_icon.supportsMessages():
            self.tray_icon.showMessage(
                title, message, QSystemTrayIcon.MessageIcon.Information, duration
            )
            logger.info(f"显示托盘通知: {title} - {message}")

    def update_auth_status(self, is_running: bool, is_online: bool = None):
        """更新认证状态显示"""
        if is_running:
            self._auth_status_action.setText("认证服务: 运行中 ✓")
            self.tray_icon.setToolTip("SHMTU Auth - 认证服务运行中")
        else:
            self._auth_status_action.setText("认证服务: 已停止 ✗")
            self.tray_icon.setToolTip("SHMTU Auth - 认证服务已停止")

        if is_online is not None:
            if is_online:
                self.tray_icon.setToolTip(f"{self.tray_icon.toolTip()} | 网络已连接")
            else:
                self.tray_icon.setToolTip(f"{self.tray_icon.toolTip()} | 网络未连接")

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
        """托盘图标点击事件处理"""
        logger.debug(f"托盘图标激活事件: {reason}")

        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            # 单击事件
            logger.debug("托盘图标单击")

        elif reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            # 双击事件
            logger.debug("托盘图标双击")

            action = cfg.tray_double_click_action.value
            if action == "show_hide":
                self.__show_or_hide_window()
            elif action == "show_only":
                self.__restore_from_tray()
            elif action == "hide_only":
                self.window.hide()

        elif reason == QSystemTrayIcon.ActivationReason.MiddleClick:
            # 中键点击
            logger.debug("托盘图标中键点击")

        elif reason == QSystemTrayIcon.ActivationReason.Context:
            # 右键点击 - 显示上下文菜单
            logger.debug("托盘图标右键点击")

    def __create_menu_action(self):
        """创建托盘菜单"""
        # 认证状态显示
        self._auth_status_action = Action(FIF.INFO, "认证服务: 未知")
        self._auth_status_action.setEnabled(False)  # 只用于显示状态，不可点击

        self._restore_action = Action(FIF.LINK, "显示主窗口")
        self._restore_action.triggered.connect(lambda: self.__restore_from_tray())

        # 快速操作
        self._quick_test_action = Action(FIF.SYNC, "快速测试网络")
        self._quick_test_action.triggered.connect(self.__quick_network_test)

        self._quit_action = Action(FIF.CLOSE, "退出程序")
        self._quit_action.triggered.connect(self.__quit_application)

        # 添加到菜单
        self._tray_icon_menu.addAction(self._auth_status_action)
        self._tray_icon_menu.addSeparator()
        self._tray_icon_menu.addAction(self._restore_action)
        self._tray_icon_menu.addAction(self._quick_test_action)
        self._tray_icon_menu.addSeparator()
        self._tray_icon_menu.addAction(self._quit_action)

    def __quick_network_test(self):
        """快速网络测试"""
        logger.info("从托盘执行快速网络测试")
        try:
            from shmtu_auth.src.core.core_exp import check_is_connected

            is_connected = check_is_connected()

            if is_connected:
                self.show_notification("网络测试", "网络连接正常 ✓")
            else:
                self.show_notification("网络测试", "网络连接异常，需要认证 ✗")

        except Exception as e:
            logger.error(f"快速网络测试失败: {str(e)}")
            self.show_notification("网络测试", f"测试失败: {str(e)}")

    def __quit_application(self):
        """退出应用程序"""
        logger.info("从托盘退出应用程序")

        try:
            # 调用主窗口的强制退出方法
            self.window.force_quit()

            # 等待一下，然后检查是否退出
            from PySide6.QtCore import QTimer

            QTimer.singleShot(1000, self.__force_quit_if_needed)

        except Exception as e:
            logger.error(f"托盘退出失败: {e}")
            self.__force_quit_if_needed()

    def __force_quit_if_needed(self):
        """如果程序还没退出，强制退出"""
        logger.info("检查程序是否需要强制退出")
        try:
            if QApplication.instance():
                logger.info("强制退出应用程序")
                QApplication.instance().quit()
        except Exception as e:
            logger.error(f"强制退出失败: {e}")
            import sys

            logger.info("使用sys.exit强制退出")
            sys.exit(0)

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
