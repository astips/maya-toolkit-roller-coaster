# -*- coding: utf-8 -*-

from .base import XRigBase


class XRigContext(XRigBase):
    CONTEXT_NAME = 'basic'

    CTRL_TAG = ['_ctrl']
    LT_CTRL_FORMAT = ['L_*']  # TODO will delete
    RT_CTRL_FORMAT = ['R_*']  # TODO will delete
    MD_CTRL_FORMAT = ['M_*']  # TODO will delete
