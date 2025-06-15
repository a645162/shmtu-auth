#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统一安装脚本
支持不同的安装模式：基础、GUI、开发环境
"""

import os
import sys
import argparse
import subprocess
from typing import List

# 全局软件源配置
PYPI_SOURCES = [
    {"name": "official", "url": "https://pypi.org/simple/", "description": "官方源"},
    {
        "name": "tsinghua",
        "url": "https://pypi.tuna.tsinghua.edu.cn/simple/",
        "description": "清华大学源",
    },
    {
        "name": "aliyun",
        "url": "https://mirrors.aliyun.com/pypi/simple/",
        "description": "阿里云源",
    },
    {
        "name": "ustc",
        "url": "https://pypi.mirrors.ustc.edu.cn/simple/",
        "description": "中科大源",
    },
    {
        "name": "tencent",
        "url": "https://mirrors.cloud.tencent.com/pypi/simple/",
        "description": "腾讯云源",
    },
]


class InstallManager:
    """安装管理器"""

    def __init__(self, source_name: str = "official"):
        self.requirements_files = {
            "base": "requirements.txt",
            "gui": "requirements/r-gui-requirements.txt",
            "dev": "requirements/r-dev-requirements.txt",
        }
        self.source_name = source_name
        self.source_url = self._get_source_url(source_name)
        self.extra_index_params = f" -i {self.source_url}" if self.source_url else ""

        # 安装选项控制变量
        self.install_base_deps = False
        self.install_gui_deps = False
        self.install_dev_deps = False
        self.install_fluent_widgets = False
        self.fluent_full_version = True

    def _get_source_url(self, source_name: str) -> str:
        """根据源名称获取源URL"""
        for source in PYPI_SOURCES:
            if source["name"] == source_name:
                return source["url"]
        return PYPI_SOURCES[0]["url"]  # 默认返回官方源

    def get_available_sources(self) -> List[dict]:
        """获取可用的软件源列表"""
        return PYPI_SOURCES

    def show_source_info(self):
        """显示当前使用的软件源信息"""
        for source in PYPI_SOURCES:
            if source["name"] == self.source_name:
                print(f"使用软件源: {source['description']} ({source['url']})")
                break

    def set_install_options(self, mode: str, fluent_full: bool = True):
        """根据安装模式设置安装选项"""
        # 重置所有选项
        self.install_base_deps = False
        self.install_gui_deps = False
        self.install_dev_deps = False
        self.install_fluent_widgets = False
        self.fluent_full_version = fluent_full

        if mode == "base":
            self.install_base_deps = True
        elif mode == "gui":
            self.install_base_deps = True
            self.install_gui_deps = True
            self.install_fluent_widgets = True
        elif mode == "dev":
            self.install_base_deps = True
            self.install_gui_deps = True
            self.install_dev_deps = True
            self.install_fluent_widgets = True
        elif mode == "all":
            self.install_base_deps = True
            self.install_gui_deps = True
            self.install_dev_deps = True
            self.install_fluent_widgets = True

    def show_install_plan(self):
        """显示安装计划"""
        print("安装计划:")
        if self.install_base_deps:
            print(f"  ✓ 基础依赖 ({self.requirements_files['base']})")
        if self.install_gui_deps:
            print(f"  ✓ GUI依赖 ({self.requirements_files['gui']})")
        if self.install_dev_deps:
            print(f"  ✓ 开发环境依赖 ({self.requirements_files['dev']})")
        if self.install_fluent_widgets:
            version_type = "完整版" if self.fluent_full_version else "轻量版"
            print(f"  ✓ PySide6-Fluent-Widgets ({version_type})")

    def run_command(self, command: str) -> bool:
        """执行命令并返回是否成功"""
        try:
            print(f"执行命令: {command}")
            # 支持os.system()调用方式
            result = os.system(command)
            return result == 0
        except Exception as e:
            print(f"命令执行失败: {e}")
            return False

    def run_command_subprocess(self, command: str) -> bool:
        """使用subprocess执行命令"""
        try:
            print(f"执行命令: {command}")
            result = subprocess.run(command, shell=True, check=True)
            return result.returncode == 0
        except subprocess.CalledProcessError as e:
            print(f"命令执行失败: {e}")
            return False

    def upgrade_pip(self) -> bool:
        """升级pip"""
        print("正在升级pip...")
        command = f"pip install --upgrade pip{self.extra_index_params}"
        return self.run_command(command)

    def install_requirements(self, requirements_file: str) -> bool:
        """安装requirements文件中的依赖"""
        if not os.path.exists(requirements_file):
            print(f"错误: 找不到文件 {requirements_file}")
            return False

        print(f"正在安装 {requirements_file} 中的依赖...")
        command = f"pip install -r {requirements_file}{self.extra_index_params}"
        return self.run_command(command)

    def install_fluent_widgets_package(self) -> bool:
        """安装PySide6-Fluent-Widgets"""
        if self.fluent_full_version:
            print("正在安装PySide6-Fluent-Widgets完整版...")
            command = f'pip install --upgrade "PySide6-Fluent-Widgets[full]"{self.extra_index_params}'
        else:
            print("正在安装PySide6-Fluent-Widgets轻量版...")
            command = (
                f"pip install --upgrade PySide6-Fluent-Widgets{self.extra_index_params}"
            )

        return self.run_command(command)

    def execute_install(self, mode_name: str = "") -> bool:
        """执行安装"""
        print(f"=== {mode_name} ===")
        self.show_source_info()
        self.show_install_plan()
        print()

        success = True

        # 总是先升级pip
        if not self.upgrade_pip():
            success = False

        # 按顺序安装各种依赖
        if self.install_base_deps:
            if not self.install_requirements(self.requirements_files["base"]):
                success = False

        if self.install_gui_deps:
            if not self.install_requirements(self.requirements_files["gui"]):
                success = False

        if self.install_dev_deps:
            if not self.install_requirements(self.requirements_files["dev"]):
                success = False

        if self.install_fluent_widgets:
            if not self.install_fluent_widgets_package():
                success = False

        return success

    def install_base(self, fluent_full: bool = True) -> bool:
        """安装基础依赖"""
        self.set_install_options("base", fluent_full)
        return self.execute_install("安装基础依赖")

    def install_gui(self, fluent_full: bool = True) -> bool:
        """安装GUI依赖"""
        self.set_install_options("gui", fluent_full)
        return self.execute_install("安装GUI依赖")

    def install_dev(self, fluent_full: bool = True) -> bool:
        """安装开发环境依赖"""
        self.set_install_options("dev", fluent_full)
        return self.execute_install("安装开发环境依赖")

    def install_all(self, fluent_full: bool = True) -> bool:
        """安装所有依赖（基础+GUI+开发环境）"""
        self.set_install_options("all", fluent_full)
        return self.execute_install("安装所有依赖")

    def install_custom(
        self, requirements_files: List[str], fluent_full: bool = True
    ) -> bool:
        """自定义安装"""
        print("=== 自定义安装 ===")
        self.show_source_info()
        success = True

        if not self.upgrade_pip():
            success = False

        for req_file in requirements_files:
            if not self.install_requirements(req_file):
                success = False

        # 如果包含GUI requirements，则安装Fluent Widgets
        if self.requirements_files["gui"] in requirements_files:
            self.fluent_full_version = fluent_full
            if not self.install_fluent_widgets_package():
                success = False

        return success


def main():
    # 支持向后兼容：如果没有命令行参数，默认执行基础安装
    if len(sys.argv) == 1:
        print("=== 默认基础安装模式 ===")
        installer = InstallManager()
        success = installer.install_base()
        if success:
            print("\n✅ 安装完成!")
        else:
            print("\n❌ 安装过程中出现错误!")
        return

    parser = argparse.ArgumentParser(
        description="统一安装脚本 - 支持不同的安装模式",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
安装模式说明:
  base    - 仅安装基础依赖 (requirements.txt)
  gui     - 安装基础 + GUI依赖 (requirements.txt + requirements/r-gui-requirements.txt)
  dev     - 安装完整开发环境 (所有requirements文件)
  all     - 安装所有依赖 (基础 + GUI + 开发环境)
  custom  - 自定义安装指定的requirements文件

可用软件源:
{chr(10).join([f"  {src['name']:<10} - {src['description']} ({src['url']})" for src in PYPI_SOURCES])}

示例:
  python install.py                         # 默认基础安装(向后兼容)
  python install.py base                    # 基础安装
  python install.py gui                     # GUI安装
  python install.py gui --fluent-light      # GUI安装(轻量版Fluent Widgets)
  python install.py dev --source tsinghua   # 开发环境安装(使用清华源)
  python install.py all --source aliyun     # 安装所有依赖(使用阿里云源)
  python install.py custom req1.txt req2.txt --source aliyun # 自定义安装(使用阿里云源)
  
支持os.system()调用方式:
  import os
  os.system("pip install --upgrade \\"PySide6-Fluent-Widgets[full]\\" -i https://pypi.org/simple/")
        """,
    )

    parser.add_argument(
        "mode", choices=["base", "gui", "dev", "all", "custom"], help="安装模式"
    )

    parser.add_argument(
        "requirements", nargs="*", help="自定义模式下的requirements文件列表"
    )

    parser.add_argument(
        "--source",
        "-s",
        choices=[src["name"] for src in PYPI_SOURCES],
        default="official",
        help="指定pip软件源 (默认: official)",
    )

    parser.add_argument(
        "--fluent-light",
        action="store_true",
        help="安装PySide6-Fluent-Widgets轻量版而非完整版",
    )

    parser.add_argument(
        "--dry-run", action="store_true", help="仅显示将要执行的操作，不实际安装"
    )

    parser.add_argument(
        "--list-sources", action="store_true", help="显示所有可用的软件源"
    )

    args = parser.parse_args()

    # 显示可用软件源
    if args.list_sources:
        print("可用的pip软件源:")
        for source in PYPI_SOURCES:
            print(f"  {source['name']:<10} - {source['description']}")
            print(f"             {source['url']}")
        return

    # 验证自定义模式参数
    if args.mode == "custom" and not args.requirements:
        parser.error("自定义模式需要指定至少一个requirements文件")

    installer = InstallManager(args.source)
    fluent_full = not args.fluent_light

    # 干运行模式
    if args.dry_run:
        print("=== 干运行模式 - 仅显示操作 ===")
        print(f"安装模式: {args.mode}")
        print(f"软件源: {args.source}")
        installer.show_source_info()
        if args.mode == "custom":
            print(f"Requirements文件: {args.requirements}")
        print(f"Fluent Widgets版本: {'完整版' if fluent_full else '轻量版'}")
        return

    # 执行安装
    success = False

    if args.mode == "base":
        success = installer.install_base()
    elif args.mode == "gui":
        success = installer.install_gui(fluent_full)
    elif args.mode == "dev":
        success = installer.install_dev(fluent_full)
    elif args.mode == "all":
        success = installer.install_all(fluent_full)
    elif args.mode == "custom":
        success = installer.install_custom(args.requirements, fluent_full)

    if success:
        print("\n✅ 安装完成!")
        sys.exit(0)
    else:
        print("\n❌ 安装过程中出现错误!")
        sys.exit(1)


if __name__ == "__main__":
    main()
