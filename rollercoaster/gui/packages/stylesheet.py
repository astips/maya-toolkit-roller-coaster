# -*- coding: utf-8 -*-

import os
import re


class StyleSheet(object):
    """
    Usage:
        >> options = {'ICON_PATH': '/QQQ/OOO/UUU'}
        >> style = StyleSheet.from_path('style.css', options=options, dpi=1)
        >> ui.setStyleSheet(style.data())
    """
    def __init__(self):
        self._data = ''

    @classmethod
    def from_path(cls, path, **kwargs):
        """
        type path: str
        rtype: str
        """
        style_sheet = cls()
        data = style_sheet.read(path)
        data = StyleSheet.format(data, **kwargs)
        style_sheet.set_data(data)
        return style_sheet

    @classmethod
    def from_text(cls, text, options=None):
        """
        type text: str
        rtype: str
        """
        style_sheet = cls()
        data = StyleSheet.format(text, options=options)
        style_sheet.set_data(data)
        return style_sheet

    def set_data(self, data):
        """
        type data: str
        """
        self._data = data

    def data(self):
        """
        rtype: str
        """
        return self._data

    @staticmethod
    def read(path):
        """
        type path: str
        rtype: str
        """
        data = ''
        if os.path.isfile(path):
            with open(path, 'r') as f:
                data = f.read()
        return data

    @staticmethod
    def format(data=None, options=None, dpi=1):
        """
        type data:
        type options: dict
        rtype: str
        """
        if options is not None:
            keys = options.keys()
            keys.sort(key=len, reverse=True)
            for key in keys:
                data = data.replace(key, options[key])

        re_dpi = re.compile('[0-9]+[*]DPI')
        new_data = []
        for line in data.split('\n'):
            dpi_ = re_dpi.search(line)
            if dpi_:
                new = dpi_.group().replace('DPI', str(dpi))
                val = int(eval(new))
                line = line.replace(dpi_.group(), str(val))
            new_data.append(line)

        data = '\n'.join(new_data)
        return data
