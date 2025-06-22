from PySide6.QtWidgets import QApplication
from qfluentwidgets import (
    BoolValidator,
    ConfigItem,
    FolderValidator,
    OptionsConfigItem,
    OptionsValidator,
    QConfig,
    RangeConfigItem,
    RangeValidator,
    Theme,
    qconfig,
)
from qfluentwidgets import __version__ as q_fluent_widgets_version

from shmtu_auth.src.config.build_info import program_version
from shmtu_auth.src.system.system_info import SystemType
from shmtu_auth.src.utils.logs import get_logger

logger = get_logger()


class Config(QConfig):
    """Config of application"""

    # shmtu-auth
    auth_auto_start_work_thread = ConfigItem("Auth", "AutoStartWorkThread", True, BoolValidator())

    check_internet_interval = RangeConfigItem("Auth", "CheckInternetInterval", 60, RangeValidator(5, 3600))

    check_internet_retry_times = RangeConfigItem("Auth", "CheckInternetRetryTimes", 3, RangeValidator(1, 10))
    check_internet_retry_wait_time = RangeConfigItem("Auth", "CheckInternetRetryTimes", 30, RangeValidator(1, 600))

    # 高级操作
    # - 导出到Docker
    auth_advanced_feature = ConfigItem("Auth", "AdvancedFeature", False, BoolValidator())
    auth_docker_save_folder = ConfigItem("Auth", "DockerSaveFolder", "", FolderValidator())

    # 通用设置
    auto_startup = ConfigItem("General", "AutoStartup", False, BoolValidator())
    auto_minimize = ConfigItem("General", "AutoMinimize", False, BoolValidator())

    # 托盘设置
    close_to_tray = ConfigItem("Tray", "CloseToTray", True, BoolValidator())
    minimize_to_tray = ConfigItem("Tray", "MinimizeToTray", True, BoolValidator())
    silent_start = ConfigItem("Tray", "SilentStart", False, BoolValidator())
    show_tray_notifications = ConfigItem("Tray", "ShowTrayNotifications", True, BoolValidator())
    tray_double_click_action = OptionsConfigItem(
        "Tray",
        "DoubleClickAction",
        "show_hide",
        OptionsValidator(["show_hide", "show_only", "hide_only"]),
    )

    # 界面个性化

    # Main Window
    mica_enabled = ConfigItem("MainWindow", "MicaEnabled", SystemType.is_windows11(), BoolValidator())
    dpi_scale = OptionsConfigItem(
        "MainWindow",
        "DpiScale",
        "Auto",
        OptionsValidator([1, 1.25, 1.5, 1.75, 2, "Auto"]),
        restart=True,
    )

    # Material
    blur_radius = RangeConfigItem("Material", "AcrylicBlurRadius", 15, RangeValidator(0, 40))

    # software update
    check_update_at_start_up = ConfigItem("Update", "CheckUpdateAtStartUp", True, BoolValidator())
    update_branch = OptionsConfigItem(
        "Update",
        "UpdateBranch",
        "main",
        OptionsValidator(["main", "beta", "dev"]),  # 默认选项，会在运行时动态更新
    )

    # 认证状态记录
    last_auth_user = ConfigItem("AuthStatus", "LastAuthUser", "")
    last_auth_time = ConfigItem("AuthStatus", "LastAuthTime", "")
    total_auth_attempts = ConfigItem("AuthStatus", "TotalAuthAttempts", 0)
    last_network_status = ConfigItem("AuthStatus", "LastNetworkStatus", False, BoolValidator())
    auth_success_count = ConfigItem("AuthStatus", "AuthSuccessCount", 0)
    auth_failure_count = ConfigItem("AuthStatus", "AuthFailureCount", 0)

    def get_dpi_ratio(self) -> float:
        dpi_scale = 1.0
        dpi_scale_str = str(self.get(cfg.dpi_scale))

        if dpi_scale_str == "Auto":
            # Get System Dpi Scale
            if SystemType.is_windows():
                dpi_scale: float = float(QApplication.primaryScreen().devicePixelRatio())
        else:
            dpi_scale: float = float(dpi_scale_str)

        return dpi_scale


YEAR = 2024
AUTHOR = "Haomin Kong"
VERSION = program_version

HELP_URL = "https://a645162.github.io/shmtu-auth/"
REPO_URL = "https://github.com/a645162/shmtu-auth"
AUTHOR_MAIN_PAGE_URL = "https://github.com/a645162"

FEEDBACK_URL = f"{REPO_URL}/issues"
RELEASE_URL = f"{REPO_URL}/releases/latest"

ZH_SUPPORT_URL = "https://a645162.github.io/shmtu-auth/"
EN_SUPPORT_URL = "https://a645162.github.io/shmtu-auth/"

INTERFACE_URL_AUTH = ""
INTERFACE_URL_USER_LIST = ""
INTERFACE_URL_LOG = ""

cfg = Config()
cfg.themeMode.value = Theme.AUTO

config_path = "config/gui_config.json"

qconfig.load(config_path, cfg)

# Print all attributes of the config(Only properties without underscore)
for attr in dir(cfg):
    if not attr.startswith("_"):
        # Check is methond or property
        if callable(getattr(cfg, attr)):
            continue

        value = getattr(cfg, attr)
        logger.info(f"Config {attr}: {value}")

logger.info(f"QFluentWidgets Version: {q_fluent_widgets_version}")
