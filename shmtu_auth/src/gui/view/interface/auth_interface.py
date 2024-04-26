# -*- coding: utf-8 -*-

from typing import List

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QApplication, QFrame, QVBoxLayout, QLabel, QWidget, QHBoxLayout
from qfluentwidgets import (FluentIcon, IconWidget, FlowLayout, isDarkTheme,
                            Theme, applyThemeColor, SmoothScrollArea, SearchLineEdit, StrongBodyLabel,
                            BodyLabel)

from .gallery_interface import GalleryInterface
from ...common.config import cfg
from qfluentwidgets import (SettingCardGroup, SwitchSettingCard, FolderListSettingCard,
                            OptionsSettingCard, PushSettingCard,
                            HyperlinkCard, PrimaryPushSettingCard, ScrollArea,
                            ComboBoxSettingCard, ExpandLayout, Theme, CustomColorSettingCard,
                            setTheme, setThemeColor, RangeSettingCard, isDarkTheme)
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import InfoBar
from PySide6.QtCore import Qt, Signal, QUrl, QStandardPaths
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import QWidget, QLabel, QFileDialog

from ...common.config import cfg, HELP_URL, FEEDBACK_URL, AUTHOR, VERSION, YEAR, isWin11
from ...common.style_sheet import StyleSheet


class AuthInterface(GalleryInterface):
    """ Auth interface """

    def __init__(self, parent=None):
        super().__init__(
            title="上海海事大学校园网自动认证",
            subtitle="Author:Haomin Kong",
            parent=parent
        )
        self.setObjectName('authInterface')

        self.authSettingsWidget = AuthSettingWidget(self)

        # self.iconView = IconCardView(self)
        self.vBoxLayout.addWidget(self.authSettingsWidget)


class AuthSettingWidget(ScrollArea):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.scrollWidget = QWidget()
        self.expandLayout = ExpandLayout(self.scrollWidget)

        # setting label
        self.settingLabel = QLabel("设置", self)

        # shmtu-auth
        self.shmtuAuthGroup = SettingCardGroup(
            self.tr("校园网自动认证"), self.scrollWidget)
        self.musicFolderCard = FolderListSettingCard(
            cfg.musicFolders,
            self.tr("Local music library"),
            directory=QStandardPaths.writableLocation(
                QStandardPaths.MusicLocation),
            parent=self.shmtuAuthGroup
        )
        self.downloadFolderCard = PushSettingCard(
            self.tr('Choose folder'),
            FIF.DOWNLOAD,
            self.tr("Download directory"),
            cfg.get(cfg.downloadFolder),
            self.shmtuAuthGroup
        )

        self.__init_widget()

    def __init_widget(self):
        # self.resize(1000, 800)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setViewportMargins(0, 80, 0, 20)
        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)
        self.setObjectName('settingInterface')

        # initialize style sheet
        self.scrollWidget.setObjectName('scrollWidget')
        self.settingLabel.setObjectName('settingLabel')
        StyleSheet.SETTING_INTERFACE.apply(self)

        # initialize layout
        self.__init_layout()
        self.__connectSignalToSlot()

    def __init_layout(self):
        self.settingLabel.move(36, 30)

        # add cards to group
        # shmtu-auth
        self.shmtuAuthGroup.addSettingCard(self.musicFolderCard)
        self.shmtuAuthGroup.addSettingCard(self.downloadFolderCard)

        # add setting card group to layout
        self.expandLayout.setSpacing(28)
        self.expandLayout.setContentsMargins(36, 10, 36, 0)
        self.expandLayout.addWidget(self.shmtuAuthGroup)

    def __showRestartTooltip(self):
        """ show restart tooltip """
        InfoBar.success(
            "更新成功",
            "设置已经保存，重启程序后生效。",
            duration=1500,
            parent=self
        )

    def __onDownloadFolderCardClicked(self):
        """ download folder card clicked slot """
        folder = QFileDialog.getExistingDirectory(
            self, self.tr("Choose folder"), "./")
        if not folder or cfg.get(cfg.downloadFolder) == folder:
            return

        cfg.set(cfg.downloadFolder, folder)
        self.downloadFolderCard.setContent(folder)

    def __connectSignalToSlot(self):
        """ connect signal to slot """
        # cfg.appRestartSig.connect(self.__showRestartTooltip)
        pass
