# GUI 异步网络操作改进说明

## 概述

为了避免阻塞UI线程，将所有耗时的网络操作改为异步执行。

## 改进内容

### 1. 创建异步网络测试工具

- **文件**: `src/shmtu_auth/src/gui/utils/async_network_test.py`
- **功能**: 提供通用的异步网络测试功能
- **组件**:
  - `AsyncNetworkTester`: 网络测试工作线程
  - `NetworkTestManager`: 网络测试管理器，简化使用

### 2. 系统托盘异步化

- **文件**: `src/shmtu_auth/src/gui/view/system_tray.py`
- **改进**:
  - 快速网络测试改为异步执行
  - 网络状态初始化改为异步执行
  - 添加测试进度提示和状态管理
  - 防止重复测试的保护机制

### 3. 认证接口异步化

- **文件**: `src/shmtu_auth/src/gui/view/interface/auth_interface.py`
- **改进**:
  - 手动网络测试改为异步执行
  - 添加测试进度反馈
  - 按钮状态管理，防止重复点击

### 4. 主窗口资源管理

- **文件**: `src/shmtu_auth/src/gui/view/main_window.py`
- **改进**:
  - 程序退出时正确清理异步线程
  - 确保所有网络测试线程都能正常停止

## 技术特点

### 线程安全

- 使用Qt的信号槽机制进行线程间通信
- 所有UI更新都在主线程中执行
- 网络操作在独立的工作线程中执行

### 用户体验

- 网络测试时显示"检查中..."状态
- 提供实时的测试进度反馈
- 防止重复点击和并发测试

### 资源管理

- 自动清理工作线程
- 程序退出时正确停止所有异步操作
- 防止内存泄漏

## 使用方式

### 系统托盘

```python
# 快速网络测试现在是异步的
self.system_tray.__quick_network_test()

# 刷新网络状态也是异步的
self.system_tray.refresh_network_status()
```

### 认证接口

```python
# 手动测试按钮点击现在是异步的
self.auth_interface.__on_manual_test_clicked()
```

### 自定义异步网络测试

```python
from shmtu_auth.src.gui.utils.async_network_test import NetworkTestManager

manager = NetworkTestManager()
manager.start_test(
    on_completed=lambda connected: print(f"结果: {connected}"),
    on_error=lambda error: print(f"错误: {error}"),
    on_started=lambda: print("测试开始"),
    on_progress=lambda msg: print(f"进度: {msg}")
)
```

## 兼容性说明

- 不修改核心网络检查函数 (`core_exp.py`)
- 保持CLI版本的兼容性
- GUI版本获得更好的用户体验

## 性能提升

- UI不再因网络操作而冻结
- 用户可以在网络测试进行时继续使用界面
- 多个组件可以独立进行网络测试而不互相影响
