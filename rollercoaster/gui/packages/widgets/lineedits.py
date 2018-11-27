# -*- coding: utf-8 -*-

from QtSide import QtCore, QtGui, QtWidgets


__all__ = [
    'IconLineEdit',
    'LabelLineEdit',
    'LockerLineEdit'
]


class IconLineEdit(QtWidgets.QLineEdit):
    def __init__(self, parent=None, icon=None):
        super(IconLineEdit, self).__init__(parent)
        self.__style(icon)

    def __style(self, icon):
        reg_exp = QtCore.QRegExp('[a-zA-Z0-9_]+')
        validator = QtGui.QRegExpValidator(reg_exp, self)
        self.setValidator(validator)
        # self.icon_btn = QtWidgets.QPushButton(self)
        # self.icon_btn.setFixedSize(25, 25)
        # self.icon_btn.setIconSize(QtCore.QSize(20, 20))
        # self.icon_btn.setFocusPolicy(QtCore.Qt.NoFocus)
        # self.icon_btn.setFlat(True)
        # self.icon_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        # self.icon_btn.setEnabled(False)
        # self.icon_btn.setIcon(icon)
        # self.icon_btn.setStyleSheet("QPushButton{background:transparent;}")

        self.label_icon = QtWidgets.QLabel(self)
        self.label_icon.setFixedSize(25, 25)
        self.label_icon.setFocusPolicy(QtCore.Qt.NoFocus)
        self.label_icon.setStyleSheet("background:transparent;")
        self.label_icon.setPixmap(icon.pixmap(20, 20))
        self.label_icon.setEnabled(False)

        self.main_layout = QtWidgets.QHBoxLayout(self)
        self.main_layout.addWidget(self.label_icon)
        self.main_layout.addStretch()
        self.main_layout.setContentsMargins(2, 0, 0, 0)

        self.setFocusPolicy(QtCore.Qt.TabFocus | QtCore.Qt.ClickFocus)
        self.setFrame(False)
        self.setTextMargins(24, 0, 0, 0)
        self.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.main_layout)

        self.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum))
        self.setMinimumSize(QtCore.QSize(30, 30))


class LockerLineEdit(QtWidgets.QLineEdit):
    def __init__(self, parent=None, icon=None, unlock_icon=None, lock_icon=None):
        super(LockerLineEdit, self).__init__(parent)
        self.icon = icon
        self.lock_icon = lock_icon
        self.unlock_icon = unlock_icon
        self.is_locked = False
        self.__style()
        self.lock_btn.clicked.connect(self.toggle_lock)

    def __style(self):
        reg_exp = QtCore.QRegExp('[a-zA-Z0-9_]+')
        validator = QtGui.QRegExpValidator(reg_exp, self)
        self.setValidator(validator)
        self.setFocusPolicy(QtCore.Qt.TabFocus | QtCore.Qt.ClickFocus)
        self.setFrame(False)
        self.setTextMargins(24, 0, 0, 0)
        self.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet("color: rgb(200, 200, 200, 255)")

        # self.icon_btn = QtWidgets.QPushButton(self)
        # self.icon_btn.setFixedSize(25, 25)
        # self.icon_btn.setIconSize(QtCore.QSize(20, 20))
        # self.icon_btn.setFocusPolicy(QtCore.Qt.NoFocus)
        # self.icon_btn.setFlat(True)
        # self.icon_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        # self.icon_btn.setEnabled(False)
        # self.icon_btn.setIcon(self.icon)
        # self.icon_btn.setStyleSheet("QPushButton{background:transparent;}")

        self.label_icon = QtWidgets.QLabel(self)
        self.label_icon.setFixedSize(25, 25)
        self.label_icon.setFocusPolicy(QtCore.Qt.NoFocus)
        self.label_icon.setStyleSheet("background:transparent;")
        self.label_icon.setPixmap(self.icon.pixmap(20, 20))
        self.label_icon.setEnabled(False)

        self.lock_btn = QtWidgets.QPushButton(self)
        self.lock_btn.setFixedSize(15, 28)
        self.lock_btn.setIconSize(QtCore.QSize(15, 15))
        self.lock_btn.setFocusPolicy(QtCore.Qt.NoFocus)
        self.lock_btn.setFlat(False)
        self.lock_btn.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.lock_btn.setEnabled(True)
        self.lock_btn.setIcon(self.unlock_icon)
        self.lock_btn.setStyleSheet(
            "QPushButton{background-color: rgb(25, 25, 25, 75);}"
            "QPushButton:hover{background-color: rgb(0, 0, 0, 0);}"
        )

        self.main_layout = QtWidgets.QHBoxLayout()
        self.main_layout.addWidget(self.label_icon)
        self.main_layout.addItem(
            QtWidgets.QSpacerItem(10000, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        )
        self.main_layout.addWidget(self.lock_btn)
        self.main_layout.addStretch()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.main_layout)
        self.setMinimumSize(QtCore.QSize(30, 30))
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.setSizePolicy(size_policy)

    def toggle_lock(self):
        if self.is_locked:
            self.setReadOnly(False)
            self.setFocusPolicy(QtCore.Qt.TabFocus | QtCore.Qt.ClickFocus)
            self.setStyleSheet("color: rgb(200, 200, 200, 255)")
            self.lock_btn.setIcon(self.unlock_icon)
            self.is_locked = False
        else:
            self.setReadOnly(True)
            self.setSelection(0, 0)
            self.setCursorPosition(0)
            self.setFocusPolicy(QtCore.Qt.NoFocus)
            self.setStyleSheet("color: rgb(100, 100, 100, 255)")
            self.lock_btn.setIcon(self.lock_icon)
            self.is_locked = True


class LabelLineEdit(QtWidgets.QLineEdit):
    def __init__(self, parent=None, text=None, color=None):
        super(LabelLineEdit, self).__init__(parent)

        if color is None:
            color = (200, 200, 200, 255)
        self.color = color
        self.__style(text)

    def __style(self, text):
        reg_exp = QtCore.QRegExp('[a-zA-Z0-9_]+')
        validator = QtGui.QRegExpValidator(reg_exp, self)
        self.setValidator(validator)
        font = QtGui.QFont()
        font.setBold(True)
        font.setPointSize(15)
        self.setFont(font)

        self.text_label = QtWidgets.QLabel(self)
        self.text_label.setFocusPolicy(QtCore.Qt.NoFocus)
        self.text_label.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.text_label.setFont(font)
        self.text_label.setText(text)
        self.text_label.setStyleSheet("color: rgb{0}".format(self.color))
        self.text_label.setEnabled(False)

        self.main_layout = QtWidgets.QHBoxLayout()
        self.main_layout.addWidget(self.text_label)
        self.main_layout.addStretch()
        self.main_layout.setContentsMargins(4, 0, 0, 0)

        self.setFocusPolicy(QtCore.Qt.TabFocus | QtCore.Qt.ClickFocus | QtCore.Qt.StrongFocus)
        self.setFrame(False)
        self.setTextMargins(self.get_text_width()+12, 0, 0, 0)
        self.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.main_layout)

        self.setMinimumSize(QtCore.QSize(30, 30))

    def text_rect(self):
        text = self.text_label.text()
        font = self.font()
        metrics = QtGui.QFontMetricsF(font)
        return metrics.boundingRect(text)

    def get_text_width(self):
        text_width = self.text_rect().width()
        return max(0, text_width)

    def get_text_height(self):
        text_height = self.text_rect().height()
        return max(0, text_height)
