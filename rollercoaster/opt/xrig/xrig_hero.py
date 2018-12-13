# -*- coding: utf-8 -*-

from .base import XRigBase


class XRigContext(XRigBase):
    CONTEXT_NAME = 'hero'

    CTRL_TAG = ['_ac_', '_sc_']

    WEIGHT_CENTER_CTRL_TAG = ['_ac_cn_upperbody']

    LT_CTRL_TAG = ['_lf_']
    LT_CTRL_FORMAT = ['*_lf_*']

    MD_CTRL_TAG = ['_cn_']
    MD_CTRL_FORMAT = ['*_cn_*']

    RT_CTRL_TAG = ['_rt_']
    RT_CTRL_FORMAT = ['*_rt_*']

    IK_CTRL_TAG = ['IK']
    FK_CTRL_TAG = ['FK']

    POLE_CTRL_TAG = ['Pole']
    POLE_CTRL_FORMAT = ['*_ac_*Pole']

    IK_FLIP_ATTR = ['translateX']
    MD_FLIP_ATTR = ['translateX', 'rotateY', 'rotateZ']
    FACE_FLIP_ATTR = ['translateX']

    MIRROR_MATRIX = [
        -1, 0, 0, 0,
         0, 1, 0, 0,
         0, 0, 1, 0,
         0, 0, 0, 1
    ]

    def is_ctrl(self, name):
        state = False
        for tag in self.CTRL_TAG:
            if tag in name:
                state = True
                break
        return state
