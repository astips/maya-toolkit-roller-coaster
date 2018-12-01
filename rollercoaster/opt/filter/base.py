# -*- coding: utf-8 -*-

import maya.OpenMaya as OpenMaya


class FilterBase(object):
    CONTEXT_NAME = 'base'

    def __init__(self):
        self.int_array = OpenMaya.MIntArray()
        self.iterator_type = OpenMaya.MIteratorType()
        self.filler()

    def filler(self):
        self.int_array.append(OpenMaya.MFn().kNurbsCurve)
        self.int_array.append(OpenMaya.MFn().kCamera)
        self.int_array.append(OpenMaya.MFn().kStereoCameraMaster)
        # self.int_array.append(OpenMaya.MFn().kPluginCameraSet)
        # self.int_array.append(OpenMaya.MFn().kCameraSet)
        # self.int_array.append(OpenMaya.MFn().kMesh)

    def filters(self):
        self.iterator_type.setFilterList(self.int_array)
        return self.iterator_type


TEMPLATE = """
# -*- coding: utf-8 -*-

from .base import FilterBase


class FilterContext(FilterBase):
    CONTEXT_NAME = {CONTEXT_NAME}'
    def filler(self):
        {APPEND_LOOP}
"""