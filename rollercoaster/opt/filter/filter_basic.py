# -*- coding: utf-8 -*-

import maya.OpenMaya as OpenMaya
from .base import FilterBase


class FilterContext(FilterBase):

    def filler(self):
        self.int_array.append(OpenMaya.MFn().kNurbsCurve)
        self.int_array.append(OpenMaya.MFn().kCamera)
        self.int_array.append(OpenMaya.MFn().kStereoCameraMaster)
