# -*- coding: utf-8 -*-

from QtSide import QtWidgets, QtCore


class ProgressButton(QtWidgets.QProgressBar):
    clicked = QtCore.pyqtSignal()

    def __init__(self, parent=None, fc=None, bc=None):
        super(ProgressButton, self).__init__(parent)
        self.fc = fc
        self.bc = bc
        self.setup_ui()
        self.__connect()

    def setup_ui(self):
        self.setTextVisible(False)
        self.button = QtWidgets.QPushButton(self)
        self.button.setStyleSheet(
            "background-color: rgb({}, {}, {}, {});".format(self.bc[0], self.bc[1], self.bc[2], self.bc[3])
        )

    def __connect(self):
        self.button.clicked.connect(self.clicked.emit)

    def resizeEvent(self, event):
        event.accept()
        self.button.setGeometry(0, 0, self.width(), self.height())
