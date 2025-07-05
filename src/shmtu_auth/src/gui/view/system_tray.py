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

from PySide6.QtCore import QTimer
from PySide6.QtGui import QIcon, QKeySequence, QShortcut
from PySide6.QtWidgets import QApplication, QMainWindow, QSystemTrayIcon
from qfluentwidgets import Action, SystemTrayMenu
from qfluentwidgets import FluentIcon as FIF

from shmtu_auth.src.gui.common.config import cfg
from shmtu_auth.src.gui.utils.async_network_test import NetworkTestManager
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

        # 网络测试管理器
        self._network_test_manager = NetworkTestManager()

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

        # 跨平台窗口激活处理
        self.__activate_window_cross_platform()

        logger.debug("窗口已还原并激活")

    def __activate_window_cross_platform(self):
        """跨平台窗口激活处理"""
        import sys

        try:
            # 首先使用标准Qt方法
            self.window.activateWindow()
            self.window.raise_()

            # 根据不同平台进行特殊处理
            if sys.platform == "win32":
                self.__activate_window_windows()
            elif sys.platform == "darwin":
                self.__activate_window_macos()
            elif sys.platform.startswith("linux"):
                self.__activate_window_linux()
            else:
                logger.debug(f"未知平台 {sys.platform}，仅使用Qt标准方法")

        except Exception as e:
            logger.error(f"跨平台窗口激活失败: {e}")
            # fallback到基本的Qt方法
            try:
                self.window.activateWindow()
                self.window.raise_()
            except Exception as fallback_e:
                logger.error(f"Qt标准激活方法也失败: {fallback_e}")

    def __activate_window_windows(self):
        """Windows系统特定的窗口激活处理"""
        try:
            import ctypes

            # 获取窗口句柄
            hwnd = int(self.window.winId())

            # 强制窗口置于前台
            user32 = ctypes.windll.user32
            kernel32 = ctypes.windll.kernel32

            # 获取当前前台窗口的线程ID
            current_thread_id = kernel32.GetCurrentThreadId()
            foreground_window = user32.GetForegroundWindow()

            if foreground_window:
                foreground_thread_id = user32.GetWindowThreadProcessId(foreground_window, None)

                # 如果不是同一个线程，需要附加到前台线程
                if foreground_thread_id != current_thread_id:
                    user32.AttachThreadInput(foreground_thread_id, current_thread_id, True)
                    user32.SetForegroundWindow(hwnd)
                    user32.AttachThreadInput(foreground_thread_id, current_thread_id, False)
                else:
                    user32.SetForegroundWindow(hwnd)
            else:
                user32.SetForegroundWindow(hwnd)

            # 确保窗口可见并激活
            user32.ShowWindow(hwnd, 9)  # SW_RESTORE
            user32.SetActiveWindow(hwnd)

            logger.debug("Windows API窗口激活完成")

        except Exception as e:
            logger.warning(f"Windows API激活窗口失败: {e}")

    def __activate_window_macos(self):
        """macOS系统特定的窗口激活处理"""
        try:
            # 在macOS上，使用NSApp来激活应用
            try:
                from AppKit import NSApp

                # 激活应用程序
                NSApp.activateIgnoringOtherApps_(True)
                logger.debug("macOS NSApp窗口激活完成")

            except ImportError:
                # 如果没有PyObjC，尝试使用osascript
                import os
                import subprocess

                # 使用AppleScript激活应用
                script = f"""
                tell application "System Events"
                    set frontmost of first process whose unix id is {os.getpid()} to true
                end tell
                """

                subprocess.run(["osascript", "-e", script], capture_output=True, timeout=5)
                logger.debug("macOS osascript窗口激活完成")

        except Exception as e:
            logger.warning(f"macOS窗口激活失败: {e}")

    def __activate_window_linux(self):
        """Linux系统特定的窗口激活处理"""
        try:
            # 在Linux上，尝试使用X11方法
            import subprocess

            # 获取窗口ID
            wid = int(self.window.winId())

            # 尝试使用wmctrl激活窗口
            try:
                subprocess.run(["wmctrl", "-i", "-a", str(wid)], capture_output=True, timeout=5, check=True)
                logger.debug("Linux wmctrl窗口激活完成")
                return
            except (subprocess.CalledProcessError, FileNotFoundError):
                pass

            # 如果wmctrl不可用，尝试使用xdotool
            try:
                subprocess.run(["xdotool", "windowactivate", str(wid)], capture_output=True, timeout=5, check=True)
                logger.debug("Linux xdotool窗口激活完成")
                return
            except (subprocess.CalledProcessError, FileNotFoundError):
                pass

            # 如果以上都不可用，尝试直接使用Qt方法
            try:
                # 请求注意力
                self.window.requestActivate()

                # 尝试设置窗口属性
                if hasattr(self.window, "setWindowState"):
                    from PySide6.QtCore import Qt

                    self.window.setWindowState(Qt.WindowState.WindowActive)

                logger.debug("Linux Qt方法窗口激活完成")

            except Exception as qt_e:
                logger.warning(f"Linux Qt方法激活失败: {qt_e}")

        except Exception as e:
            logger.warning(f"Linux窗口激活失败: {e}")

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

        # 初始化网络状态（异步）
        self.__update_network_status_async()

    def __quick_network_test(self):
        """快速网络测试（异步版本）"""
        logger.info("从托盘执行快速网络测试（异步）")

        # 如果已有测试在进行，不重复启动
        if self._network_test_manager.is_testing():
            logger.info("网络测试已在进行中，跳过")
            self.show_notification("网络测试", "测试正在进行中，请稍候...")
            return

        # 禁用快速测试按钮，防止重复点击
        if self._quick_test_action:
            self._quick_test_action.setEnabled(False)

        # 显示测试开始状态
        if self._network_status_action:
            self._network_status_action.setText("网络状态: 检查中... ⏳")
            self._network_status_action.setIcon(FIF.SYNC)

        # 启动异步网络检查
        success = self._network_test_manager.start_test(
            on_started=self.__on_quick_test_started,
            on_completed=self.__on_quick_test_completed,
            on_error=self.__on_quick_test_error,
            on_progress=self.__on_quick_test_progress,
        )

        if not success:
            # 如果启动失败，恢复按钮状态
            if self._quick_test_action:
                self._quick_test_action.setEnabled(True)

    def __on_quick_test_started(self):
        """快速测试开始回调"""
        logger.debug("快速网络测试已开始")
        self.show_notification("网络测试", "正在检查网络连接...")

    def __on_quick_test_progress(self, message: str):
        """快速测试进度回调"""
        logger.debug(f"快速网络测试进度: {message}")

    def __on_quick_test_completed(self, is_connected: bool):
        """快速测试完成回调"""
        logger.debug(f"快速网络测试完成，结果: {is_connected}")

        # 更新网络状态显示
        self.update_network_status_only(is_connected)

        # 显示结果通知
        if is_connected:
            self.show_notification("网络测试", "网络连接正常 ✓")
        else:
            self.show_notification("网络测试", "网络连接异常，需要认证 ✗")

        # 启用快速测试按钮
        if self._quick_test_action:
            self._quick_test_action.setEnabled(True)

    def __on_quick_test_error(self, error_msg: str):
        """快速测试出错回调"""
        logger.error(f"快速网络测试失败: {error_msg}")

        # 显示错误状态
        if self._network_status_action:
            self._network_status_action.setText("网络状态: 检查失败 ⚠")
            self._network_status_action.setIcon(FIF.LABEL)

        self.show_notification("网络测试", f"测试失败: {error_msg}")

        # 启用快速测试按钮
        if self._quick_test_action:
            self._quick_test_action.setEnabled(True)

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
            # 使用跨平台激活方法
            self.__activate_window_cross_platform()

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
        """刷新网络状态（公共方法，可被外部调用）- 异步版本"""
        logger.info("手动刷新网络状态（异步）")
        self.__update_network_status_async()

    def __update_network_status_async(self):
        """异步更新网络状态显示"""
        logger.debug("启动异步网络状态检查...")

        # 显示检查中状态
        if self._network_status_action:
            self._network_status_action.setText("网络状态: 检查中... ⏳")
            self._network_status_action.setIcon(FIF.SYNC)

        # 启动异步检查
        self._network_test_manager.start_test(
            on_completed=self.__on_network_status_checked, on_error=self.__on_network_status_check_error
        )

    def __on_network_status_checked(self, is_connected: bool):
        """网络状态检查完成回调"""
        logger.debug(f"网络状态检查完成，结果: {is_connected}")

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

    def __on_network_status_check_error(self, error_msg: str):
        """网络状态检查出错回调"""
        logger.error(f"网络状态检查失败: {error_msg}")

        if self._network_status_action:
            self._network_status_action.setText("网络状态: 检查失败 ⚠")
            self._network_status_action.setIcon(FIF.LABEL)

    def cleanup(self):
        """清理资源，包括停止网络检查线程"""
        logger.info("清理SystemTray资源...")

        # 停止网络测试管理器
        if self._network_test_manager:
            self._network_test_manager.cleanup()
            self._network_test_manager = None

        # 隐藏托盘图标
        if hasattr(self, "tray_icon"):
            self.tray_icon.hide()

        logger.info("SystemTray资源清理完成")
