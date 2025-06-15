# -*- coding: utf-8 -*-

from PySide6.QtCore import QObject, Signal


class SignalBus(QObject):
    """Signal bus"""

    signal_log_new = Signal(str, str)
    signal_new_version = Signal(str)

    # 认证相关信号
    signal_auth_status_changed = Signal(bool)  # 网络连接状态变化
    signal_auth_attempt = Signal(str)  # 认证尝试 (用户ID)
    signal_auth_success = Signal(str)  # 认证成功 (用户ID)
    signal_auth_failed = Signal(str, str)  # 认证失败 (用户ID, 错误信息)
    signal_auth_thread_started = Signal()  # 认证线程启动
    signal_auth_thread_stopped = Signal()  # 认证线程停止


signal_bus = SignalBus()


def log_new(event: str, status: str):
    signal_bus.signal_log_new.emit(event, status)


def auth_status_changed(is_online: bool):
    """网络连接状态变化"""
    signal_bus.signal_auth_status_changed.emit(is_online)


def auth_attempt(user_id: str):
    """认证尝试"""
    signal_bus.signal_auth_attempt.emit(user_id)
    log_new("Auth", f"尝试认证用户: {user_id}")


def auth_success(user_id: str):
    """认证成功"""
    signal_bus.signal_auth_success.emit(user_id)
    log_new("Auth", f"认证成功: {user_id}")


def auth_failed(user_id: str, error_msg: str):
    """认证失败"""
    signal_bus.signal_auth_failed.emit(user_id, error_msg)
    log_new("Auth", f"认证失败: {user_id} - {error_msg}")


def auth_thread_started():
    """认证线程启动"""
    signal_bus.signal_auth_thread_started.emit()
    log_new("Auth", "认证服务已启动")


def auth_thread_stopped():
    """认证线程停止"""
    signal_bus.signal_auth_thread_stopped.emit()
    log_new("Auth", "认证服务已停止")
