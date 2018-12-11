# -*- coding: utf-8 -*-

from .base import XRigBase


class XRigContext(XRigBase):
    CONTEXT_NAME = 'basic'

    CTRL_TAG = ['_ctrl']
    LT_CTRL_FORMAT = ['L_*']
    RT_CTRL_FORMAT = ['R_*']
    MD_CTRL_FORMAT = ['M_*']

    MIRROR_MATRIX = [
        -1, 0, 0, 0,
         0, 1, 0, 0,
         0, 0, 1, 0,
         0, 0, 0, 1
    ]
