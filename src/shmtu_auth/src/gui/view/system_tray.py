"""
系统托盘类 - 增强版

新增功能：
1. 网络状态显示：在托盘菜单中显示当前网络连接状态
2. 实时状态更新：网络状态会实时更新并显示不同的图标
3. 快速网络测试：测试后会自动更新网络状态显示
4. 状态同步：认证状态和网络状态保持同步更新

托盘菜单结构：
- 认证服务: [运行中/已停止] ✓/✗
- 网络状态: [已连接/未连接/检查失败] ✓/✗/⚠
- ─────────────────
- 显示主窗口
- 快速测试网络
- ─────────────────
- 退出程序
"""

from PySide6.QtGui import QIcon, QKeySequence, QShortcut
from PySide6.QtWidgets import QApplication, QMainWindow, QSystemTrayIcon
from PySide6.QtCore import QTimer
from qfluentwidgets import Action, SystemTrayMenu
from qfluentwidgets import FluentIcon as FIF

from shmtu_auth.src.gui.common.config import cfg
from shmtu_auth.src.utils.logs import get_logger

logger = get_logger()


class SystemTray:
    window: QMainWindow

    def __init__(self, window: QMainWindow):
        super().__init__()

        self.window = window

        # 菜单
        self._tray_icon_menu = SystemTrayMenu(parent=self.window)
        # 菜单项 - 先初始化为None，在创建菜单时赋值
        self._restore_action = None
        self._quit_action = None
        self._auth_status_action = None
        self._network_status_action = None

        # 托盘图标
        self.tray_icon = QSystemTrayIcon(self.window)
        # 设置托盘的属性
        self.tray_icon.setIcon(QIcon(":/gui/Logo32"))
        self.tray_icon.setToolTip("SHMTU Auth - 校园网认证助手")

        # 连接系统托盘图标的激活事件
        self.tray_icon.activated.connect(lambda reason: self.__on_tray_icon_activated(reason))

        self.__create_menu_action()
        self.tray_icon.setContextMenu(self._tray_icon_menu)

        self.tray_icon.show()

        # 应用程序键盘监听
        self.__listen_keyboard()

        logger.info("系统托盘初始化完成")

    def show_notification(self, title: str, message: str, duration: int = 3000):
        """显示托盘通知"""
        if cfg.show_tray_notifications.value and self.tray_icon.supportsMessages():
            self.tray_icon.showMessage(title, message, QSystemTrayIcon.MessageIcon.Information, duration)
            logger.info(f"显示托盘通知: {title} - {message}")

    def update_auth_status(self, is_running: bool | None = None, is_online: bool | None = None):
        """更新认证状态显示"""
        logger.debug(f"更新认证状态: is_running={is_running}, is_online={is_online}")
        logger.debug(f"当前认证状态Action ID: {id(self._auth_status_action) if self._auth_status_action else 'None'}")

        # 确保Action对象已创建
        if self._auth_status_action is None:
            logger.warning("认证状态Action未创建，无法更新状态")
            return

        # 处理运行状态更新
        if is_running is not None:
            if is_running:
                self._auth_status_action.setText("认证服务: 运行中 ✓")
                self.tray_icon.setToolTip("SHMTU Auth - 认证服务运行中")
                logger.debug("托盘状态已更新为: 运行中")
            else:
                self._auth_status_action.setText("认证服务: 已停止 ✗")
                self.tray_icon.setToolTip("SHMTU Auth - 认证服务已停止")
                logger.debug("托盘状态已更新为: 已停止")

        # 处理在线状态更新（同时更新网络状态Action和工具提示）
        if is_online is not None:
            # 更新网络状态Action
            self.update_network_status_only(is_online)

            # 更新工具提示
            current_tooltip = self.tray_icon.toolTip()
            # 移除之前的网络状态信息
            if " | 网络" in current_tooltip:
                current_tooltip = current_tooltip.split(" | 网络")[0]

            if is_online:
                self.tray_icon.setToolTip(f"{current_tooltip} | 网络已连接")
                logger.debug("托盘提示已更新: 网络已连接")
            else:
                self.tray_icon.setToolTip(f"{current_tooltip} | 网络未连接")
                logger.debug("托盘提示已更新: 网络未连接")

    def __restore_from_tray(self):
        logger.info("restore_from_tray")

        # 还原窗口
        if self.window.isMinimized():
            self.window.showNormal()
        elif self.window.isMaximized():
            self.window.showMaximized()
        else:
            self.window.show()

    def __on_tray_icon_activated(self, reason):
        """托盘图标点击事件处理"""
        logger.debug(f"托盘图标激活事件: {reason}")

        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            # 单击事件
            logger.debug("托盘图标单击")

        elif reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            # 双击事件
            logger.debug("托盘图标双击")

            action = cfg.tray_double_click_action.value
            if action == "show_hide":
                self.__show_or_hide_window()
            elif action == "show_only":
                self.__restore_from_tray()
            elif action == "hide_only":
                self.window.hide()

        elif reason == QSystemTrayIcon.ActivationReason.MiddleClick:
            # 中键点击
            logger.debug("托盘图标中键点击")

        elif reason == QSystemTrayIcon.ActivationReason.Context:
            # 右键点击 - 显示上下文菜单
            logger.debug("托盘图标右键点击")

    def __create_menu_action(self):
        """创建托盘菜单"""
        # 认证状态显示
        self._auth_status_action = Action(FIF.INFO, "认证服务: 未知")
        self._auth_status_action.setEnabled(False)  # 只用于显示状态，不可点击

        # 网络状态显示
        self._network_status_action = Action(FIF.WIFI, "网络状态: 未知")
        self._network_status_action.setEnabled(False)  # 只用于显示状态，不可点击

        self._restore_action = Action(FIF.LINK, "显示主窗口")
        self._restore_action.triggered.connect(lambda: self.__restore_from_tray())

        # 快速操作
        self._quick_test_action = Action(FIF.SYNC, "快速测试网络")
        self._quick_test_action.triggered.connect(self.__quick_network_test)

        self._quit_action = Action(FIF.CLOSE, "退出程序")
        self._quit_action.triggered.connect(self.__quit_application)

        # 添加到菜单
        self._tray_icon_menu.addAction(self._auth_status_action)
        self._tray_icon_menu.addAction(self._network_status_action)
        self._tray_icon_menu.addSeparator()
        self._tray_icon_menu.addAction(self._restore_action)
        self._tray_icon_menu.addAction(self._quick_test_action)
        self._tray_icon_menu.addSeparator()
        self._tray_icon_menu.addAction(self._quit_action)

        logger.debug(f"托盘菜单创建完成，认证状态Action ID: {id(self._auth_status_action)}")
        logger.debug(f"网络状态Action ID: {id(self._network_status_action)}")

        # 初始化网络状态
        self.__update_network_status()

    def __quick_network_test(self):
        """快速网络测试"""
        logger.info("从托盘执行快速网络测试")
        try:
            from shmtu_auth.src.core.core_exp import check_is_connected

            is_connected = check_is_connected()

            # 更新网络状态显示
            self.update_network_status_only(is_connected)

            if is_connected:
                self.show_notification("网络测试", "网络连接正常 ✓")
            else:
                self.show_notification("网络测试", "网络连接异常，需要认证 ✗")

        except Exception as e:
            logger.error(f"快速网络测试失败: {str(e)}")
            self.show_notification("网络测试", f"测试失败: {str(e)}")
            # 测试失败时显示为检查失败状态
            if self._network_status_action:
                self._network_status_action.setText("网络状态: 检查失败 ⚠")
                self._network_status_action.setIcon(FIF.LABEL)

    def __quit_application(self):
        """退出应用程序"""
        logger.info("从托盘退出应用程序")

        try:
            # 调用主窗口的强制退出方法
            self.window.force_quit()

            # 等待一下，然后检查是否退出
            QTimer.singleShot(1000, self.__force_quit_if_needed)

        except Exception as e:
            logger.error(f"托盘退出失败: {e}")
            self.__force_quit_if_needed()

    def __force_quit_if_needed(self):
        """如果程序还没退出，强制退出"""
        logger.info("检查程序是否需要强制退出")
        try:
            if QApplication.instance():
                logger.info("强制退出应用程序")
                QApplication.instance().quit()
        except Exception as e:
            logger.error(f"强制退出失败: {e}")
            import sys

            logger.info("使用sys.exit强制退出")
            sys.exit(0)

    def __listen_keyboard(self):
        # 键盘监听
        shortcut = QShortcut(QKeySequence("Esc"), self.window)
        # 当按下 Esc 键时隐藏窗口
        shortcut.activated.connect(self.window.hide)

    def __show_or_hide_window(self):
        logger.debug("show_or_hide_window")
        if self.window.isVisible():
            logger.debug("hide_window")
            self.window.hide()
        else:
            logger.debug("show_window")
            self.window.show()

    def test_status_update(self):
        """测试状态更新功能 - 仅用于调试"""
        logger.info("开始测试托盘状态更新...")

        # 测试运行状态更新
        logger.info("测试更新为运行中...")
        self.update_auth_status(is_running=True)

        # 等待2秒
        QTimer.singleShot(2000, lambda: self._test_stopped_status())

    def _test_stopped_status(self):
        """测试停止状态"""
        logger.info("测试更新为已停止...")
        self.update_auth_status(is_running=False)

        # 测试在线状态
        QTimer.singleShot(2000, lambda: self._test_online_status())

    def _test_online_status(self):
        """测试在线状态"""
        logger.info("测试更新网络状态...")
        self.update_auth_status(is_running=None, is_online=True)

        # 测试离线状态
        QTimer.singleShot(2000, lambda: self._test_offline_status())

    def _test_offline_status(self):
        """测试离线状态"""
        logger.info("测试更新为离线状态...")
        self.update_auth_status(is_running=None, is_online=False)
        logger.info("托盘状态测试完成")

    def __update_network_status(self):
        """更新网络状态显示"""
        try:
            from shmtu_auth.src.core.core_exp import check_is_connected

            logger.debug("检查网络连接状态...")
            is_connected = check_is_connected()

            if self._network_status_action is None:
                logger.warning("网络状态Action未创建，无法更新状态")
                return

            if is_connected:
                self._network_status_action.setText("网络状态: 已连接 ✓")
                self._network_status_action.setIcon(FIF.WIFI)
                logger.debug("网络状态已更新为: 已连接")
            else:
                self._network_status_action.setText("网络状态: 未连接 ✗")
                self._network_status_action.setIcon(FIF.DISCONNECT)
                logger.debug("网络状态已更新为: 未连接")

        except Exception as e:
            logger.error(f"更新网络状态失败: {str(e)}")
            if self._network_status_action:
                self._network_status_action.setText("网络状态: 检查失败 ⚠")
                self._network_status_action.setIcon(FIF.LABEL)

    def update_network_status_only(self, is_online: bool):
        """仅更新网络状态显示（不影响认证状态）"""
        logger.debug(f"更新网络状态: is_online={is_online}")

        if self._network_status_action is None:
            logger.warning("网络状态Action未创建，无法更新状态")
            return

        if is_online:
            self._network_status_action.setText("网络状态: 已连接 ✓")
            self._network_status_action.setIcon(FIF.WIFI)
            logger.debug("网络状态已更新为: 已连接")
        else:
            self._network_status_action.setText("网络状态: 未连接 ✗")
            self._network_status_action.setIcon(FIF.DISCONNECT)
            logger.debug("网络状态已更新为: 未连接")

    def refresh_network_status(self):
        """刷新网络状态（公共方法，可被外部调用）"""
        logger.info("手动刷新网络状态")
        self.__update_network_status()
