# -*- coding: utf-8 -*-

from qfluentwidgets import (
    SettingCardGroup,
    SwitchSettingCard,
    OptionsSettingCard,
    HyperlinkCard,
    PrimaryPushSettingCard,
    ScrollArea,
    ExpandLayout,
    CustomColorSettingCard,
    setTheme,
    setThemeColor,
    RangeSettingCard,
)
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import InfoBar
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import QWidget, QLabel

from shmtu_auth.src.gui.common.config import (
    cfg,
    HELP_URL,
    FEEDBACK_URL,
    AUTHOR,
    VERSION,
    YEAR,
)
from shmtu_auth.src.gui.common.style_sheet import StyleSheet

from shmtu_auth.src.gui.task.check_update import start_check_update_once_thread

from shmtu_auth.src.utils.logs import get_logger

logger = get_logger()


class SettingInterface(ScrollArea):
    """Setting interface"""

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.scrollWidget = QWidget()
        self.expandLayout = ExpandLayout(self.scrollWidget)

        # setting label
        self.settingLabel = QLabel("设置", self)

        # shmtu-auth
        self.shmtu_auth_group = SettingCardGroup("校园网自动认证", self.scrollWidget)
        self.auth_auto_start_work_thread_card = SwitchSettingCard(
            FIF.PLAY,
            "自动开始工作",
            "启动程序后自动开始工作(联网认证)",
            cfg.auth_auto_start_work_thread,
            self.shmtu_auth_group,
        )

        # 通用设置
        self.general_group = SettingCardGroup("通用设置", self.scrollWidget)
        self.auto_startup_card = SwitchSettingCard(
            FIF.PLAY,
            "开机自动启动",
            "计算机开机后自动启动。(开发中，后续版本将支持~)",
            cfg.auto_startup,
            self.general_group,
        )
        self.auto_startup_card.setEnabled(False)
        self.auto_minimize_card = SwitchSettingCard(
            FIF.MINIMIZE,
            "自动隐藏",
            "程序启动后自动最小化(隐藏)到系统托盘",
            cfg.auto_minimize,
            self.general_group,
        )

        # 托盘设置
        self.tray_group = SettingCardGroup("系统托盘设置", self.scrollWidget)
        self.close_to_tray_card = SwitchSettingCard(
            FIF.CLOSE,
            "关闭到托盘",
            "点击关闭按钮时最小化到系统托盘而不是退出程序",
            cfg.close_to_tray,
            self.tray_group,
        )
        self.minimize_to_tray_card = SwitchSettingCard(
            FIF.DOWN,
            "最小化到托盘",
            "最小化窗口时隐藏到系统托盘",
            cfg.minimize_to_tray,
            self.tray_group,
        )
        self.silent_start_card = SwitchSettingCard(
            FIF.QUIET_HOURS,
            "静默启动",
            "程序启动时直接最小化到托盘，不显示主窗口",
            cfg.silent_start,
            self.tray_group,
        )
        self.show_tray_notifications_card = SwitchSettingCard(
            FIF.MESSAGE,
            "托盘通知",
            "显示系统托盘通知消息",
            cfg.show_tray_notifications,
            self.tray_group,
        )
        self.tray_double_click_action_card = OptionsSettingCard(
            cfg.tray_double_click_action,
            FIF.ARROW_DOWN,
            "双击托盘动作",
            "设置双击托盘图标时的行为",
            texts=["显示/隐藏切换", "仅显示窗口", "仅隐藏窗口"],
            parent=self.tray_group,
        )

        # 个性化设置
        self.personalization_group = SettingCardGroup("个性化设置", self.scrollWidget)
        self.mica_card = SwitchSettingCard(
            FIF.TRANSPARENT,
            "Windows 11 云母(Mica)特效",
            "Windows 11系统下为界面使用Semi半透明。(AMD GPU下有Bug，暂时禁用！)",
            cfg.mica_enabled,
            self.personalization_group,
        )
        self.mica_card.setEnabled(False)
        self.theme_card = OptionsSettingCard(
            cfg.themeMode,
            FIF.BRUSH,
            "配色方案",
            "改变程序的外观",
            texts=["亮色", "暗色", "跟随系统设置"],
            parent=self.personalization_group,
        )
        self.theme_color_card = CustomColorSettingCard(
            cfg.themeColor,
            FIF.PALETTE,
            "主题颜色",
            "改变主题颜色",
            self.personalization_group,
        )
        self.zoom_card = OptionsSettingCard(
            cfg.dpi_scale,
            FIF.ZOOM,
            "界面缩放比例",
            "改变程序控件以及字体的大小",
            texts=["100%", "125%", "150%", "175%", "200%", "跟随系统设置"],
            parent=self.personalization_group,
        )

        # material
        self.material_group = SettingCardGroup("界面材质", self.scrollWidget)
        self.blurRadiusCard = RangeSettingCard(
            cfg.blur_radius,
            FIF.ALBUM,
            "Acrylic模糊半径",
            "模糊半径越大，图片越模糊。",
            self.material_group,
        )
        self.blurRadiusCard.setEnabled(False)

        # update software
        self.update_software_group = SettingCardGroup("软件更新", self.scrollWidget)
        self.update_on_start_up_card = SwitchSettingCard(
            FIF.UPDATE,
            "自动检查更新",
            "程序将在启动时自动联网检测是否存在新版本。",
            configItem=cfg.check_update_at_start_up,
            parent=self.update_software_group,
        )

        # application
        self.about_group = SettingCardGroup("关于", self.scrollWidget)
        self.help_card = HyperlinkCard(
            HELP_URL, "打开帮助页面", FIF.HELP, "帮助", "查看帮助信息", self.about_group
        )
        self.feedback_card = PrimaryPushSettingCard(
            "反馈", FIF.FEEDBACK, "提供反馈", "帮助我们改进程序", self.about_group
        )
        self.about_card = PrimaryPushSettingCard(
            "检查更新",
            FIF.INFO,
            "关于",
            "© " + "Copyright" + f" {YEAR}, {AUTHOR}. " + "Version: " + " " + VERSION,
            self.about_group,
        )
        self.about_card.clicked.connect(lambda: start_check_update_once_thread())

        self.__init_widget()

    def __init_widget(self):
        self.resize(1000, 800)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setViewportMargins(0, 80, 0, 20)
        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)
        self.setObjectName("settingInterface")

        # initialize style sheet
        self.scrollWidget.setObjectName("scrollWidget")
        self.settingLabel.setObjectName("settingLabel")
        StyleSheet.SETTING_INTERFACE.apply(self)

        # self.micaCard.setEnabled(isWin11())

        # initialize layout
        self.__init_layout()
        self.__connectSignalToSlot()

    def __init_layout(self):
        self.settingLabel.move(36, 30)

        # 添加所有Card到Group

        # shmtu-auth
        self.shmtu_auth_group.addSettingCard(self.auth_auto_start_work_thread_card)

        # 通用设置
        self.general_group.addSettingCard(self.auto_startup_card)
        self.general_group.addSettingCard(self.auto_minimize_card)

        # 托盘设置
        self.tray_group.addSettingCard(self.close_to_tray_card)
        self.tray_group.addSettingCard(self.minimize_to_tray_card)
        self.tray_group.addSettingCard(self.silent_start_card)
        self.tray_group.addSettingCard(self.show_tray_notifications_card)
        self.tray_group.addSettingCard(self.tray_double_click_action_card)

        # 界面个性化设置
        self.personalization_group.addSettingCard(self.mica_card)
        self.personalization_group.addSettingCard(self.theme_card)
        self.personalization_group.addSettingCard(self.theme_color_card)
        self.personalization_group.addSettingCard(self.zoom_card)
        # self.personalGroup.addSettingCard(self.languageCard)

        self.material_group.addSettingCard(self.blurRadiusCard)

        self.update_software_group.addSettingCard(self.update_on_start_up_card)

        self.about_group.addSettingCard(self.help_card)
        self.about_group.addSettingCard(self.feedback_card)
        self.about_group.addSettingCard(self.about_card)

        # add setting card group to layout
        self.expandLayout.setSpacing(28)
        self.expandLayout.setContentsMargins(36, 10, 36, 0)
        self.expandLayout.addWidget(self.shmtu_auth_group)
        self.expandLayout.addWidget(self.general_group)
        self.expandLayout.addWidget(self.tray_group)
        self.expandLayout.addWidget(self.personalization_group)
        self.expandLayout.addWidget(self.material_group)
        self.expandLayout.addWidget(self.update_software_group)
        self.expandLayout.addWidget(self.about_group)

    def __show_restart_tooltip(self):
        """show restart tooltip"""
        InfoBar.success(
            "更新成功", "设置已经保存，重启程序后生效。", duration=1500, parent=self
        )

    # def __onDownloadFolderCardClicked(self):
    #     """ download folder card clicked slot """
    #     folder = QFileDialog.getExistingDirectory(
    #         self, self.tr("Choose folder"), "./")
    #     if not folder or cfg.get(cfg.downloadFolder) == folder:
    #         return
    #
    #     cfg.set(cfg.downloadFolder, folder)
    #     self.downloadFolderCard.setContent(folder)

    def __connectSignalToSlot(self):
        """connect signal to slot"""
        cfg.appRestartSig.connect(self.__show_restart_tooltip)

        # music in the pc
        # self.downloadFolderCard.clicked.connect(
        #     self.__onDownloadFolderCardClicked)

        # personalization
        self.theme_card.optionChanged.connect(lambda ci: setTheme(cfg.get(ci)))
        self.theme_color_card.colorChanged.connect(lambda c: setThemeColor(c))

        # about
        self.feedback_card.clicked.connect(
            lambda: QDesktopServices.openUrl(QUrl(FEEDBACK_URL))
        )
