#!/usr/bin/env python3
"""
验证 UV 环境设置的脚本
"""

import subprocess
import sys
from pathlib import Path


def run_command(cmd):
    """运行命令并返回结果"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=Path(__file__).parent)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)


def check_uv_installation():
    """检查 uv 是否安装"""
    print("🔍 检查 UV 安装状态...")
    success, stdout, stderr = run_command("uv --version")

    if success:
        print(f"✅ UV 已安装: {stdout.strip()}")
        return True
    else:
        print("❌ UV 未安装或不在 PATH 中")
        print("请运行以下命令安装 UV:")
        print("  Windows: Invoke-RestMethod https://astral.sh/uv/install.ps1 | Invoke-Expression")
        print("  Linux/macOS: curl -LsSf https://astral.sh/uv/install.sh | sh")
        return False


def check_python_version():
    """检查 Python 版本"""
    print("\n🐍 检查 Python 版本...")

    # 检查当前 Python 版本
    current_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    print(f"✅ 当前 Python 版本: {current_version}")

    # 检查 .python-version 文件
    python_version_file = Path(".python-version")
    if python_version_file.exists():
        required_version = python_version_file.read_text().strip()
        print(f"📄 项目要求的 Python 版本: {required_version}")

        if sys.version_info >= tuple(map(int, required_version.split("."))):
            print("✅ Python 版本满足要求")
            return True
        else:
            print(f"⚠️  建议使用 Python {required_version} 或更高版本")
            return False
    else:
        print("⚠️  未找到 .python-version 文件")
        return True


def check_project_files():
    """检查项目文件"""
    print("\n📁 检查项目文件...")

    required_files = ["pyproject.toml", "requirements.txt", "start_cli.py", "src/shmtu_auth"]

    all_exist = True
    for file_path in required_files:
        path = Path(file_path)
        if path.exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} 不存在")
            all_exist = False

    return all_exist


def check_uv_sync():
    """检查 uv sync 是否工作"""
    print("\n📦 检查依赖同步...")

    success, stdout, stderr = run_command("uv sync --dry-run")

    if success:
        print("✅ UV 同步检查通过")
        return True
    else:
        print("❌ UV 同步检查失败:")
        print(f"错误: {stderr}")
        return False


def check_project_run():
    """检查项目是否能运行"""
    print("\n🚀 检查项目运行...")

    success, stdout, stderr = run_command("uv run python start_cli.py --help")

    if success:
        print("✅ 项目可以正常运行")
        return True
    else:
        print("❌ 项目运行失败:")
        print(f"错误: {stderr}")
        return False


def main():
    """主函数"""
    print("🔧 SHMTU-Auth UV 环境验证")
    print("=" * 50)

    checks = [
        ("UV 安装", check_uv_installation),
        ("Python 版本", check_python_version),
        ("项目文件", check_project_files),
        ("依赖同步", check_uv_sync),
        ("项目运行", check_project_run),
    ]

    passed = 0
    total = len(checks)

    for _name, check_func in checks:
        if check_func():
            passed += 1
        print()

    print("=" * 50)
    print(f"📊 验证结果: {passed}/{total} 项检查通过")

    if passed == total:
        print("🎉 恭喜！UV 环境配置完成，可以开始使用了！")
        print("\n💡 常用命令:")
        print("  uv run python start_cli.py    # 运行程序")
        print("  uv add <package>               # 添加依赖")
        print("  uv sync                        # 同步依赖")
        print("  uv run pytest                 # 运行测试")
        return 0
    else:
        print("❌ 部分检查未通过，请根据上述信息进行修复")
        return 1


if __name__ == "__main__":
    sys.exit(main())
