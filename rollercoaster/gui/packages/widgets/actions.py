# -*- coding: utf-8 -*-

from QtSide import QtWidgets, QtGui, QtCore


__all__ = ['CheckBoxAction', 'RadioAction', 'SliderAction']


class CheckBoxAction(QtWidgets.QWidgetAction):
    def __init__(self, parent=None, text=''):
        """
        type parent: QtGui.QMenu
        """
        QtWidgets.QWidgetAction.__init__(self, parent)
        self._frame = QtWidgets.QFrame(parent)
        self._checkbox = QtWidgets.QCheckBox(text)

    def frame(self):
        return self._frame

    def checkbox(self):
        return self._checkbox

    def createWidget(self, parent=None):
        """
        type parent: QtGui.QMenu
        """
        action_widget = self.frame()
        action_layout = QtWidgets.QHBoxLayout(action_widget)
        action_layout.setSpacing(0)
        action_layout.setContentsMargins(1, 4, 0, 0)
        action_layout.addWidget(self.checkbox())
        action_widget.setLayout(action_layout)
        return action_widget


class RadioAction(QtWidgets.QWidgetAction):

    _toggled = QtCore.pyqtSignal(str)

    def __init__(self, parent=None, labels=None):
        """
        type parent: QtGui.QMenu
        """

        QtWidgets.QWidgetAction.__init__(self, parent)

        self.labels = labels
        self._frame = QtWidgets.QFrame(parent)

        self.radio_buttons = []

    def frame(self):
        return self._frame

    def radios(self):
        return self.radio_buttons

    def checked(self):
        for radio_button in self.radio_buttons:
            if radio_button.isChecked():
                self._toggled.emit(str(radio_button.text()).lower())
                break

    def createWidget(self, parent=None):
        """
        type parent: QtGui.QMenu
        """
        action_widget = self.frame()
        action_layout = QtWidgets.QVBoxLayout(action_widget)
        action_layout.setSpacing(5)

        action_layout.setContentsMargins(2, 4, 0, 0)

        for label in self.labels:
            radio_button = QtWidgets.QRadioButton(label)
            radio_button.setMouseTracking(0)
            self.radio_buttons.append(radio_button)
            action_layout.addWidget(radio_button)
            radio_button.clicked.connect(self.checked)

        self.radio_buttons[0].setChecked(True)
        action_widget.setLayout(action_layout)
        return action_widget


class SliderAction(QtWidgets.QWidgetAction):

    def __init__(self, label='', parent=None, pixmap=None):
        """
        type parent: QtWidgets.QMenu
        """
        QtWidgets.QWidgetAction.__init__(self, parent)
        self._frame = QtWidgets.QFrame(parent)
        self._label = QtWidgets.QLabel(label, self._frame)
        self._label.setMinimumWidth(0)
        self._label.setPixmap(pixmap)

        self._slider = QtWidgets.QSlider(QtCore.Qt.Horizontal, self._frame)
        self.valueChanged = self._slider.valueChanged

    def frame(self):
        return self._frame

    def label(self):
        return self._label

    def slider(self):
        return self._slider

    def createWidget(self, parent=None):
        """
        type parent: QtWidgets.QMenu
        """
        action_widget = self.frame()
        action_layout = QtWidgets.QHBoxLayout(action_widget)
        action_layout.setSpacing(0)
        action_layout.setContentsMargins(1, 4, 0, 0)
        action_layout.addWidget(self.label())
        action_layout.addWidget(self.slider())
        action_widget.setLayout(action_layout)
        return action_widget
