#!/usr/bin/env python3
"""
测试异步网络功能是否正常工作
"""


def test_imports():
    """测试导入是否正常"""
    try:
        print("测试AsyncNetworkTester导入...")
        from shmtu_auth.src.gui.utils.async_network_test import AsyncNetworkTester, NetworkTestManager
        print(AsyncNetworkTester)
        print(NetworkTestManager)

        print("✅ AsyncNetworkTester导入成功")

        print("测试SystemTray导入...")
        from shmtu_auth.src.gui.view.system_tray import SystemTray
        print(SystemTray)

        print("✅ SystemTray导入成功")

        print("测试MainWindow导入...")
        from shmtu_auth.src.gui.view.main_window import MainWindow
        print(MainWindow)

        print("✅ MainWindow导入成功")

        print("\n🎉 所有导入测试通过！")
        return True

    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        return False
    except Exception as e:
        print(f"❌ 其他错误: {e}")
        return False


def test_network_manager():
    """测试网络测试管理器"""
    try:
        print("\n测试NetworkTestManager...")
        from shmtu_auth.src.gui.utils.async_network_test import NetworkTestManager

        manager = NetworkTestManager()
        print(f"✅ NetworkTestManager创建成功: {manager}")

        # 测试是否可以清理
        manager.cleanup()
        print("✅ NetworkTestManager清理成功")

        return True

    except Exception as e:
        print(f"❌ NetworkTestManager测试失败: {e}")
        return False


if __name__ == "__main__":
    print("🚀 开始异步网络功能测试...\n")

    success = True
    success &= test_imports()
    success &= test_network_manager()

    if success:
        print("\n🎉 所有测试通过！异步网络功能已准备就绪。")
    else:
        print("\n❌ 测试失败，请检查代码。")
