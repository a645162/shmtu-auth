# -*- coding: utf-8 -*-

from typing import List, Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout

from qfluentwidgets import (
    SettingCardGroup,
    PrimaryPushSettingCard,
    ExpandGroupSettingCard,
    ScrollArea,
    ExpandLayout,
    Slider,
    RangeConfigItem,
    qconfig,
    InfoBar,
)
from qfluentwidgets import FluentIcon as FIF

from shmtu_auth.src.gui.view.interface.gallery_interface import GalleryInterface
from shmtu_auth.src.gui.view.components.fluent.widget_label import FBodyLabel
from shmtu_auth.src.gui.view.components.fluent.widget_push_button import FPushButton

from shmtu_auth.src.gui.common.config import cfg, Config
from shmtu_auth.src.gui.common.style_sheet import StyleSheet
from shmtu_auth.src.datatype.shmtu.auth.auth_user import UserItem

from shmtu_auth.src.gui.feature.network_auth import AuthThread
from shmtu_auth.src.gui.common.signal_bus import signal_bus

from shmtu_auth.src.utils.logs import get_logger

logger = get_logger()


class InternetCheckSettingCard(ExpandGroupSettingCard):
    class SliderWithText(QWidget):
        def __init__(self, parent=None):
            super().__init__(parent)

            self.value_label = QLabel(self)

            self.slider = Slider(Qt.Horizontal, self)
            self.slider.setFixedWidth(200)
            self.slider.valueChanged.connect(self.__on_value_update)

            self.hBoxLayout = QHBoxLayout(self)

            self.hBoxLayout.addWidget(self.value_label)
            self.hBoxLayout.addWidget(self.slider)

            self.setLayout(self.hBoxLayout)

        def __on_value_update(self, value):
            self.value_label.setText(str(value))

        def set_range(self, min_value, max_value):
            self.slider.setRange(min_value, max_value)

        def set_value(self, value):
            self.slider.setValue(value)

        def get_value(self):
            return self.slider.value()

    class SettingGroupSliderWithText(SliderWithText):
        def __init__(self, range_config_item: RangeConfigItem, parent=None):
            super().__init__(parent)
            self.range_config_item = range_config_item

            value_range: tuple = self.range_config_item.range
            self.set_range(value_range[0], value_range[1])

            self.set_value(qconfig.get(range_config_item))

            self.slider.valueChanged.connect(self.__value_change_update_setting)

        def __value_change_update_setting(self, value):
            qconfig.set(self.range_config_item, value)

        def restore_default_value(self):
            self.set_value(self.range_config_item.defaultValue)

    def __init__(self, cfg: Config, parent=None):
        super().__init__(
            FIF.SPEED_OFF,
            "网络状态监控设置",
            "设置网络状态监控的具体细节(一般不需要调整)",
            parent,
        )

        self.cfg = cfg

        # 调整内部布局
        self.viewLayout.setContentsMargins(0, 0, 0, 0)
        self.viewLayout.setSpacing(0)

        # 加载其他组件
        self.__init_content()

        # 恢复默认按钮
        self.restore_button = FPushButton(self, "恢复默认")
        self.restore_button.clicked.connect(self.__restore_default)
        self.restore_button.setFixedWidth(135)
        self.restore_label = FBodyLabel("调错了？！恢复缺省值吧~", self)
        self.add(self.restore_label, self.restore_button)

    def __init_content(self):
        self.check_internet_interval_slider = self.SettingGroupSliderWithText(
            self.cfg.check_internet_interval, self
        )
        self.add(FBodyLabel("检测间隔", self), self.check_internet_interval_slider)

        self.check_internet_retry_times_slider = self.SettingGroupSliderWithText(
            self.cfg.check_internet_retry_times, self
        )
        self.add(
            FBodyLabel("联网失败的重试次数", self),
            self.check_internet_retry_times_slider,
        )

        self.check_internet_retry_wait_time_slider = self.SettingGroupSliderWithText(
            self.cfg.check_internet_retry_wait_time, self
        )
        self.add(
            FBodyLabel("重试等待时间", self), self.check_internet_retry_wait_time_slider
        )

    def __restore_default(self):
        self.check_internet_interval_slider.restore_default_value()
        self.check_internet_retry_times_slider.restore_default_value()
        self.check_internet_retry_wait_time_slider.restore_default_value()

    def add(self, label, widget):
        w = QWidget()
        w.setFixedHeight(60)

        layout = QHBoxLayout(w)
        layout.setContentsMargins(48, 12, 48, 12)

        layout.addWidget(label)
        layout.addStretch(1)
        layout.addWidget(widget)

        # 添加组件到设置卡
        self.addGroupWidget(w)


