from typing import List, Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QLabel, QWidget
from qfluentwidgets import (
    ExpandGroupSettingCard,
    ExpandLayout,
    InfoBar,
    PrimaryPushSettingCard,
    RangeConfigItem,
    ScrollArea,
    SettingCardGroup,
    Slider,
    qconfig,
)
from qfluentwidgets import FluentIcon as FIF

from shmtu_auth.src.datatype.shmtu.auth.auth_user import UserItem
from shmtu_auth.src.gui.common.config import Config, cfg
from shmtu_auth.src.gui.common.signal_bus import signal_bus
from shmtu_auth.src.gui.common.style_sheet import StyleSheet
from shmtu_auth.src.gui.feature.network_auth import AuthThread
from shmtu_auth.src.gui.view.components.fluent.widget_label import FBodyLabel
from shmtu_auth.src.gui.view.components.fluent.widget_push_button import FPushButton
from shmtu_auth.src.gui.view.interface.gallery_interface import GalleryInterface
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
        self.check_internet_interval_slider = self.SettingGroupSliderWithText(self.cfg.check_internet_interval, self)
        self.add(FBodyLabel("检测间隔", self), self.check_internet_interval_slider)

        self.check_internet_retry_times_slider = self.SettingGroupSliderWithText(self.cfg.check_internet_retry_times, self)
        self.add(
            FBodyLabel("联网失败的重试次数", self),
            self.check_internet_retry_times_slider,
        )

        self.check_internet_retry_wait_time_slider = self.SettingGroupSliderWithText(
            self.cfg.check_internet_retry_wait_time, self
        )
        self.add(FBodyLabel("重试等待时间", self), self.check_internet_retry_wait_time_slider)

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

        self.start_card = PrimaryPushSettingCard(text="启动", icon=FIF.HELP, title="运行状态", content="启动或关闭服务")

        self.auth_group_general.addSettingCard(self.start_card)

        self.check_interval_card = InternetCheckSettingCard(cfg=cfg, parent=self.auth_group_general)
        self.auth_group_general.addSettingCard(self.check_interval_card)

        # 手动测试按钮
        self.manual_test_card = PrimaryPushSettingCard(
            text="测试", icon=FIF.SYNC, title="手动测试", content="手动测试网络连接状态"
        )
        # 注意：信号连接将在AuthInterface中进行
        self.auth_group_general.addSettingCard(self.manual_test_card)

        # 重置统计按钮
        self.reset_stats_card = PrimaryPushSettingCard(
            text="重置", icon=FIF.DELETE, title="重置统计", content="清除所有认证历史统计数据"
        )
        # 注意：信号连接将在AuthInterface中进行
        self.auth_group_general.addSettingCard(self.reset_stats_card)

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
        InfoBar.success("更新成功", "设置已经保存，重启程序后生效。", duration=1500, parent=self)


