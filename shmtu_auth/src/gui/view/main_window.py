# -*- coding: utf-8 -*-

from typing import List
from PySide6.QtCore import Qt, Signal, QEasingCurve, QUrl, QSize
from PySide6.QtGui import QIcon, QDesktopServices, QColor
from PySide6.QtWidgets import QApplication, QHBoxLayout, QFrame, QWidget

from qfluentwidgets import (NavigationAvatarWidget, NavigationItemPosition, MessageBox, FluentWindow,
                            SplashScreen)
from qfluentwidgets import FluentIcon as FIF

from .interface.about_interface import AboutInterface
from .interface.gallery_interface import GalleryInterface
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

from ...utils.logs import get_logger

logger = get_logger()


class MainWindow(FluentWindow):
    user_list: List[UserItem] = []

    def __init__(self):
        super().__init__()

        logger.info("MainWindow initializing...")

        self._init_window()

        # create sub interface
        self.homeInterface = HomeInterface(self)
        self.authInterface = AuthInterface(self, self.user_list)
        self.userListInterface = UserListInterface(self, self.user_list)
        self.logInterface = LogInterface(self)
        self.settingInterface = SettingInterface(self)
        self.aboutInterface = AboutInterface(self)

        # enable acrylic effect
        self.navigationInterface.setAcrylicEnabled(True)
        self.setCustomBackgroundColor(QColor(240, 244, 249), QColor(32, 32, 32))

        # self.connectSignalToSlot()

        # add items to navigation interface
        self.init_left_navigation_item()
        self.splashScreen.finish()

    # def connectSignalToSlot(self):
    #     signalBus.micaEnableChanged.connect(self.setMicaEffectEnabled)
    #     signalBus.switchToSampleCard.connect(self.switchToSample)
    #     signalBus.supportSignal.connect(self.onGithubPage)

    def init_left_navigation_item(self):
        # add navigation items
        self.addSubInterface(self.homeInterface, FIF.HOME, "主页")

        # 分隔线
        self.navigationInterface.addSeparator()

        pos = NavigationItemPosition.SCROLL
        self.addSubInterface(
            self.authInterface,
            FIF.VPN,
            "校园网认证",
            pos
        )
        self.addSubInterface(
            self.userListInterface,
            FIF.PEOPLE,
            "用户列表",
            pos
        )

        self.navigationInterface.addSeparator(pos)

        self.addSubInterface(
            self.logInterface,
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
            self.settingInterface,
            FIF.SETTING,
            "设置",
            NavigationItemPosition.BOTTOM
        )
        self.addSubInterface(
            self.aboutInterface,
            FIF.INFO,
            "关于",
            NavigationItemPosition.BOTTOM
        )

    def _init_window(self):
        self.resize(960, 780)
        self.setMinimumWidth(600)
        self.setMinimumWidth(400)
        self.setWindowIcon(QIcon(':/gui/Logo128'))
        self.setWindowTitle('shmtu-auth')

        # 直接关闭Mica云母特效(我的AMD Radeon RX 6800 显卡反正是显示有问题)
        self.setMicaEffectEnabled(False)

        # create splash screen
        self.splashScreen = SplashScreen(self.windowIcon(), self)
        self.splashScreen.setIconSize(QSize(106, 106))
        self.splashScreen.raise_()

        desktop = QApplication.screens()[0].availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)
        self.show()

        SystemTray(self)

        QApplication.processEvents()

    def onGithubPage(self):
        QDesktopServices.openUrl(QUrl("https://a645162.github.io/shmtu-auth/"))

    def resizeEvent(self, e):
        super().resizeEvent(e)
        if hasattr(self, 'splashScreen'):
            self.splashScreen.resize(self.size())

    def switchToSample(self, routeKey, index):
        """ switch to sample """
        interfaces = self.findChildren(GalleryInterface)
        for w in interfaces:
            if w.objectName() == routeKey:
                self.stackedWidget.setCurrentWidget(w, False)
                w.scrollToCard(index)
