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
)
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import InfoBar

from shmtu_auth.src.gui.view.interface.gallery_interface import GalleryInterface
from shmtu_auth.src.gui.view.components.fluent.widget_label import FBodyLabel
from shmtu_auth.src.gui.view.components.fluent.widget_push_button import FPushButton

from shmtu_auth.src.gui.common.config import cfg, Config
from shmtu_auth.src.gui.common.style_sheet import StyleSheet
from shmtu_auth.src.datatype.shmtu.auth.auth_user import UserItem

from shmtu_auth.src.gui.feature.network_auth import AuthThread

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

        # shmtu-auth
        self.auth_group_general = SettingCardGroup("通用", self.scroll_widget)

        self.start_card = PrimaryPushSettingCard(
            text="启动", icon=FIF.HELP, title="运行状态", content="启动或关闭服务"
        )

        self.auth_group_general.addSettingCard(self.start_card)

        self.check_interval_card = InternetCheckSettingCard(
            cfg=cfg, parent=self.auth_group_general
        )
        self.auth_group_general.addSettingCard(self.check_interval_card)
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

        self.current_status = False
        self.set_auth_work_status(False)

        if cfg.auth_auto_start_work_thread.value:
            self.__on_work_button_clicked()

    def __on_work_button_clicked(self):

        if not self.current_status:
            # 当前为False,需要启动
            if self.work_thread is not None:
                if self.work_thread.is_alive():
                    self.work_thread.need_work = False
                    self.work_thread.join()
                self.work_thread = None

            self.work_thread = AuthThread(
                user_list=self.user_list,
                check_internet_interval=cfg.check_internet_interval.value,
                check_internet_retry_times=cfg.check_internet_retry_times.value,
                check_internet_retry_wait_time=cfg.check_internet_retry_wait_time.value,
            )

            self.work_thread.start()

            self.current_status = True
        else:
            # 当前为True,需要停止
            if self.work_thread is not None:
                if self.work_thread.is_alive():
                    self.work_thread.need_work = False
                    self.work_thread.join()
                self.work_thread = None

            self.current_status = False

        self.set_auth_work_status(self.current_status)

    def set_auth_work_status(self, status: bool):
        """set auth work status"""
        if status:
            # Started
            self.authSettingsWidget.start_card.iconLabel.setIcon(FIF.PLAY_SOLID)
            self.authSettingsWidget.start_card.button.setText("停止")
            self.authSettingsWidget.start_card.setContent("当前服务已经启动")
        else:
            # Stopped
            self.authSettingsWidget.start_card.iconLabel.setIcon(FIF.PAUSE_BOLD)
            self.authSettingsWidget.start_card.button.setText("启动")
            self.authSettingsWidget.start_card.setContent("当前服务已经停止")
