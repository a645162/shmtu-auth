# -*- coding: utf-8 -*-

"""
Unified Installation Script
Supports different installation modes: Basic, GUI, Development Environment
"""

import os
import sys
import argparse
import subprocess
from typing import List


# Fix Windows console encoding issues
def fix_console_encoding():
    """Fix console encoding issues"""
    if sys.platform.startswith("win"):
        try:
            # Try to set the console to UTF-8
            import codecs

            sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
            sys.stderr = codecs.getwriter("utf-8")(sys.stderr.detach())
        except Exception:
            # If it fails, use a safe print function
            pass


def safe_print(text):
    """Safe print function to handle encoding issues"""
    try:
        print(text)
    except UnicodeEncodeError:
        # If a encoding error occurs, replace with ASCII characters
        safe_text = text.encode("ascii", "replace").decode("ascii")
        print(safe_text)


# Fix encoding when the module is loaded
fix_console_encoding()

# Global software source configuration
PYPI_SOURCES = [
    {"name": "official", "url": "https://pypi.org/simple/", "description": "Official Source"},
    {
        "name": "tsinghua",
        "url": "https://pypi.tuna.tsinghua.edu.cn/simple/",
        "description": "Tsinghua University Source",
    },
    {
        "name": "aliyun",
        "url": "https://mirrors.aliyun.com/pypi/simple/",
        "description": "Aliyun Source",
    },
    {
        "name": "ustc",
        "url": "https://pypi.mirrors.ustc.edu.cn/simple/",
        "description": "USTC Source",
    },
    {
        "name": "tencent",
        "url": "https://mirrors.cloud.tencent.com/pypi/simple/",
        "description": "Tencent Cloud Source",
    },
]


class InstallManager:
    """Installation Manager"""

    def __init__(self, source_name: str = "official"):
        self.requirements_files = {
            "base": "requirements.txt",
            "gui": "requirements/r-gui-requirements.txt",
            "dev": "requirements/r-dev-requirements.txt",
        }
        self.source_name = source_name
        self.source_url = self._get_source_url(source_name)
        self.extra_index_params = f" -i {self.source_url}" if self.source_url else ""

        # Installation option control variables
        self.install_base_deps = False
        self.install_gui_deps = False
        self.install_dev_deps = False
        self.install_fluent_widgets = False
        self.fluent_full_version = True

    def _get_source_url(self, source_name: str) -> str:
        """Get source URL by source name"""
        for source in PYPI_SOURCES:
            if source["name"] == source_name:
                return source["url"]
        return PYPI_SOURCES[0]["url"]  # Default to official source

    def get_available_sources(self) -> List[dict]:
        """Get a list of available software sources"""
        return PYPI_SOURCES

    def show_source_info(self):
        """Show the current software source information"""
        for source in PYPI_SOURCES:
            if source["name"] == self.source_name:
                print(f"Using software source: {source['description']} ({source['url']})")
                break

    def set_install_options(self, mode: str, fluent_full: bool = True):
        """Set installation options based on the installation mode"""
        # Reset all options
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
        """Show the installation plan"""
        print("Installation Plan:")
        if self.install_base_deps:
            print(f"  ✓ Base dependencies ({self.requirements_files['base']})")
        if self.install_gui_deps:
            print(f"  ✓ GUI dependencies ({self.requirements_files['gui']})")
        if self.install_dev_deps:
            print(f"  ✓ Development environment dependencies ({self.requirements_files['dev']})")
        if self.install_fluent_widgets:
            version_type = "Full Version" if self.fluent_full_version else "Lightweight Version"
            print(f"  ✓ PySide6-Fluent-Widgets ({version_type})")

    def run_command(self, command: str) -> bool:
        """Execute a command and return whether it was successful"""
        try:
            print(f"Executing command: {command}")
            # Support os.system() call method
            result = os.system(command)
            return result == 0
        except Exception as e:
            print(f"Command execution failed: {e}")
            return False

    def run_command_subprocess(self, command: str) -> bool:
        """Execute a command using subprocess"""
        try:
            print(f"Executing command: {command}")
            result = subprocess.run(command, shell=True, check=True)
            return result.returncode == 0
        except subprocess.CalledProcessError as e:
            print(f"Command execution failed: {e}")
            return False

    def upgrade_pip(self) -> bool:
        """Upgrade pip"""
        print("Upgrading pip...")
        command = f"pip install --upgrade pip{self.extra_index_params}"
        return self.run_command(command)

    def install_requirements(self, requirements_file: str) -> bool:
        """Install dependencies from the requirements file"""
        if not os.path.exists(requirements_file):
            print(f"Error: File {requirements_file} not found")
            return False

        print(f"Installing dependencies from {requirements_file}...")
        command = f"pip install -r {requirements_file}{self.extra_index_params}"
        return self.run_command(command)

    def install_fluent_widgets_package(self) -> bool:
        """Install PySide6-Fluent-Widgets"""
        if self.fluent_full_version:
            print("Installing PySide6-Fluent-Widgets Full Version...")
            command = f'pip install --upgrade "PySide6-Fluent-Widgets[full]"{self.extra_index_params}'
        else:
            print("Installing PySide6-Fluent-Widgets Lightweight Version...")
            command = (
                f"pip install --upgrade PySide6-Fluent-Widgets{self.extra_index_params}"
            )

        return self.run_command(command)

    def execute_install(self, mode_name: str = "") -> bool:
        """Execute the installation"""
        print(f"=== {mode_name} ===")
        self.show_source_info()
        self.show_install_plan()
        print()

        success = True

        # Always upgrade pip first
        if not self.upgrade_pip():
            success = False

        # Install various dependencies in order
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
        """Install base dependencies"""
        self.set_install_options("base", fluent_full)
        return self.execute_install("Installing Base Dependencies")

    def install_gui(self, fluent_full: bool = True) -> bool:
        """Install GUI dependencies"""
        self.set_install_options("gui", fluent_full)
        return self.execute_install("Installing GUI Dependencies")

    def install_dev(self, fluent_full: bool = True) -> bool:
        """Install development environment dependencies"""
        self.set_install_options("dev", fluent_full)
        return self.execute_install("Installing Development Environment Dependencies")

    def install_all(self, fluent_full: bool = True) -> bool:
        """Install all dependencies (Base + GUI + Development Environment)"""
        self.set_install_options("all", fluent_full)
        return self.execute_install("Installing All Dependencies")

    def install_custom(
        self, requirements_files: List[str], fluent_full: bool = True
    ) -> bool:
        """Custom installation"""
        print("=== Custom Installation ===")
        self.show_source_info()
        success = True

        if not self.upgrade_pip():
            success = False

        for req_file in requirements_files:
            if not self.install_requirements(req_file):
                success = False

        # If GUI requirements are included, install Fluent Widgets
        if self.requirements_files["gui"] in requirements_files:
            self.fluent_full_version = fluent_full
            if not self.install_fluent_widgets_package():
                success = False

        return success


