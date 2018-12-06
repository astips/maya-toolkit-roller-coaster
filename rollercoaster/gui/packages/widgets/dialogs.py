# -*- coding: utf-8 -*-

import fnmatch
from QtSide import QtGui, QtWidgets
from ..utils import to_utf8


__all__ = [
    'LimitInputDialog'
]


class LimitInputDialog(QtWidgets.QInputDialog):
    def __init__(self, parent=None, title=None, label=None, width=100, height=50):
        super(LimitInputDialog, self).__init__(parent)
        self.setInputMode(QtWidgets.QInputDialog.TextInput)
        self.setWindowTitle(title)
        self.setLabelText(label)
        self.resize(width, height)
        self.__connect()

    def __connect(self):
        self.textValueChanged.connect(self.__check)

    def __check(self):
        text = to_utf8(self.textValue())
        if text:
            if not fnmatch.fnmatch(text[-1], '[a-zA-z0-9_]'):
                self.setTextValue(text[0:-1])
