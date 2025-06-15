# -*- coding: utf-8 -*-

from typing import List
from PySide6.QtCore import QUrl, QSize
from PySide6.QtGui import QIcon, QDesktopServices, QColor
from PySide6.QtWidgets import QApplication

from qfluentwidgets import (
    NavigationItemPosition,
    FluentWindow,
    SplashScreen,
    MessageBox,
)
from qfluentwidgets import FluentIcon as FIF

from shmtu_auth.src.gui.common.config import cfg, RELEASE_URL

from shmtu_auth.src.gui.view.interface.about_interface import AboutInterface
from shmtu_auth.src.gui.view.interface.log_interface import LogInterface
from shmtu_auth.src.gui.view.interface.user_list_interface import UserListInterface

from shmtu_auth.src.gui.view.interface.home_interface import HomeInterface
from shmtu_auth.src.gui.view.interface.auth_interface import AuthInterface
from shmtu_auth.src.gui.view.interface.settings_interface import SettingInterface

# 加载资源文件,虽然表面上没有调用(不可以移除!)
from shmtu_auth.src.gui.resource import resources

from shmtu_auth.src.gui.view.system_tray import SystemTray
from shmtu_auth.src.datatype.shmtu.auth.auth_user import UserItem

from shmtu_auth.src.gui.common.system_menu import init_system_menu
from shmtu_auth.src.gui.common.signal_bus import signal_bus, log_new

from shmtu_auth.src.gui.task.task_center import task_auto_start
from shmtu_auth.src.gui.software import program_update
from shmtu_auth.src.system.system_info import SystemType

from shmtu_auth.src.utils.logs import get_logger

logger = get_logger()

# dummy import for type hinting
resources


