# coding:utf-8
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


class SettingInterface(ScrollArea):
    """ Setting interface """

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

        # personalization
        self.personalGroup = SettingCardGroup(
            self.tr('Personalization'), self.scrollWidget)
        self.micaCard = SwitchSettingCard(
            FIF.TRANSPARENT,
            self.tr('Mica effect'),
            self.tr('Apply semi transparent to windows and surfaces'),
            cfg.micaEnabled,
            self.personalGroup
        )
        self.themeCard = OptionsSettingCard(
            cfg.themeMode,
            FIF.BRUSH,
            "配色方案",
            "改变程序的外观",
            texts=[
                "亮色", "暗色",
                "跟随系统设置"
            ],
            parent=self.personalGroup
        )
        self.themeColorCard = CustomColorSettingCard(
            cfg.themeColor,
            FIF.PALETTE,
            self.tr('Theme color'),
            self.tr('Change the theme color of you application'),
            self.personalGroup
        )
        self.zoomCard = OptionsSettingCard(
            cfg.dpiScale,
            FIF.ZOOM,
            "界面缩放比例",
            "改变程序控件以及字体的大小",
            texts=[
                "100%", "125%", "150%", "175%", "200%",
                "跟随系统设置"
            ],
            parent=self.personalGroup
        )

        # material
        self.materialGroup = SettingCardGroup(
            self.tr('Material'), self.scrollWidget)
        self.blurRadiusCard = RangeSettingCard(
            cfg.blurRadius,
            FIF.ALBUM,
            self.tr('Acrylic blur radius'),
            self.tr('The greater the radius, the more blurred the image'),
            self.materialGroup
        )

        # update software
        self.updateSoftwareGroup = SettingCardGroup(
            self.tr("Software update"), self.scrollWidget)
        self.updateOnStartUpCard = SwitchSettingCard(
            FIF.UPDATE,
            self.tr('Check for updates when the application starts'),
            self.tr('The new version will be more stable and have more features'),
            configItem=cfg.checkUpdateAtStartUp,
            parent=self.updateSoftwareGroup
        )

        # application
        self.aboutGroup = SettingCardGroup(self.tr('About'), self.scrollWidget)
        self.helpCard = HyperlinkCard(
            HELP_URL,
            "打开帮助页面",
            FIF.HELP,
            "帮助",
            "查看帮助信息",
            self.aboutGroup
        )
        self.feedbackCard = PrimaryPushSettingCard(
            "反馈",
            FIF.FEEDBACK,
            "提供反馈",
            "帮助我们改进程序",
            self.aboutGroup
        )
        self.aboutCard = PrimaryPushSettingCard(
            "检查更新",
            FIF.INFO,
            "关于",
            '© ' + self.tr('Copyright') + f" {YEAR}, {AUTHOR}. " +
            self.tr('Version') + " " + VERSION,
            self.aboutGroup
        )

        self.__initWidget()

    def __initWidget(self):
        self.resize(1000, 800)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setViewportMargins(0, 80, 0, 20)
        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)
        self.setObjectName('settingInterface')

        # initialize style sheet
        self.scrollWidget.setObjectName('scrollWidget')
        self.settingLabel.setObjectName('settingLabel')
        StyleSheet.SETTING_INTERFACE.apply(self)

        # self.micaCard.setEnabled(isWin11())
        self.micaCard.setEnabled(False)

        # initialize layout
        self.__initLayout()
        self.__connectSignalToSlot()

    def __initLayout(self):
        self.settingLabel.move(36, 30)

        # add cards to group
        self.shmtuAuthGroup.addSettingCard(self.musicFolderCard)
        self.shmtuAuthGroup.addSettingCard(self.downloadFolderCard)

        self.personalGroup.addSettingCard(self.micaCard)
        self.personalGroup.addSettingCard(self.themeCard)
        self.personalGroup.addSettingCard(self.themeColorCard)
        self.personalGroup.addSettingCard(self.zoomCard)
        # self.personalGroup.addSettingCard(self.languageCard)

        self.materialGroup.addSettingCard(self.blurRadiusCard)

        self.updateSoftwareGroup.addSettingCard(self.updateOnStartUpCard)

        self.aboutGroup.addSettingCard(self.helpCard)
        self.aboutGroup.addSettingCard(self.feedbackCard)
        self.aboutGroup.addSettingCard(self.aboutCard)

        # add setting card group to layout
        self.expandLayout.setSpacing(28)
        self.expandLayout.setContentsMargins(36, 10, 36, 0)
        self.expandLayout.addWidget(self.shmtuAuthGroup)
        self.expandLayout.addWidget(self.personalGroup)
        self.expandLayout.addWidget(self.materialGroup)
        self.expandLayout.addWidget(self.updateSoftwareGroup)
        self.expandLayout.addWidget(self.aboutGroup)

    def __showRestartTooltip(self):
        """ show restart tooltip """
        InfoBar.success(
            self.tr('Updated successfully'),
            self.tr('Configuration takes effect after restart'),
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
        cfg.appRestartSig.connect(self.__showRestartTooltip)

        # music in the pc
        self.downloadFolderCard.clicked.connect(
            self.__onDownloadFolderCardClicked)

        # personalization
        self.themeCard.optionChanged.connect(lambda ci: setTheme(cfg.get(ci)))
        self.themeColorCard.colorChanged.connect(lambda c: setThemeColor(c))

        # about
        self.feedbackCard.clicked.connect(
            lambda: QDesktopServices.openUrl(QUrl(FEEDBACK_URL)))
