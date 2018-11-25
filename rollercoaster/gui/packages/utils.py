# -*- coding: utf-8 -*-

import re


def to_utf8(text):
    if text.__class__.__name__ == 'QString':
        text = str(text.toUtf8())
        text = text.decode('utf-8')
    elif text.__class__.__name__ == 'str':
        text = text.decode('utf-8')
    return text


def natural_sort(items):
    convert = lambda text: (int(text) if text.isdigit() else text)
    _key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    items.sort(key=_key)
