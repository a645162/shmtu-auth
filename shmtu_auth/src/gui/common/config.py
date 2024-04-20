# coding:utf-8
import sys
from enum import Enum

from PySide6.QtCore import QLocale
from qfluentwidgets import (qconfig, QConfig, ConfigItem, OptionsConfigItem, BoolValidator,
                            OptionsValidator, RangeConfigItem, RangeValidator,
                            FolderListValidator, Theme, FolderValidator, ConfigSerializer, __version__)

def isWin11():
    return sys.platform == 'win32' and sys.getwindowsversion().build >= 22000


class Config(QConfig):
    """ Config of application """

    # folders
    musicFolders = ConfigItem(
        "Folders", "LocalMusic", [], FolderListValidator())
    downloadFolder = ConfigItem(
        "Folders", "Download", "app/download", FolderValidator())

    # main window
    micaEnabled = ConfigItem("MainWindow", "MicaEnabled", isWin11(), BoolValidator())
    dpiScale = OptionsConfigItem(
        "MainWindow", "DpiScale", "Auto", OptionsValidator([1, 1.25, 1.5, 1.75, 2, "Auto"]), restart=True)
    # language = OptionsConfigItem(
    #     "MainWindow", "Language", Language.AUTO, OptionsValidator(Language), LanguageSerializer(), restart=True)

    # Material
    blurRadius  = RangeConfigItem("Material", "AcrylicBlurRadius", 15, RangeValidator(0, 40))

    # software update
    checkUpdateAtStartUp = ConfigItem("Update", "CheckUpdateAtStartUp", True, BoolValidator())


YEAR = 2024
AUTHOR = "Haomin Kong"
VERSION = __version__

HELP_URL = "https://qfluentwidgets.com"
REPO_URL = "https://github.com/zhiyiYo/PyQt-Fluent-Widgets"
EXAMPLE_URL = "https://github.com/zhiyiYo/PyQt-Fluent-Widgets/tree/PySide6/examples"
FEEDBACK_URL = "https://github.com/zhiyiYo/PyQt-Fluent-Widgets/issues"
RELEASE_URL = "https://github.com/zhiyiYo/PyQt-Fluent-Widgets/releases/latest"
ZH_SUPPORT_URL = "https://qfluentwidgets.com/zh/price/"
EN_SUPPORT_URL = "https://qfluentwidgets.com/price/"


cfg = Config()
cfg.themeMode.value = Theme.AUTO
qconfig.load('config/gui_config.json', cfg)
