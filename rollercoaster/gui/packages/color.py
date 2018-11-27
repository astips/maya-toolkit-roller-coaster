# -*- coding: utf-8 -*-

from QtSide import QtGui


class Color(QtGui.QColor):
    @classmethod
    def from_color(cls, color):
        color = 'rgb(%d, %d, %d, %d)' % color.getRgb()
        return cls.from_string(color)

    @classmethod
    def from_string(cls, text):
        a = 255
        try:
            r, g, b, a = text.replace('rgb(', '').replace(')', '').split(',')
        except ValueError:
            r, g, b = text.replace('rgb(', '').replace(')', '').split(',')

        return cls(int(r), int(g), int(b), int(a))

    def __eq__(self, other):
        if other == self:
            return True
        elif isinstance(other, Color):
            return self.to_string() == other.to_string()
        else:
            return False

    def to_string(self):
        return 'rgb(%d, %d, %d, %d)' % self.getRgb()

    def is_dark(self):
        return self.red() < 125 and self.green() < 125 and self.blue() < 125
