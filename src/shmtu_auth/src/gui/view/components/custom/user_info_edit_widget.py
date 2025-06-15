# -*- coding: utf-8 -*-

from typing import List

from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

from qfluentwidgets import (
    PushButton,
    LineEdit,
    PasswordLineEdit,
    ZhDatePicker,
    TeachingTip,
    TeachingTipTailPosition,
    InfoBarIcon,
)

from shmtu_auth.src.datatype.shmtu.auth.auth_user import (
    UserItem,
    NetworkType,
    user_is_exist_in_list,
)
from shmtu_auth.src.gui.view.components.custom.list_checkbox_widget import (
    ListCheckboxWidgets,
)

from shmtu_auth.src.gui.view.components.fluent.widget_push_button import FPushButton
from shmtu_auth.src.gui.view.components.fluent.widget_date_picker import (
    FDatePicker,
    convert_date_to_qdate,
    convert_qdate_to_date,
)


class UserInfoEditWidget(QWidget):
    # Signal Slot
    # Send
    onModifyButtonClick = Signal()
    # Receive
    onSelectedItemChanged = Signal()

    layout: QVBoxLayout

    input_user_id: LineEdit
    input_user_name: LineEdit
    input_password: PasswordLineEdit

    checkbox_support_type: ListCheckboxWidgets

    widget_expire_date: ZhDatePicker

    button_save: PushButton

    # Data
    user_list: List[UserItem]
    selected_index: List[int]

    def __init__(
        self,
        parent=None,
        user_list: List[UserItem] = None,
        selected_index: List[int] = None,
    ):
        super().__init__(parent)

        self.user_list = user_list
        self.selected_index = selected_index

        self.setFixedWidth(250)

        self.__init_widget()
        self.__init_layout()

    def __init_widget(self):
        self.input_user_id = LineEdit(self)
        self.input_user_id.setText("")
        self.input_user_id.setPlaceholderText("请输入学号")
        self.input_user_id.setClearButtonEnabled(True)
        # 只允许数字
        self.input_user_id.setInputMask("0" * 12)
        self.input_user_id.setMaxLength(12)

        self.input_user_name = LineEdit(self)
        self.input_user_name.setText("")
        self.input_user_name.setPlaceholderText("请输入姓名")
        self.input_user_name.setClearButtonEnabled(True)

        self.input_password = PasswordLineEdit(self)
        self.input_password.setFixedWidth(230)
        self.input_password.setPlaceholderText("请输入密码")

        self.checkbox_support_type = ListCheckboxWidgets(
            self,
            [
                {"name": "校园网", "default": True},
                {"name": "iSMU", "default": False, "enable": False},
            ],
        )

        self.widget_expire_date = FDatePicker(self)

        self.button_save = FPushButton(self, "保存修改")
        self.button_save.clicked.connect(self.__button_save_clicked)

        # 连接接收的信号槽
        self.onSelectedItemChanged.connect(self.__selection_changed)
        self.__selection_changed()

    def __init_layout(self):

        class TitleLabelLevel1(QLabel):
            def __init__(self, text: str, parent=None):
                super().__init__(parent)
                self.setText(text)
                self.setStyleSheet(
                    """
                    QLabel {
                        font-size: 14px;
                        color: #333333;
                    }
                """
                )

        class TitleLabelLevel2(QLabel):
            def __init__(self, text: str, parent=None):
                super().__init__(parent)
                self.setText(text)
                self.setStyleSheet(
                    """
                    QLabel {
                        font-size: 12px;
                        color: #333333;
                    }
                """
                )

        self.layout = QVBoxLayout(self)

        # Separator
        self.layout.addWidget(TitleLabelLevel1("用户信息编辑"))

        self.layout.addWidget(TitleLabelLevel2(""))

        self.layout.addWidget(TitleLabelLevel1("学号"))
        self.layout.addWidget(self.input_user_id)
        self.layout.addWidget(TitleLabelLevel1("姓名"))
        self.layout.addWidget(self.input_user_name)
        self.layout.addWidget(TitleLabelLevel1("密码"))
        self.layout.addWidget(self.input_password)

        self.layout.addWidget(TitleLabelLevel1("支持的服务类型"))
        self.layout.addWidget(self.checkbox_support_type)

        self.layout.addWidget(TitleLabelLevel1("毕业(过期)时间"))
        self.layout.addWidget(self.widget_expire_date)

        self.layout.addWidget(self.button_save)

        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout.setContentsMargins(2, 0, 0, 0)

        self.setLayout(self.layout)

    def __selection_changed(self):
        selection_count = len(self.selected_index)

        self.setEnabled(selection_count == 1)

        if selection_count == 0:
            return

        index = self.selected_index[0]
        self.__update_input_box_data(index=index)

    def __before_save_blocker(self) -> bool:
        self.input_user_id.setText(self.input_user_id.text().strip())
        self.input_user_name.setText(self.input_user_name.text().strip())
        self.input_password.setText(self.input_password.text().strip())

        if (
            not self.input_user_id.text().isdigit()
            or len(self.input_user_id.text()) != 12
        ):
            TeachingTip.create(
                target=self.input_user_id,
                icon=InfoBarIcon.ERROR,
                title="错误",
                content="学号应该为12位！",
                isClosable=True,
                tailPosition=TeachingTipTailPosition.BOTTOM,
                duration=-1,
                parent=self,
            )
            return False

        if user_is_exist_in_list(
            user_list=self.user_list,
            user_id=self.input_user_id.text(),
            excluded_indexes=self.selected_index,
        ):
            TeachingTip.create(
                target=self.input_user_id,
                icon=InfoBarIcon.ERROR,
                title="错误",
                content="与该学号相同的用户已存在！",
                isClosable=True,
                tailPosition=TeachingTipTailPosition.BOTTOM,
                duration=-1,
                parent=self,
            )
            return False

        if len(self.input_password.text()) == 0:
            TeachingTip.create(
                target=self.input_password,
                icon=InfoBarIcon.ERROR,
                title="错误",
                content="密码不能为空！",
                isClosable=True,
                tailPosition=TeachingTipTailPosition.BOTTOM,
                duration=-1,
                parent=self,
            )
            return False

        return True

    def __button_save_clicked(self):
        # 先经过拦截器进行数据校验
        if not self.__before_save_blocker():
            return

        # 修改数据
        self.__modify_user_data(index=self.selected_index[0])

        TeachingTip.create(
            target=self.button_save,
            icon=InfoBarIcon.SUCCESS,
            title="成功",
            content="保存成功！",
            isClosable=True,
            tailPosition=TeachingTipTailPosition.BOTTOM,
            duration=3000,
            parent=self,
        )

        # 发送信号
        self.onModifyButtonClick.emit()

    def __modify_user_data(self, index: int = 0):
        if index >= len(self.user_list):
            return

        current_item: UserItem = self.user_list[index]

        current_item.user_id = self.input_user_id.text()
        current_item.user_name = self.input_user_name.text()
        current_item.password = self.input_password.text()

        current_item.support_type_list = NetworkType.to_binary_list_by_name_list(
            self.checkbox_support_type.get_selected_list()
        )

        current_item.expire_date = convert_qdate_to_date(
            self.widget_expire_date.getDate()
        )
        current_item.update_auto_generate_info()

    def __update_input_box_data(self, index: int = 0):
        if index >= len(self.user_list):
            return

        current_item: UserItem = self.user_list[index]

        self.input_user_id.setText(current_item.user_id)
        self.input_user_name.setText(current_item.user_name)
        self.input_password.setText(current_item.password)

        self.checkbox_support_type.set_selected_list(current_item.support_type_str_list)

        q_date = convert_date_to_qdate(current_item.expire_date)
        self.widget_expire_date.setDate(q_date)
