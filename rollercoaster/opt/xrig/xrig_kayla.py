# -*- coding: utf-8 -*-

from .base import XRigBase


class XRigKayla(XRigBase):
    CONTEXT_NAME = 'kayla'
    CTRL_TAG = ['_CON']

    LT_CTRL_TAG = ['L_']
    LT_CTRL_FORMAT = ['L_*']

    MD_CTRL_TAG = ['M_']
    MD_CTRL_FORMAT = ['M_*']

    RT_CTRL_TAG = ['R_']
    RT_CTRL_FORMAT = ['R_*']

    IK_CTRL_TAG = ['_ik']
    FK_CTRL_TAG = ['_fk']

    IK_FLIP_ATTR = []
    MD_FLIP_ATTR = []
    FACE_FLIP_ATTR = []
