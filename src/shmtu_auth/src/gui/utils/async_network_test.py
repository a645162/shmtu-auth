"""
异步网络测试工具模块
提供GUI界面使用的异步网络检查功能
"""

from PySide6.QtCore import QThread, Signal

from shmtu_auth.src.utils.logs import get_logger

logger = get_logger()


class AsyncNetworkTester(QThread):
    """异步网络测试器，避免阻塞UI线程"""

    # 定义信号
    test_started = Signal()  # 测试开始信号
    test_completed = Signal(bool)  # 测试完成信号，传递连接状态
    test_error = Signal(str)  # 测试出错信号，传递错误信息
    test_progress = Signal(str)  # 测试进度信号，传递状态信息

    def __init__(self, parent=None):
        super().__init__(parent)
        self.is_testing = False
        self.should_stop = False

    def run(self):
        """在后台线程中执行网络检查"""
        try:
            logger.debug("AsyncNetworkTester: 开始异步网络检查...")
            self.is_testing = True
            self.should_stop = False

            # 发送测试开始信号
            self.test_started.emit()
            self.test_progress.emit("正在检查网络连接...")

            # 调用现有的网络检查函数
            from shmtu_auth.src.core.core_exp import check_is_connected

            # 检查是否被中断
            if self.should_stop:
                logger.debug("AsyncNetworkTester: 测试被中断")
                return

            is_connected = check_is_connected()

            if not self.should_stop:
                logger.debug(f"AsyncNetworkTester: 网络检查完成，结果: {is_connected}")
                self.test_completed.emit(is_connected)

        except Exception as e:
            if not self.should_stop:
                logger.error(f"AsyncNetworkTester: 网络检查异常: {str(e)}")
                self.test_error.emit(str(e))
        finally:
            self.is_testing = False

    def stop_test(self):
        """停止测试"""
        if self.is_testing:
            logger.debug("AsyncNetworkTester: 请求停止网络测试...")
            self.should_stop = True
            self.requestInterruption()

    def is_running_test(self):
        """检查是否正在测试"""
        return self.is_testing


class NetworkTestManager:
    """网络测试管理器，提供简化的异步网络测试接口"""

    def __init__(self):
        self._tester = None
        self._test_completed_callback = None
        self._test_error_callback = None
        self._test_started_callback = None
        self._test_progress_callback = None

    def start_test(self, on_completed=None, on_error=None, on_started=None, on_progress=None):
        """
        启动异步网络测试

        Args:
            on_completed: 测试完成回调函数，参数为 bool (is_connected)
            on_error: 测试出错回调函数，参数为 str (error_message)
            on_started: 测试开始回调函数，无参数
            on_progress: 测试进度回调函数，参数为 str (progress_message)

        Returns:
            bool: 如果成功启动测试返回True，如果已有测试在进行返回False
        """
        # 如果已有测试在进行，不重复启动
        if self._tester and self._tester.is_running_test():
            logger.warning("NetworkTestManager: 测试已在进行中，跳过新的测试请求")
            return False

        # 清理之前的测试器
        self._cleanup_tester()

        # 保存回调函数
        self._test_completed_callback = on_completed
        self._test_error_callback = on_error
        self._test_started_callback = on_started
        self._test_progress_callback = on_progress

        try:
            # 创建新的测试器
            self._tester = AsyncNetworkTester()

            # 连接信号
            if on_completed:
                self._tester.test_completed.connect(on_completed)
            if on_error:
                self._tester.test_error.connect(on_error)
            if on_started:
                self._tester.test_started.connect(on_started)
            if on_progress:
                self._tester.test_progress.connect(on_progress)

            # 启动测试
            self._tester.start()
            logger.debug("NetworkTestManager: 异步网络测试已启动")
            return True

        except Exception as e:
            logger.error(f"NetworkTestManager: 启动测试失败: {str(e)}")
            if on_error:
                on_error(str(e))
            return False

    def stop_test(self):
        """停止当前的网络测试"""
        if self._tester:
            self._tester.stop_test()

    def is_testing(self):
        """检查是否正在测试"""
        return self._tester and self._tester.is_running_test()

    def cleanup(self):
        """清理资源"""
        logger.debug("NetworkTestManager: 清理资源...")
        self._cleanup_tester()

    def _cleanup_tester(self):
        """清理测试器"""
        if self._tester:
            if self._tester.isRunning():
                self._tester.stop_test()
                if not self._tester.wait(3000):  # 等待3秒
                    logger.warning("NetworkTestManager: 测试线程未能正常停止，强制终止")
                    self._tester.terminate()
                    self._tester.wait()
            self._tester = None