class AuthSettingWidget(ScrollArea):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.scroll_widget = QWidget()
        self.expand_layout = ExpandLayout(self.scroll_widget)
        self.expand_layout.setSpacing(28)
        self.expand_layout.setContentsMargins(36, 10, 36, 0)

        # 状态显示组
        self.status_group = AuthStatusCard(self.scroll_widget)
        self.expand_layout.addWidget(self.status_group)

        # shmtu-auth 控制组
        self.auth_group_general = SettingCardGroup("认证控制", self.scroll_widget)

        self.start_card = PrimaryPushSettingCard(
            text="启动", icon=FIF.HELP, title="运行状态", content="启动或关闭服务"
        )

        self.auth_group_general.addSettingCard(self.start_card)

        self.check_interval_card = InternetCheckSettingCard(
            cfg=cfg, parent=self.auth_group_general
        )
        self.auth_group_general.addSettingCard(self.check_interval_card)

        # 手动测试按钮
        self.manual_test_card = PrimaryPushSettingCard(
            text="测试", icon=FIF.SYNC, title="手动测试", content="手动测试网络连接状态"
        )
        # 注意：信号连接将在AuthInterface中进行
        self.auth_group_general.addSettingCard(self.manual_test_card)

        self.expand_layout.addWidget(self.auth_group_general)

        self.__init_widget()

    def __init_widget(self):
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setViewportMargins(0, 0, 0, 0)
        self.setWidget(self.scroll_widget)
        self.setWidgetResizable(True)
        self.setObjectName("settingInterface")

        # initialize style sheet
        self.scroll_widget.setObjectName("scrollWidget")
        StyleSheet.SETTING_INTERFACE.apply(self)

    def __show_restart_tooltip(self):
        """show restart tooltip"""
        InfoBar.success(
            "更新成功", "设置已经保存，重启程序后生效。", duration=1500, parent=self
        )


class AuthStatusCard(SettingCardGroup):
    """显示认证状态的卡片"""

    def __init__(self, parent=None):
        super().__init__("认证状态", parent)

        # 网络状态
        self.network_status_card = self.__create_status_card(
            "网络状态", "检查中...", FIF.WIFI
        )
        self.addSettingCard(self.network_status_card)

        # 认证服务状态
        self.service_status_card = self.__create_status_card(
            "认证服务", "已停止", FIF.POWER_BUTTON
        )
        self.addSettingCard(self.service_status_card)

        # 最后认证用户
        self.last_auth_card = self.__create_status_card("最后认证", "无", FIF.PEOPLE)
        self.addSettingCard(self.last_auth_card)

        # 认证尝试次数
        self.auth_attempts_card = self.__create_status_card("认证次数", "0", FIF.FLAG)
        self.addSettingCard(self.auth_attempts_card)

        self.auth_attempt_count = 0

    def __create_status_card(self, title, content, icon):
        """创建状态显示卡片"""
        from qfluentwidgets import SettingCard

        card = SettingCard(icon, title, content)
        return card

    def update_network_status(self, is_online: bool):
        """更新网络状态"""
        if is_online:
            self.network_status_card.setContent("已连接 ✓")
        else:
            self.network_status_card.setContent("未连接 ✗")

    def update_service_status(self, is_running: bool):
        """更新服务状态"""
        if is_running:
            self.service_status_card.setContent("运行中 ✓")
        else:
            self.service_status_card.setContent("已停止 ✗")

    def update_last_auth_user(self, user_id: str):
        """更新最后认证用户"""
        self.last_auth_card.setContent(f"{user_id}")

    def update_auth_attempt(self, user_id: str):
        """更新认证尝试"""
        self.auth_attempt_count += 1
        self.auth_attempts_card.setContent(f"{self.auth_attempt_count}")

    def reset_counters(self):
        """重置计数器"""
        self.auth_attempt_count = 0
        self.auth_attempts_card.setContent("0")


