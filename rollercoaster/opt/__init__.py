# -*- coding: utf-8 -*-

import importlib


def xrig_context(context=None):
    """
    get the context class from a context name string.
    """
    context = str(context).lower()
    try:
        _xrig_module = importlib.import_module('rollercoaster.opt.xrig.xrig_{0}'.format(context))
        reload(_xrig_module)
        return _xrig_module.XRigContext()
    except Exception as e:
        raise e


def filter_context(context=None):
    """
    get the filter function from a context name string.
    """
    try:
        _filter_module = importlib.import_module('rollercoaster.opt.filter.filter_{0}'.format(context))
        reload(_filter_module)
        return _filter_module.FilterContext().filters()
    except Exception as e:
        print('{0}\nUse basic filter instead...'.format(e))
        _filter_module = importlib.import_module('rollercoaster.opt.filter.filter_basic')
        reload(_filter_module)
        return _filter_module.FilterContext().filters()