class MainWindow(FluentWindow):
    user_list: List[UserItem] = []

    def __init__(self):
        super().__init__()

        logger.info("MainWindow initializing...")

        self.__init_window()

        # create sub interface
        self.home_interface = HomeInterface(self)
        self.auth_interface = AuthInterface(self, self.user_list)
        self.user_list_interface = UserListInterface(self, self.user_list)
        self.log_interface = LogInterface(self)
        self.setting_interface = SettingInterface(self)
        self.about_interface = AboutInterface(self)

        # enable acrylic effect
        self.navigationInterface.setAcrylicEnabled(True)
        self.setCustomBackgroundColor(QColor(240, 244, 249), QColor(32, 32, 32))

        # add items to navigation interface
        self.__init_left_navigation_item()
        self.splash_screen.finish()

        log_new("Info", "MainWindow initialized.")

        logger.info("Start Auto Task.")
        task_auto_start()
        logger.info("Auto Task Finished.")

        # 处理认证服务自动启动（在所有界面初始化完成后）
        self.__handle_auth_auto_start()

    def __handle_auth_auto_start(self):
        """处理认证服务自动启动"""
        if cfg.auth_auto_start_work_thread.value:
            logger.info("配置了认证服务自动启动，准备启动...")
            # 延迟一点时间确保所有数据都已加载
            from PySide6.QtCore import QTimer

            QTimer.singleShot(
                1000, self.auth_interface._AuthInterface__on_work_button_clicked
            )
            logger.info("已安排认证服务自动启动")

    def __connect_tray_signals(self):
        """连接托盘相关信号"""
        # 连接认证状态信号到托盘更新
        signal_bus.signal_auth_thread_started.connect(
            lambda: self.system_tray.update_auth_status(True)
        )
        signal_bus.signal_auth_thread_stopped.connect(
            lambda: self.system_tray.update_auth_status(False)
        )
        signal_bus.signal_auth_status_changed.connect(
            lambda is_online: self.system_tray.update_auth_status(None, is_online)
        )
        signal_bus.signal_auth_success.connect(
            lambda user_id: self.system_tray.show_notification(
                "认证成功", f"用户 {user_id} 认证成功"
            )
        )
        signal_bus.signal_auth_failed.connect(
            lambda user_id, error: self.system_tray.show_notification(
                "认证失败", f"用户 {user_id} 认证失败"
            )
        )
        logger.info("托盘信号连接完成")

    def try_to_show(self):
        """根据配置显示或隐藏窗口"""
        if cfg.auto_minimize.value or cfg.silent_start.value:
            logger.info("根据配置自动隐藏到系统托盘")
            self.hide()
            if cfg.show_tray_notifications.value:
                self.system_tray.show_notification(
                    "SHMTU Auth", "程序已启动并隐藏到系统托盘"
                )
        else:
            self.show()

    def closeEvent(self, event):
        """重写关闭事件"""
        # 检查是否是从托盘强制退出
        force_quit = getattr(self, "_force_quit", False)

        if cfg.close_to_tray.value and not force_quit:
            logger.info("关闭按钮点击 - 最小化到托盘")
            event.ignore()
            self.hide()
            if cfg.show_tray_notifications.value:
                self.system_tray.show_notification(
                    "SHMTU Auth", "程序已最小化到系统托盘，双击托盘图标可恢复窗口"
                )
        else:
            logger.info("关闭按钮点击 - 退出程序")
            self.__cleanup_resources()
            event.accept()

    def __cleanup_resources(self):
        """清理程序资源"""
        logger.info("开始清理程序资源...")

        try:
            # 停止认证线程
            if hasattr(self, "auth_interface") and self.auth_interface.work_thread:
                if self.auth_interface.work_thread.is_alive():
                    logger.info("停止认证线程...")
                    self.auth_interface.work_thread.stop()
                    self.auth_interface.work_thread.join(timeout=3)
                    logger.info("认证线程已停止")

            # 隐藏托盘图标
            if hasattr(self, "system_tray"):
                self.system_tray.tray_icon.hide()
                logger.info("托盘图标已隐藏")

        except Exception as e:
            logger.error(f"清理资源时出错: {e}")

        logger.info("程序资源清理完成")

    def force_quit(self):
        """强制退出程序"""
        logger.info("强制退出程序")
        self._force_quit = True
        self.close()

    def changeEvent(self, event):
        """重写改变事件（处理最小化）"""
        if (
            event.type() == event.Type.WindowStateChange
            and self.isMinimized()
            and cfg.minimize_to_tray.value
        ):
            logger.info("窗口最小化 - 隐藏到托盘")
            self.hide()
            event.ignore()
        else:
            super().changeEvent(event)

    def __init_left_navigation_item(self):
        # add navigation items
        self.addSubInterface(self.home_interface, FIF.HOME, "主页")

        # 分隔线
        self.navigationInterface.addSeparator()

        pos = NavigationItemPosition.SCROLL
        self.addSubInterface(self.auth_interface, FIF.VPN, "校园网认证", pos)
        self.addSubInterface(self.user_list_interface, FIF.PEOPLE, "用户列表", pos)

        self.navigationInterface.addSeparator(pos)

        self.addSubInterface(self.log_interface, FIF.DATE_TIME, "工作日志", pos)

        # add custom widget to bottom
        self.navigationInterface.addItem(
            routeKey="github.io",
            icon=FIF.DOCUMENT,
            text="项目文档",
            onClick=lambda: QDesktopServices.openUrl(
                QUrl("https://a645162.github.io/shmtu-auth/")
            ),
            selectable=False,
            tooltip="项目文档",
            position=NavigationItemPosition.BOTTOM,
        )
        self.navigationInterface.addItem(
            routeKey="github",
            icon=FIF.GITHUB,
            text="项目源代码仓库",
            onClick=lambda: QDesktopServices.openUrl(
                QUrl("https://github.com/a645162/shmtu-auth")
            ),
            selectable=False,
            tooltip="官方网站",
            position=NavigationItemPosition.BOTTOM,
        )

        self.navigationInterface.addSeparator(position=NavigationItemPosition.BOTTOM)

        self.addSubInterface(
            self.setting_interface, FIF.SETTING, "设置", NavigationItemPosition.BOTTOM
        )
        self.addSubInterface(
            self.about_interface, FIF.INFO, "关于", NavigationItemPosition.BOTTOM
        )

    def __init_window(self):
        dpi_scale = cfg.get_dpi_ratio()
        logger.info(f"MainWindow DPI Scale: {dpi_scale}")

        default_width: int = int(800 * dpi_scale)
        default_height: int = int(600 * dpi_scale)

        # 适配MacBook的Retina屏幕
        # Mac设备的屏幕往往不是16:9且分辨率较高
        # 因此可以适当增大默认窗口大小，尤其是高度！
        if SystemType.is_macos():
            default_width = int(960 * dpi_scale)
            default_height = int(840 * dpi_scale)

        min_width: int = int(800 * dpi_scale)
        min_height: int = int(600 * dpi_scale)

        self.setMinimumWidth(min_width)
        self.setMinimumHeight(min_height)
        self.resize(default_width, default_height)

        self.setWindowIcon(QIcon(":/gui/Logo128"))
        self.setWindowTitle("shmtu-auth")

        # 直接关闭Mica云母特效(我的AMD Radeon RX 6800 显卡反正是显示有问题)
        self.setMicaEffectEnabled(False)

        # create splash screen
        self.splash_screen = SplashScreen(self.windowIcon(), self)
        self.splash_screen.setIconSize(QSize(106, 106))
        self.splash_screen.raise_()

        desktop = QApplication.screens()[0].availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)

        # 初始化系统托盘
        self.system_tray = SystemTray(self)

        # 连接信号以更新托盘状态
        self.__connect_tray_signals()

        self.try_to_show()

        QApplication.processEvents()

        # 连接信号槽
        self.__connect_to_global_slot()

        init_system_menu()

    def __connect_to_global_slot(self):
        signal_bus.signal_new_version.connect(self.__pop_up_new_version)

    def __pop_up_new_version(self, version: str):
        logger.info("Receive Signal New Version:", version)
        if not program_update.is_have_new_version():
            return

        current_version = program_update.PROGRAM_VERSION
        new_version = program_update.LATEST_VERSION

        title = "检测到新版本"
        content = (
            f"当前版本: {current_version}\n"
            f"最新版本: {new_version}\n"
            f"您是否需要前往官网下载?"
        )

        w = MessageBox(title, content, self)
        w.setContentCopyable(True)
        if w.exec():
            QDesktopServices.openUrl(QUrl(RELEASE_URL))

    def open_github_page(self):
        QDesktopServices.openUrl(QUrl("https://a645162.github.io/shmtu-auth/"))

    def resizeEvent(self, e):
        super().resizeEvent(e)
        if hasattr(self, "splashScreen"):
            self.splash_screen.resize(self.size())