class AuthInterface(GalleryInterface):
    """Auth interface"""

    user_list: List[UserItem]
    current_status: bool

    work_thread: Optional[AuthThread] = None

    def __init__(self, parent=None, user_list: List[UserItem] = None):
        super().__init__(
            title="上海海事大学校园网自动认证",
            subtitle="Author:Haomin Kong",
            parent=parent,
        )
        self.setObjectName("authInterface")

        if user_list is None:
            raise Exception("user_list is None")
        self.user_list = user_list

        self.authSettingsWidget = AuthSettingWidget(self)

        self.vBoxLayout.addWidget(self.authSettingsWidget)

        self.authSettingsWidget.start_card.clicked.connect(
            self.__on_work_button_clicked
        )
        self.authSettingsWidget.manual_test_card.clicked.connect(
            self.__on_manual_test_clicked
        )

        # 连接信号
        self.__connect_signals()

        self.current_status = False
        self.set_auth_work_status(False)

        # 注意：不在这里自动启动，而是在MainWindow初始化完成后处理
        # if cfg.auth_auto_start_work_thread.value:
        #     self.__on_work_button_clicked()

    def __connect_signals(self):
        """连接信号总线的信号"""
        # 连接认证状态变化信号
        signal_bus.signal_auth_status_changed.connect(
            self.authSettingsWidget.status_group.update_network_status
        )

        # 连接认证尝试信号
        signal_bus.signal_auth_attempt.connect(
            self.authSettingsWidget.status_group.update_auth_attempt
        )

        # 连接认证成功信号
        signal_bus.signal_auth_success.connect(self.__on_auth_success)

        # 连接认证失败信号
        signal_bus.signal_auth_failed.connect(self.__on_auth_failed)

        # 连接线程启动信号
        signal_bus.signal_auth_thread_started.connect(self.__on_thread_started)

        # 连接线程停止信号
        signal_bus.signal_auth_thread_stopped.connect(self.__on_thread_stopped)

        logger.info("认证界面信号连接完成")

    def __on_thread_stopped(self):
        """处理认证线程停止信号"""
        logger.info("GUI收到认证线程停止信号")
        self.authSettingsWidget.status_group.update_service_status(False)
        self.authSettingsWidget.status_group.reset_counters()

    def __on_auth_success(self, user_id: str):
        """处理认证成功"""
        logger.info(f"GUI收到认证成功信号：{user_id}")
        self.authSettingsWidget.status_group.update_last_auth_user(user_id)
        InfoBar.success(
            "认证成功", f"用户 {user_id} 认证成功", duration=3000, parent=self
        )

    def __on_auth_failed(self, user_id: str, error_msg: str):
        """处理认证失败"""
        logger.warning(f"GUI收到认证失败信号：{user_id} - {error_msg}")
        InfoBar.warning(
            "认证失败",
            f"用户 {user_id} 认证失败：{error_msg}",
            duration=3000,
            parent=self,
        )

    def __on_thread_started(self):
        """处理线程启动"""
        logger.info("GUI收到认证线程启动信号")
        self.authSettingsWidget.status_group.update_service_status(True)

    def __on_work_button_clicked(self):
        """处理启动/停止按钮点击"""
        logger.info(f"认证服务按钮点击，当前状态：{self.current_status}")

        if not self.current_status:
            # 当前为False,需要启动
            logger.info("准备启动认证服务...")

            # 检查用户列表 - 添加更详细的调试信息
            logger.info(f"当前用户列表长度: {len(self.user_list)}")
            logger.info(
                f"用户列表内容: {[user.user_id if hasattr(user, 'user_id') else str(user) for user in self.user_list]}"
            )

            # 过滤有效用户
            from shmtu_auth.src.datatype.shmtu.auth.auth_user import get_valid_user_list

            valid_users = get_valid_user_list(self.user_list)
            logger.info(f"有效用户数量: {len(valid_users)}")

            if not valid_users or len(valid_users) == 0:
                logger.warning("没有有效的认证用户，无法启动认证服务")
                InfoBar.warning(
                    "启动失败",
                    "请先在用户列表中添加有效的认证用户",
                    duration=3000,
                    parent=self,
                )
                return

            # 停止已有线程
            if self.work_thread is not None:
                if self.work_thread.is_alive():
                    logger.info("停止现有认证线程...")
                    self.work_thread.stop()
                    self.work_thread.join(timeout=5)
                self.work_thread = None

            # 创建新线程
            self.work_thread = AuthThread(
                user_list=self.user_list,
                check_internet_interval=cfg.check_internet_interval.value,
                check_internet_retry_times=cfg.check_internet_retry_times.value,
                check_internet_retry_wait_time=cfg.check_internet_retry_wait_time.value,
            )

            logger.info("启动认证线程...")
            self.work_thread.start()
            self.current_status = True

            InfoBar.success("启动成功", "认证服务已启动", duration=2000, parent=self)

        else:
            # 当前为True,需要停止
            logger.info("准备停止认证服务...")

            if self.work_thread is not None:
                if self.work_thread.is_alive():
                    logger.info("停止认证线程...")
                    self.work_thread.stop()
                    self.work_thread.join(timeout=5)
                self.work_thread = None

            self.current_status = False

            InfoBar.info("已停止", "认证服务已停止", duration=2000, parent=self)

        self.set_auth_work_status(self.current_status)
        logger.info(f"认证服务状态已更新：{self.current_status}")

    def set_auth_work_status(self, status: bool):
        """设置认证工作状态"""
        logger.info(f"更新认证工作状态UI：{status}")

        if status:
            # Started
            self.authSettingsWidget.start_card.iconLabel.setIcon(FIF.PLAY_SOLID)
            self.authSettingsWidget.start_card.button.setText("停止")
            self.authSettingsWidget.start_card.setContent("当前服务已经启动")
            self.authSettingsWidget.status_group.update_service_status(True)
        else:
            # Stopped
            self.authSettingsWidget.start_card.iconLabel.setIcon(FIF.PAUSE_BOLD)
            self.authSettingsWidget.start_card.button.setText("启动")
            self.authSettingsWidget.start_card.setContent("当前服务已经停止")
            self.authSettingsWidget.status_group.update_service_status(False)

    def __on_manual_test_clicked(self):
        """处理手动测试按钮点击"""
        logger.info("开始手动测试网络连接...")

        # 显示测试进行中的提示
        InfoBar.info(
            "测试中", "正在测试网络连接状态，请稍候...", duration=2000, parent=self
        )

        # 执行网络测试
        from shmtu_auth.src.core.core_exp import check_is_connected

        try:
            is_connected = check_is_connected()

            if is_connected:
                logger.info("手动测试结果：网络已连接")
                InfoBar.success(
                    "测试完成", "网络连接正常 ✓", duration=3000, parent=self
                )
                self.authSettingsWidget.status_group.update_network_status(True)
            else:
                logger.warning("手动测试结果：网络未连接")
                InfoBar.warning(
                    "测试完成", "网络连接异常，需要认证 ✗", duration=3000, parent=self
                )
                self.authSettingsWidget.status_group.update_network_status(False)

        except Exception as e:
            logger.error(f"手动测试出错：{str(e)}")
            InfoBar.error(
                "测试失败", f"测试过程中出现错误：{str(e)}", duration=3000, parent=self
            )
