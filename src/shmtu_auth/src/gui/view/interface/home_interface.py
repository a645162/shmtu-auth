# -*- coding: utf-8 -*-

from PySide6.QtCore import Qt, QRectF, QSize
from PySide6.QtGui import (
    QPixmap,
    QPainter,
    QColor,
    QBrush,
    QPainterPath,
    QLinearGradient,
)
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

from qfluentwidgets import (
    ScrollArea,
    isDarkTheme,
    FluentIcon,
    SettingCardGroup,
    SettingCard,
)

from shmtu_auth.src.gui.common.components.link_card import LinkCardView
from shmtu_auth.src.gui.common.components.sample_card import SampleCardView
from shmtu_auth.src.gui.common.signal_bus import signal_bus

from shmtu_auth.src.gui.common.style_sheet import StyleSheet
from shmtu_auth.src.gui.common import font_confg
from shmtu_auth.src.gui.common.config import (
    FEEDBACK_URL,
    HELP_URL,
    REPO_URL,
    AUTHOR_MAIN_PAGE_URL,
)

from shmtu_auth.src.utils.logs import get_logger

logger = get_logger()


class BannerWidget(QWidget):
    """Banner widget"""

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setFixedHeight(336)

        self.vBoxLayout = QVBoxLayout(self)

        self.galleryLabel = QLabel("ShangHai Maritime University", self)
        self.galleryLabel.setFont(font_confg.title_font)
        self.galleryLabel.setObjectName("galleryLabel")

        self.banner: QPixmap = QPixmap(":/shmtu/banner1")
        self.linkCardView = LinkCardView(self)

        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.setContentsMargins(0, 20, 0, 0)
        self.vBoxLayout.addWidget(self.galleryLabel)
        self.vBoxLayout.addWidget(self.linkCardView, 1, Qt.AlignBottom)

        margin_widget = QWidget(self)
        margin_widget.setFixedHeight(20)
        self.vBoxLayout.addWidget(margin_widget)

        self.vBoxLayout.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        self.linkCardView.addCard(
            ":/gui/Logo128", "快速入门", "查看本程序的在线文档。", HELP_URL
        )

        self.linkCardView.addCard(
            FluentIcon.GITHUB, "Github主页", "查看本程序的源代码。", REPO_URL
        )

        self.linkCardView.addCard(
            FluentIcon.HOME_FILL,
            "孔昊旻的主页",
            "查看作者的其他项目",
            AUTHOR_MAIN_PAGE_URL,
        )

        self.linkCardView.addCard(
            FluentIcon.FEEDBACK,
            "问题反馈",
            "反馈问题或建议(需要Github账户)。",
            FEEDBACK_URL,
        )

    def paintEvent(self, e):
        super().paintEvent(e)

        painter = QPainter(self)
        painter.setRenderHints(QPainter.SmoothPixmapTransform | QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)

        path = QPainterPath()
        path.setFillRule(Qt.WindingFill)
        w, h = self.width(), self.height()
        path.addRoundedRect(QRectF(0, 0, w, h), 10, 10)
        path.addRect(QRectF(0, h - 50, 50, 50))
        path.addRect(QRectF(w - 50, 0, 50, 50))
        path.addRect(QRectF(w - 50, h - 50, 50, 50))
        path = path.simplified()

        # 绘图逻辑
        # pixmap = self.banner.scaled(
        #     self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        # painter.fillPath(path, QBrush(pixmap))

        # painter.drawPixmap(self.rect(), pixmap)

        width_origin = self.banner.width()
        height_origin = self.banner.height()
        wh_ratio = width_origin / height_origin

        width_target = self.width()
        height_target = self.height()

        height_new = height_target
        width_new = height_new * wh_ratio
        if width_new < width_target:
            width_new = width_target
            height_new = width_new / wh_ratio

        scaled_pixmap = self.banner.scaled(
            QSize(width_new, height_new),
            Qt.AspectRatioMode.IgnoreAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )

        # 计算裁剪坐标(水平全部，垂直是中心部分)
        crop_x = 0
        crop_y = (height_new - height_target) / 2
        crop_width = width_target
        crop_height = height_target

        # 裁剪图片
        croped_pixmap = scaled_pixmap.copy(
            int(crop_x), int(crop_y), int(crop_width), int(crop_height)
        )

        # print(width_target, height_target)
        # print(croped_pixmap.width(), croped_pixmap.height())
        # print()

        # 在路径内部绘制缩放并裁剪后的图像
        painter.drawPixmap(
            path.boundingRect(),
            croped_pixmap,
            QRectF(0, 0, width_target, height_target),
        )

        # init linear gradient effect
        gradient = QLinearGradient(0, 0, 0, h)

        # draw background color
        if not isDarkTheme():
            gradient.setColorAt(0, QColor(207, 216, 228, 255))
            gradient.setColorAt(1, QColor(207, 216, 228, 0))
        else:
            gradient.setColorAt(0, QColor(0, 0, 0, 255))
            gradient.setColorAt(1, QColor(0, 0, 0, 0))

        painter.fillPath(path, QBrush(gradient))


