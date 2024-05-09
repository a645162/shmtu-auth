from PySide6.QtCore import QUrl
from PySide6.QtGui import QDesktopServices
from qfluentwidgets import MessageBox

from ..common.config import cfg, RELEASE_URL
from ..software import program_update


def program_auto_check_update(parent, dialog=False) -> bool:
    if not program_update.is_have_new_version():
        if dialog:
            w = MessageBox(
                "检查新版本",
                "您正在使用最新版本。",
                parent
            )
            w.setContentCopyable(True)
        return False

    current_version = program_update.PROGRAM_VERSION
    new_version = program_update.LATEST_VERSION

    title = "检测到新版本"
    content = (
        f"当前版本: {current_version}\n"
        f"最新版本: {new_version}\n"
        f"您是否需要前往官网下载?"
    )

    w = MessageBox(title, content, parent)
    w.setContentCopyable(True)
    if w.exec():
        QDesktopServices.openUrl(QUrl(RELEASE_URL))

    return True
