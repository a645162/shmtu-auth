# -*- coding: utf-8 -*-

import sys

from qfluentwidgets import (qconfig, QConfig, ConfigItem, OptionsConfigItem, BoolValidator,
                            OptionsValidator, RangeConfigItem, RangeValidator,
                            FolderListValidator, Theme, FolderValidator, ConfigSerializer, __version__)

from ...utils.logs import get_logger

logger = get_logger()


def is_windows11():
    return sys.platform == 'win32' and sys.getwindowsversion().build >= 22000


class Config(QConfig):
    """ Config of application """

    # shmtu-auth
    musicFolders = ConfigItem(
        "Folders", "LocalMusic", [], FolderListValidator())
    downloadFolder = ConfigItem(
        "Folders", "Download", "app/download", FolderValidator())
    auth_advanced_feature = ConfigItem(
        "Auth", "AdvancedFeature", False, BoolValidator()
    )
    auth_docker_save_folder = ConfigItem(
        "Auth", "DockerSaveFolder", "", FolderValidator())

    # 通用设置
    autoStartup = ConfigItem(
        "General", "AutoStartup", False, BoolValidator()
    )
    autoMinimize = ConfigItem(
        "General", "AutoMinimize", False, BoolValidator()
    )

    # 界面个性化

    # Main Window
    micaEnabled = ConfigItem("MainWindow", "MicaEnabled", is_windows11(), BoolValidator())
    dpiScale = OptionsConfigItem(
        "MainWindow", "DpiScale", "Auto",
        OptionsValidator([1, 1.25, 1.5, 1.75, 2, "Auto"]),
        restart=True
    )

    # Material
    blurRadius = RangeConfigItem(
        "Material", "AcrylicBlurRadius", 15,
        RangeValidator(0, 40)
    )

    # software update
    checkUpdateAtStartUp = ConfigItem(
        "Update",
        "CheckUpdateAtStartUp",
        True,
        BoolValidator()
    )


YEAR = 2024
AUTHOR = "Haomin Kong"
VERSION = __version__

HELP_URL = "https://a645162.github.io/shmtu-auth/"
REPO_URL = "https://github.com/a645162/shmtu-auth"
AUTHOR_MAIN_PAGE_URL = "https://github.com/a645162"

FEEDBACK_URL = f"{REPO_URL}/issues"
RELEASE_URL = f"{REPO_URL}/releases/latest"

ZH_SUPPORT_URL = "https://a645162.github.io/shmtu-auth/"
EN_SUPPORT_URL = "https://a645162.github.io/shmtu-auth/"

cfg = Config()
cfg.themeMode.value = Theme.AUTO
qconfig.load('config/gui_config.json', cfg)
