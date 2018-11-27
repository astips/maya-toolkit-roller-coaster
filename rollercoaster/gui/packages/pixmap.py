# -*- coding: utf-8 -*-

from QtSide import QtGui
from .color import Color


class Pixmap(QtGui.QPixmap):
    def __init__(self, *args):
        QtGui.QPixmap.__init__(self, *args)
        self._color = None

    def set_color(self, color):
        if isinstance(color, basestring):
            color = Color.from_string(color)

        if not self.isNull():
            painter = QtGui.QPainter(self)
            painter.setCompositionMode(QtGui.QPainter.CompositionMode_SourceIn)
            painter.setBrush(color)
            painter.setPen(color)
            painter.drawRect(self.rect())
            painter.end()