class QuickStatusCard(SettingCardGroup):
    """主页快速状态概览卡片"""

    def __init__(self, parent=None):
        super().__init__("系统状态概览", parent)

        # 网络状态卡
        self.network_card = SettingCard(FluentIcon.WIFI, "网络状态", "检查中...")
        self.addSettingCard(self.network_card)

        # 服务状态卡
        self.service_card = SettingCard(FluentIcon.POWER_BUTTON, "认证服务", "未启动")
        self.addSettingCard(self.service_card)

        # 连接信号
        signal_bus.signal_auth_status_changed.connect(self.update_network_status)
        signal_bus.signal_auth_thread_started.connect(
            lambda: self.service_card.setContent("运行中 ✓")
        )
        signal_bus.signal_auth_thread_stopped.connect(
            lambda: self.service_card.setContent("已停止 ✗")
        )

    def update_network_status(self, is_online: bool):
        """更新网络状态"""
        if is_online:
            self.network_card.setContent("已连接 ✓")
        else:
            self.network_card.setContent("需要认证 ⚠")


class HomeInterface(ScrollArea):
    """Home interface"""

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.banner = BannerWidget(self)
        self.view = QWidget(self)
        self.vBoxLayout = QVBoxLayout(self.view)

        self.__initWidget()
        self.load_card_content()

    def __initWidget(self):
        self.view.setObjectName("view")
        self.setObjectName("homeInterface")
        StyleSheet.HOME_INTERFACE.apply(self)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidget(self.view)
        self.setWidgetResizable(True)

        self.vBoxLayout.setContentsMargins(0, 0, 0, 36)
        self.vBoxLayout.setSpacing(40)
        self.vBoxLayout.addWidget(self.banner)
        self.vBoxLayout.setAlignment(Qt.AlignTop)

    def load_card_content(self):
        # 状态概览卡片 - 添加左右边距
        from PySide6.QtWidgets import QHBoxLayout

        status_container = QWidget(self.view)
        status_layout = QHBoxLayout(status_container)
        status_layout.setContentsMargins(20, 0, 20, 0)  # 左右各20px边距

        self.status_card = QuickStatusCard(self.view)
        status_layout.addWidget(self.status_card)

        self.vBoxLayout.addWidget(status_container)

        current_application_view_group = SampleCardView("本程序功能", self.view)
        current_application_view_group.addSampleCard(
            icon=":/gui/Logo128",
            title="校园网自动认证",
            content="监控网络状况，自动认证校园网，\n" "避免因各种因素导致断网。",
            index=26,
            url="https://a645162.github.io/shmtu-auth/"
            "1.Guide/0.Quick%20Start/1.Quick%20Start.html",
        )
        self.vBoxLayout.addWidget(current_application_view_group)

        # 为上海海事大学开发的项目
        shmtu_project_view_group = SampleCardView(
            "数字海大系列(非官方,个人学习使用)", self.view
        )
        shmtu_project_view_group.addSampleCard(
            icon=":/project/logo_terminal",
            title="用户终端(非官方)",
            content="数字海大的用户终端(第三方)\n" "主要包括账单获取、账单分析等功能。",
            index=3,
            url="https://github.com/a645162/SHMTU-Terminal-Wails",
        )
        shmtu_project_view_group.addSampleCard(
            icon=":/project/logo_shmtu",
            title="验证码识别服务器(C++)",
            content="自动识别统一认证平台的验证码。",
            index=4,
            url="https://github.com/a645162/shmtu-cas-ocr-server",
        )
        shmtu_project_view_group.addSampleCard(
            icon=":/project/logo_golang",
            title="登录流程(Golang)",
            content="统一认证平台的登录流程\n" "包括调用识别验证码接口。",
            index=5,
            url="https://github.com/a645162/shmtu-cas-go",
        )
        shmtu_project_view_group.addSampleCard(
            icon=":/project/logo_kotlin",
            title="登录流程(Kotlin)",
            content="统一认证平台的登录流程\n" "包括调用识别验证码接口。",
            index=5,
            url="https://github.com/a645162/shmtu-cas-kotlin",
        )
        self.vBoxLayout.addWidget(shmtu_project_view_group)

        # 为课题组开发的项目
        group_project_view_group = SampleCardView("为课题组开发的项目", self.view)
        group_project_view_group.addSampleCard(
            icon=":/project/logo_gpu_dashboard",
            title="GPU任务通知工具",
            content="我与师兄合作开发的一款GPU任务监控工具，\n"
            "GPU训练任务结束自动推送消息。",
            index=4,
            url="https://github.com/a645162/nvi-notify",
        )
        group_project_view_group.addSampleCard(
            icon=":/project/logo_gpu_dashboard",
            title="GPU看板",
            content="GPU任务面板基于"
            "Vue3 + Element Plus + Pinia"
            "开发，"
            "后端为显卡监控脚本的Flask。",
            index=4,
            url="https://github.com/a645162/nvi-notify",
        )
        self.vBoxLayout.addWidget(group_project_view_group)
