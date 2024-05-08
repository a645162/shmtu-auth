# -*- coding: utf-8 -*-

from typing import List
from PySide6.QtCore import QUrl, QSize
from PySide6.QtGui import QIcon, QDesktopServices, QColor
from PySide6.QtWidgets import QApplication

from qfluentwidgets import (NavigationItemPosition, FluentWindow,
                            SplashScreen)
from qfluentwidgets import FluentIcon as FIF

from .interface.about_interface import AboutInterface
from .interface.log_interface import LogInterface
from .interface.user_list_interface import UserListInterface
from ..common.config import cfg

from .interface.home_interface import HomeInterface
from .interface.auth_interface import AuthInterface
from .interface.settings_interface import SettingInterface

# 加载资源文件,虽然表面上没有调用(不可以移除!)
from ..resource import resources

from .system_tray import SystemTray
from ...datatype.shmtu.auth.auth_user import UserItem

from ..common.signal_bus import log_new

from ...utils.logs import get_logger

logger = get_logger()


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

        self.__connect_signal_to_global_slot()

        # add items to navigation interface
        self.__init_left_navigation_item()
        self.splash_screen.finish()

        log_new("MainWindow initialized.", "Info")

    def try_to_show(self):
        if cfg.autoMinimize.value:
            logger.info("Auto minimize to system tray enabled.")
            self.hide()
        else:
            self.show()

    def __connect_signal_to_global_slot(self):
        pass
    #     signalBus.micaEnableChanged.connect(self.setMicaEffectEnabled)
    #     signalBus.switchToSampleCard.connect(self.switchToSample)
    #     signalBus.supportSignal.connect(self.onGithubPage)

    def __init_left_navigation_item(self):
        # add navigation items
        self.addSubInterface(self.home_interface, FIF.HOME, "主页")

        # 分隔线
        self.navigationInterface.addSeparator()

        pos = NavigationItemPosition.SCROLL
        self.addSubInterface(
            self.auth_interface,
            FIF.VPN,
            "校园网认证",
            pos
        )
        self.addSubInterface(
            self.user_list_interface,
            FIF.PEOPLE,
            "用户列表",
            pos
        )

        self.navigationInterface.addSeparator(pos)

        self.addSubInterface(
            self.log_interface,
            FIF.DATE_TIME,
            "工作日志",
            pos
        )

        # add custom widget to bottom
        self.navigationInterface.addItem(
            routeKey='github.io',
            icon=FIF.DOCUMENT,
            text="项目文档",
            onClick=
            lambda: QDesktopServices.openUrl(
                QUrl("https://a645162.github.io/shmtu-auth/")
            ),
            selectable=False,
            tooltip="项目文档",
            position=NavigationItemPosition.BOTTOM
        )
        self.navigationInterface.addItem(
            routeKey='github',
            icon=FIF.GITHUB,
            text="项目源代码仓库",
            onClick=
            lambda: QDesktopServices.openUrl(
                QUrl("https://github.com/a645162/shmtu-auth")
            ),
            selectable=False,
            tooltip="官方网站",
            position=NavigationItemPosition.BOTTOM
        )

        self.navigationInterface.addSeparator(
            position=NavigationItemPosition.BOTTOM
        )

        self.addSubInterface(
            self.setting_interface,
            FIF.SETTING,
            "设置",
            NavigationItemPosition.BOTTOM
        )
        self.addSubInterface(
            self.about_interface,
            FIF.INFO,
            "关于",
            NavigationItemPosition.BOTTOM
        )

    def __init_window(self):
        dpi_scale = cfg.get_dpi_ratio()
        logger.info(f"MainWindow DPI Scale: {dpi_scale}")

        default_width: int = int(800 * dpi_scale)
        default_height: int = int(600 * dpi_scale)

        min_width: int = int(800 * dpi_scale)
        min_height: int = int(600 * dpi_scale)

        self.setMinimumWidth(min_width)
        self.setMinimumHeight(min_height)
        self.resize(
            default_width,
            default_height
        )

        self.setWindowIcon(QIcon(':/gui/Logo128'))
        self.setWindowTitle('shmtu-auth')

        # 直接关闭Mica云母特效(我的AMD Radeon RX 6800 显卡反正是显示有问题)
        self.setMicaEffectEnabled(False)

        # create splash screen
        self.splash_screen = SplashScreen(self.windowIcon(), self)
        self.splash_screen.setIconSize(QSize(106, 106))
        self.splash_screen.raise_()

        desktop = QApplication.screens()[0].availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)
        self.try_to_show()

        SystemTray(self)

        QApplication.processEvents()

    def open_github_page(self):
        QDesktopServices.openUrl(QUrl("https://a645162.github.io/shmtu-auth/"))

    def resizeEvent(self, e):
        super().resizeEvent(e)
        if hasattr(self, 'splashScreen'):
            self.splash_screen.resize(self.size())