class AuthStatusCard(SettingCardGroup):
    """显示认证状态的卡片"""

    def __init__(self, parent=None):
        super().__init__("认证状态", parent)

        # 网络状态
        self.network_status_card = self.__create_status_card("网络状态", "检查中...", FIF.WIFI)
        self.addSettingCard(self.network_status_card)

        # 认证服务状态
        self.service_status_card = self.__create_status_card("认证服务", "已停止", FIF.POWER_BUTTON)
        self.addSettingCard(self.service_status_card)

        # 最后认证用户
        self.last_auth_card = self.__create_status_card("最后认证", "无", FIF.PEOPLE)
        self.addSettingCard(self.last_auth_card)

        # 认证统计
        self.auth_stats_card = self.__create_status_card("认证统计", "成功: 0 | 失败: 0", FIF.FLAG)
        self.addSettingCard(self.auth_stats_card)

        # 当前会话认证尝试次数
        self.current_session_attempts = 0

        # 加载保存的状态
        self.__load_saved_status()

    def __create_status_card(self, title, content, icon):
        """创建状态显示卡片"""
        from qfluentwidgets import SettingCard

        card = SettingCard(icon, title, content)
        return card

    def __load_saved_status(self):
        """从配置文件加载保存的状态"""
        from shmtu_auth.src.gui.common.config import cfg

        logger.info("加载保存的认证状态...")

        # 加载最后认证用户和时间
        last_user = cfg.last_auth_user.value
        last_time = cfg.last_auth_time.value
        if last_user and last_time:
            self.last_auth_card.setContent(f"{last_user} ({last_time})")
        else:
            self.last_auth_card.setContent("无")

        # 加载网络状态
        last_network_status = cfg.last_network_status.value
        self.update_network_status(last_network_status)

        # 加载认证统计
        success_count = cfg.auth_success_count.value
        failure_count = cfg.auth_failure_count.value
        self.__update_auth_stats(success_count, failure_count)

        logger.info(f"状态加载完成 - 最后用户: {last_user}, 成功: {success_count}, 失败: {failure_count}")

    def __save_auth_status(self):
        """保存认证状态到配置文件"""
        from shmtu_auth.src.gui.common.config import qconfig

        # 自动保存配置
        qconfig.save()
        logger.debug("认证状态已保存到配置文件")

    def __update_auth_stats(self, success_count, failure_count):
        """更新认证统计显示"""
        total = success_count + failure_count
        self.auth_stats_card.setContent(f"总计: {total} | 成功: {success_count} | 失败: {failure_count}")

    def update_network_status(self, is_online: bool):
        """更新网络状态"""
        from shmtu_auth.src.gui.common.config import cfg

        if is_online:
            self.network_status_card.setContent("已连接 ✓")
        else:
            self.network_status_card.setContent("未连接 ✗")

        # 保存网络状态
        cfg.last_network_status.value = is_online
        self.__save_auth_status()

    def update_service_status(self, is_running: bool):
        """更新服务状态"""
        if is_running:
            self.service_status_card.setContent("运行中 ✓")
        else:
            self.service_status_card.setContent("已停止 ✗")

    def update_last_auth_user(self, user_id: str):
        """更新最后认证用户"""
        import datetime

        from shmtu_auth.src.gui.common.config import cfg

        # 获取当前时间
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 更新显示
        self.last_auth_card.setContent(f"{user_id} ({current_time})")

        # 保存到配置
        cfg.last_auth_user.value = user_id
        cfg.last_auth_time.value = current_time
        self.__save_auth_status()

        logger.info(f"已更新最后认证用户: {user_id} at {current_time}")

    def update_auth_attempt(self, user_id: str):
        """更新认证尝试"""
        from shmtu_auth.src.gui.common.config import cfg

        # 增加总尝试次数
        current_total = cfg.total_auth_attempts.value
        cfg.total_auth_attempts.value = current_total + 1

        # 增加当前会话尝试次数
        self.current_session_attempts += 1

        self.__save_auth_status()
        logger.debug(
            f"认证尝试计数更新: 用户={user_id}, 总计={cfg.total_auth_attempts.value}, 本次会话={self.current_session_attempts}"
        )

    def record_auth_success(self, user_id: str):
        """记录认证成功"""
        from shmtu_auth.src.gui.common.config import cfg

        # 增加成功计数
        success_count = cfg.auth_success_count.value + 1
        cfg.auth_success_count.value = success_count

        # 更新最后认证用户
        self.update_last_auth_user(user_id)

        # 更新统计显示
        failure_count = cfg.auth_failure_count.value
        self.__update_auth_stats(success_count, failure_count)

        self.__save_auth_status()
        logger.info(f"记录认证成功: {user_id}, 总成功次数: {success_count}")

    def record_auth_failure(self, user_id: str, error_msg: str):
        """记录认证失败"""
        from shmtu_auth.src.gui.common.config import cfg

        # 增加失败计数
        failure_count = cfg.auth_failure_count.value + 1
        cfg.auth_failure_count.value = failure_count

        # 更新统计显示
        success_count = cfg.auth_success_count.value
        self.__update_auth_stats(success_count, failure_count)

        self.__save_auth_status()
        logger.warning(f"记录认证失败: {user_id}, 错误: {error_msg}, 总失败次数: {failure_count}")

    def reset_counters(self):
        """重置计数器（仅重置当前会话计数，不影响历史统计）"""
        self.current_session_attempts = 0
        logger.info("当前会话计数器已重置")

    def reset_all_statistics(self):
        """重置所有统计数据（包括历史记录）"""
        from shmtu_auth.src.gui.common.config import cfg

        # 重置所有计数
        cfg.total_auth_attempts.value = 0
        cfg.auth_success_count.value = 0
        cfg.auth_failure_count.value = 0
        cfg.last_auth_user.value = ""
        cfg.last_auth_time.value = ""
        self.current_session_attempts = 0

        # 更新显示
        self.last_auth_card.setContent("无")
        self.__update_auth_stats(0, 0)

        self.__save_auth_status()
        logger.info("所有认证统计数据已重置")


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

        self.authSettingsWidget.start_card.clicked.connect(self.__on_work_button_clicked)
        self.authSettingsWidget.manual_test_card.clicked.connect(self.__on_manual_test_clicked)
        self.authSettingsWidget.reset_stats_card.clicked.connect(self.__on_reset_stats_clicked)

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
        signal_bus.signal_auth_status_changed.connect(self.authSettingsWidget.status_group.update_network_status)

        # 连接认证尝试信号
        signal_bus.signal_auth_attempt.connect(self.authSettingsWidget.status_group.update_auth_attempt)

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
        # 使用新的记录方法
        self.authSettingsWidget.status_group.record_auth_success(user_id)
        InfoBar.success("认证成功", f"用户 {user_id} 认证成功", duration=3000, parent=self)

    def __on_auth_failed(self, user_id: str, error_msg: str):
        """处理认证失败"""
        logger.warning(f"GUI收到认证失败信号：{user_id} - {error_msg}")
        # 使用新的记录方法
        self.authSettingsWidget.status_group.record_auth_failure(user_id, error_msg)
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
        """处理启动/停止按钮点击（异步优化版本）"""
        logger.info(f"认证服务按钮点击，当前状态：{self.current_status}")

        if not self.current_status:
            # 当前为False,需要启动
            logger.info("准备启动认证服务...")

            # 禁用按钮，防止重复点击
            start_button = getattr(self.authSettingsWidget.start_card, "button", None)
            if start_button:
                start_button.setEnabled(False)

            # 显示启动中状态
            InfoBar.info("启动中", "正在验证用户列表并启动认证服务...", duration=2000, parent=self)

            # 异步验证用户列表并启动服务
            self.__start_auth_service_async()

        else:
            # 当前为True,需要停止
            self.__stop_auth_service()

    def __start_auth_service_async(self):
        """异步启动认证服务"""
        # 初始化用户验证管理器（如果尚未创建）
        if not hasattr(self, "_user_validation_manager"):
            from shmtu_auth.src.gui.utils.async_network_test import NetworkTestManager

            self._user_validation_manager = NetworkTestManager()

        # 使用自定义工作线程来处理用户验证
        from PySide6.QtCore import QThread, Signal

        class UserValidationWorker(QThread):
            validation_completed = Signal(list)  # 验证完成信号，传递有效用户列表
            validation_error = Signal(str)  # 验证出错信号

            def __init__(self, user_list):
                super().__init__()
                self.user_list = user_list

            def run(self):
                try:
                    from shmtu_auth.src.datatype.shmtu.auth.auth_user import get_valid_user_list

                    valid_users = get_valid_user_list(self.user_list)
                    self.validation_completed.emit(valid_users)
                except Exception as e:
                    self.validation_error.emit(str(e))

        # 创建并启动用户验证线程
        self._validation_worker = UserValidationWorker(self.user_list)
        self._validation_worker.validation_completed.connect(self.__on_user_validation_completed)
        self._validation_worker.validation_error.connect(self.__on_user_validation_error)
        self._validation_worker.start()

    def __on_user_validation_completed(self, valid_users):
        """用户验证完成回调"""
        logger.info(f"用户验证完成，有效用户数量: {len(valid_users)}")

        if not valid_users or len(valid_users) == 0:
            logger.warning("没有有效的认证用户，无法启动认证服务")
            InfoBar.warning(
                "启动失败",
                "请先在用户列表中添加有效的认证用户",
                duration=3000,
                parent=self,
            )
            self.__restore_start_button()
            return

        # 继续启动认证服务
        self.__do_start_auth_service_with_users(valid_users)

    def __on_user_validation_error(self, error_msg):
        """用户验证出错回调"""
        logger.error(f"用户验证失败: {error_msg}")
        InfoBar.error("验证失败", f"用户验证过程中出现错误：{error_msg}", duration=3000, parent=self)
        self.__restore_start_button()

    def __do_start_auth_service_with_users(self, valid_users):
        """使用验证过的用户启动认证服务"""
        try:
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
            self.set_auth_work_status(self.current_status)

        except Exception as e:
            logger.error(f"启动认证服务时出错: {str(e)}")
            InfoBar.error("启动失败", f"启动过程中出现错误：{str(e)}", duration=3000, parent=self)

        finally:
            self.__restore_start_button()

        logger.info(f"认证服务状态已更新：{self.current_status}")

    def __restore_start_button(self):
        """恢复启动按钮状态"""
        start_button = getattr(self.authSettingsWidget.start_card, "button", None)
        if start_button:
            start_button.setEnabled(True)

    def __stop_auth_service(self):
        """停止认证服务"""
        logger.info("准备停止认证服务...")

        # 禁用按钮，防止重复点击
        start_button = getattr(self.authSettingsWidget.start_card, "button", None)
        if start_button:
            start_button.setEnabled(False)

        if self.work_thread is not None:
            if self.work_thread.is_alive():
                logger.info("停止认证线程...")
                self.work_thread.stop()
                self.work_thread.join(timeout=5)
            self.work_thread = None

        self.current_status = False
        InfoBar.info("已停止", "认证服务已停止", duration=2000, parent=self)
        self.set_auth_work_status(self.current_status)
        self.__restore_start_button()
        logger.info(f"认证服务状态已更新：{self.current_status}")

    def __restore_start_button(self):
        """恢复启动按钮状态"""
        start_button = getattr(self.authSettingsWidget.start_card, "button", None)
        if start_button:
            start_button.setEnabled(True)

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
        """处理手动测试按钮点击（异步版本）"""
        logger.info("开始手动测试网络连接（异步）...")

        # 检查是否已有测试在进行
        if hasattr(self, "_network_test_manager") and self._network_test_manager.is_testing():
            InfoBar.warning("测试进行中", "网络测试正在进行，请稍候...", duration=2000, parent=self)
            return

        # 初始化网络测试管理器（如果尚未创建）
        if not hasattr(self, "_network_test_manager"):
            from shmtu_auth.src.gui.utils.async_network_test import NetworkTestManager

            self._network_test_manager = NetworkTestManager()

        # 禁用测试按钮，防止重复点击
        test_button = getattr(self, "manual_test_button", None)
        if test_button:
            test_button.setEnabled(False)

        # 显示测试开始的提示
        InfoBar.info("测试开始", "正在异步测试网络连接状态，请稍候...", duration=2000, parent=self)

        # 启动异步网络测试
        success = self._network_test_manager.start_test(
            on_completed=self.__on_manual_test_completed,
            on_error=self.__on_manual_test_error,
            on_started=self.__on_manual_test_started,
        )

        if not success:
            # 如果启动失败，恢复按钮状态
            if test_button:
                test_button.setEnabled(True)
            InfoBar.error("启动失败", "无法启动网络测试，请重试", duration=3000, parent=self)

    def __on_manual_test_started(self):
        """手动测试开始回调"""
        logger.debug("手动网络测试已开始")

    def __on_manual_test_completed(self, is_connected: bool):
        """手动测试完成回调"""
        logger.info(f"手动测试结果：{'网络已连接' if is_connected else '网络未连接'}")

        # 恢复测试按钮
        test_button = getattr(self, "manual_test_button", None)
        if test_button:
            test_button.setEnabled(True)

        if is_connected:
            InfoBar.success("测试完成", "网络连接正常 ✓", duration=3000, parent=self)
            self.authSettingsWidget.status_group.update_network_status(True)
        else:
            InfoBar.warning("测试完成", "网络连接异常，需要认证 ✗", duration=3000, parent=self)
            self.authSettingsWidget.status_group.update_network_status(False)

    def __on_manual_test_error(self, error_msg: str):
        """手动测试出错回调"""
        logger.error(f"手动测试出错：{error_msg}")

        # 恢复测试按钮
        test_button = getattr(self, "manual_test_button", None)
        if test_button:
            test_button.setEnabled(True)

        InfoBar.error("测试失败", f"测试过程中出现错误：{error_msg}", duration=3000, parent=self)

    def __on_reset_stats_clicked(self):
        """处理重置统计按钮点击"""
        from qfluentwidgets import MessageBox, MessageBoxButton

        logger.info("用户点击重置统计按钮")

        # 创建确认对话框
        msg_box = MessageBox(
            title="确认重置",
            content="此操作将清除所有认证历史统计数据，包括：\n• 最后认证用户和时间\n• 认证成功/失败次数\n• 总认证尝试次数\n\n此操作不可撤销，是否继续？",
            parent=self,
        )

        # 设置按钮
        msg_box.yesButton.setText("重置")
        msg_box.cancelButton.setText("取消")

        # 显示对话框并处理结果
        if msg_box.exec() == MessageBoxButton.YES:
            # 用户确认重置
            logger.info("用户确认重置统计数据")
            self.authSettingsWidget.status_group.reset_all_statistics()
            InfoBar.success("重置完成", "所有认证统计数据已清除", duration=3000, parent=self)
        else:
            logger.info("用户取消重置操作")

    def cleanup(self):
        """清理认证接口资源"""
        logger.info("清理AuthInterface资源...")

        # 停止用户验证线程
        if hasattr(self, "_validation_worker"):
            if self._validation_worker.isRunning():
                logger.debug("停止用户验证线程...")
                self._validation_worker.quit()
                if not self._validation_worker.wait(3000):
                    logger.warning("用户验证线程未能正常停止，强制终止")
                    self._validation_worker.terminate()
                    self._validation_worker.wait()
            self._validation_worker = None

        # 清理网络测试管理器
        if hasattr(self, "_network_test_manager"):
            self._network_test_manager.cleanup()
            self._network_test_manager = None

        # 清理用户验证管理器
        if hasattr(self, "_user_validation_manager"):
            self._user_validation_manager.cleanup()
            self._user_validation_manager = None

        logger.info("AuthInterface资源清理完成")
