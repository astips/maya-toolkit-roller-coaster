# -*- coding: utf-8 -*-

import os
import maya.OpenMaya as OpenMaya


location = os.path.dirname(__file__)


class FilterBase(object):
    CONTEXT_NAME = 'base'

    def __init__(self):
        self.int_array = OpenMaya.MIntArray()
        self.iterator_type = OpenMaya.MIteratorType()
        self.build()

    def append(self, num):
        self.int_array.append(num)

    def build(self):
        self.append(267)  # OpenMaya.MFn().kNurbsCurve
        self.append(250)  # OpenMaya.MFn().kCamera
        self.append(1041)  # OpenMaya.MFn().kStereoCameraMaster
        # self.append(1004)  # OpenMaya.MFn().kCameraSet
        # self.append(296)  # OpenMaya.MFn().kMesh

    def filters(self):
        self.iterator_type.setFilterList(self.int_array)
        return self.iterator_type


TEMPLATE = """
# -*- coding: utf-8 -*-

from .base import FilterBase


class FilterContext(FilterBase):
    CONTEXT_NAME = '{CONTEXT_NAME}'
    
    def filler(self):
        {APPEND_LOOP}
"""