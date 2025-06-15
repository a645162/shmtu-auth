from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMenuBar


class MenuAction(QAction):

    def __init__(self, text="", parent=None):
        super().__init__(text, parent)


class SystemMenu:
    def __init__(self):
        self.menu_bar = QMenuBar(parent=None)

        self.__init_macos_program_menu()

        self.__init_children()

    def __init_macos_program_menu(self):
        import platform

        def is_macos():
            return platform.system().lower() == "darwin"

        # Check is macOS
        if not is_macos():
            return

        print("macOS detected.")
        print("Try to init macOS program menu.")

    def __init_children(self):
        # File Menu
        self.file_menu = self.menu_bar.addMenu("File")

        self.file_menu_open_dir = MenuAction("Open Directory", self.file_menu)
        self.file_menu.addAction(self.file_menu_open_dir)

        # Help Menu
        self.help_menu = self.menu_bar.addMenu("Help")

        self.help_menu_about = MenuAction("About", self.help_menu)
        self.help_menu_about.setMenuRole(QAction.MenuRole.AboutRole)
        self.help_menu.addAction(self.help_menu_about)


system_menu = None


def init_system_menu() -> SystemMenu:
    global system_menu
    if system_menu is None:
        system_menu = SystemMenu()
    return system_menu
