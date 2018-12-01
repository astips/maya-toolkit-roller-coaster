# -*- coding: utf-8 -*-

import maya.OpenMaya as OpenMaya
from .base import FilterBase


class FilterContext(FilterBase):
    CONTEXT_NAME = 'kayla'

    def filler(self):
        self.int_array.append(OpenMaya.MFn().kNurbsCurve)
