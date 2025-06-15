# -*- coding: utf-8 -*-

import datetime

from PySide6.QtCore import QDate
from qfluentwidgets import ZhDatePicker


# Convert datetime.date to QDate
def convert_date_to_qdate(date: datetime.date) -> QDate:
    return QDate(date.year, date.month, date.day)


# Convert QDate to datetime.date
def convert_qdate_to_date(qdate: QDate) -> datetime.date:
    return datetime.date(qdate.year(), qdate.month(), qdate.day())


class FDatePicker(ZhDatePicker):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.set_date_today()

    def set_date_today(self):
        date_today = datetime.date.today()
        qdate_today = convert_date_to_qdate(date_today)
        self.setDate(qdate_today)