def main():
    # Support backward compatibility: if there are no command line arguments, default to basic installation
    if len(sys.argv) == 1:
        print("=== Default Basic Installation Mode ===")
        installer = InstallManager()
        success = installer.install_base()
        if success:
            print("\n✅ Installation Complete!")
        else:
            print("\n❌ An error occurred during installation!")
        return

    parser = argparse.ArgumentParser(
        description="Unified Installation Script - Supports different installation modes",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
Installation Mode Description:
  base    - Install only base dependencies (requirements.txt)
  gui     - Install base + GUI dependencies (requirements.txt + requirements/r-gui-requirements.txt)
  dev     - Install complete development environment (all requirements files)
  all     - Install all dependencies (Base + GUI + Development Environment)
  custom  - Custom installation of specified requirements files

Available Software Sources:
{chr(10).join([f"  {src['name']:<10} - {src['description']} ({src['url']})" for src in PYPI_SOURCES])}

Examples:
  python install.py                         # Default basic installation (backward compatible)
  python install.py base                    # Basic installation
  python install.py gui                     # GUI installation
  python install.py gui --fluent-light      # GUI installation (Lightweight Fluent Widgets)
  python install.py dev --source tsinghua   # Development environment installation (using Tsinghua source)
  python install.py all --source aliyun     # Install all dependencies (using Aliyun source)
  python install.py custom req1.txt req2.txt --source aliyun # Custom installation (using Aliyun source)
  
Supports os.system() call method:
  import os
  os.system("pip install --upgrade \\"PySide6-Fluent-Widgets[full]\\" -i https://pypi.org/simple/")
        """,
    )

    parser.add_argument(
        "mode", choices=["base", "gui", "dev", "all", "custom"], help="Installation mode"
    )

    parser.add_argument(
        "requirements", nargs="*", help="List of requirements files in custom mode"
    )

    parser.add_argument(
        "--source",
        "-s",
        choices=[src["name"] for src in PYPI_SOURCES],
        default="official",
        help="Specify pip software source (default: official)",
    )

    parser.add_argument(
        "--fluent-light",
        action="store_true",
        help="Install PySide6-Fluent-Widgets lightweight version instead of full version",
    )

    parser.add_argument(
        "--dry-run", action="store_true", help="Only show the operations to be performed, do not actually install"
    )

    parser.add_argument(
        "--list-sources", action="store_true", help="Show all available software sources"
    )

    args = parser.parse_args()

    # Show available software sources
    if args.list_sources:
        print("Available pip software sources:")
        for source in PYPI_SOURCES:
            print(f"  {source['name']:<10} - {source['description']}")
            print(f"             {source['url']}")
        return

    # Validate custom mode parameters
    if args.mode == "custom" and not args.requirements:
        parser.error("Custom mode requires specifying at least one requirements file")

    installer = InstallManager(args.source)
    fluent_full = not args.fluent_light

    # Dry run mode
    if args.dry_run:
        print("=== Dry Run Mode - Only showing operations ===")
        print(f"Installation Mode: {args.mode}")
        print(f"Software Source: {args.source}")
        installer.show_source_info()
        if args.mode == "custom":
            print(f"Requirements Files: {args.requirements}")
        print(f"Fluent Widgets Version: {'Full Version' if fluent_full else 'Lightweight Version'}")
        return

    # Execute installation
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
        print("\n✅ Installation Complete!")
        sys.exit(0)
    else:
        print("\n❌ An error occurred during installation!")
        sys.exit(1)


if __name__ == "__main__":
    main()
