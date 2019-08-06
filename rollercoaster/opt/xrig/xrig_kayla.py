# -*- coding: utf-8 -*-

from .base import XRigBase


class XRigContext(XRigBase):
    CONTEXT_NAME = 'kayla'

    CTRL_TAG = ['_CON']

    WEIGHT_CENTER_CTRL_TAG = ['_ac_cn_upperbody']

    LT_CTRL_TAG = ['L_']
    LT_CTRL_FORMAT = ['L_*']

    MD_CTRL_TAG = ['M_']
    MD_CTRL_FORMAT = ['M_*']

    RT_CTRL_TAG = ['R_']
    RT_CTRL_FORMAT = ['R_*']

    IK_CTRL_TAG = ['_ik']
    FK_CTRL_TAG = ['_fk']

    POLE_CTRL_TAG = ['Pole']
    POLE_CTRL_FORMAT = ['*_ac_*Pole']

    IK_FLIP_ATTR = []
    MD_FLIP_ATTR = []
    FACE_FLIP_ATTR = []
