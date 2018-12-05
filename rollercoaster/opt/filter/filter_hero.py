# -*- coding: utf-8 -*-

from .base import FilterBase


class FilterContext(FilterBase):
    CONTEXT_NAME = 'hero'

    def build(self):
        self.append(267)  # OpenMaya.MFn().kNurbsCurve
