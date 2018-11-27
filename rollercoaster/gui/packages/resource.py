# -*- coding: utf-8 -*-

import os
from QtSide import QtGui
from .pixmap import Pixmap


class Resource(object):
    def __init__(self, head, *args):
        self._dirname = head
        if self._dirname is None:
            self._dirname = os.path.join(os.path.dirname(__file__), 'resource', 'icon')
        self._dirname = os.path.join(self._dirname, *args)
        if os.path.isfile(self._dirname):
            self._dirname = os.path.dirname(self._dirname)

    def dirname(self):
        return self._dirname

    def get(self, *args):
        return os.path.join(self.dirname(), *args)

    def pixmap(self, name, ext='png', color=None):
        path = self.get('{0}.{1}'.format(name, ext))
        p = Pixmap(path)
        if color:
            p.set_color(color)
        return p

    def icon(self, name, ext='png', color=None):
        p = self.pixmap(name, ext=ext, color=color)
        return QtGui.QIcon(p)
