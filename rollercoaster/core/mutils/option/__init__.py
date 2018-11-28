# -*- coding: utf-8 -*-

from .xrig import xrig_basic
from .filter import filter_basic


def xrig_context(context=None):
    """
    get the context class from a context name string.
    """
    context = str(context).lower()
    if context == 'basic':
        return xrig_basic.XRigContext()
    else:
        raise Exception('Invalid XRig Context.')


def xrig_filter(context=None):
    """
    get the filter function from a context name string.
    """
    if context == 'basic':
        return filter_basic._filter
    else:
        raise Exception('Invalid XRig Context.')
