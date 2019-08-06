# -*- coding: utf-8 -*-

from .base import FilterBase


class FilterContext(FilterBase):
    CONTEXT_NAME = 'basic'

    def build(self):
        self.append(267)  # OpenMaya.MFn().kNurbsCurve
        self.append(250)  # OpenMaya.MFn().kCamera
        self.append(1041)  # OpenMaya.MFn().kStereoCameraMaster
