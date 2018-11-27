# -*- coding: utf-8 -*-


import fnmatch


class XRigBase(object):

    CONTEXT_NAME = 'base'

    CTRL_TAG = []

    LT_CTRL_TAG = []
    LT_CTRL_FORMAT = []

    MD_CTRL_TAG = []
    MD_CTRL_FORMAT = []

    RT_CTRL_TAG = []
    RT_CTRL_FORMAT = []

    IK_CTRL_TAG = []
    FK_CTRL_TAG = []

    IK_FLIP_ATTR = []
    MD_FLIP_ATTR = []
    FACE_FLIP_ATTR = []

    TRANSLATE_ATTR = ['translateX', 'translateY', 'translateZ']
    ROTATE_ATTR = ['rotateX', 'rotateY', 'rotateZ']

    def is_ctrl(self, name):
        state = False
        for tag in self.CTRL_TAG:
            if name.endswith(tag):
                state = True
                break
        return state

    def is_lt_ctrl(self, name):
        state = False
        for fmt in self.LT_CTRL_FORMAT:
            if fnmatch.fnmatch(name, fmt):
                state = True
                break
        return state

    def is_md_ctrl(self, name):
        state = False
        for fmt in self.MD_CTRL_FORMAT:
            if fnmatch.fnmatch(name, fmt):
                state = True
                break
        return state

    def is_rt_ctrl(self, name):
        state = False
        for fmt in self.RT_CTRL_FORMAT:
            if fnmatch.fnmatch(name, fmt):
                state = True
                break
        return state

    def is_ik_ctrl(self, name):
        state = False
        for tag in self.IK_CTRL_TAG:
            if tag in name:
                state = True
                break
        return state

    def is_fk_ctrl(self, name):
        state = False
        for tag in self.FK_CTRL_TAG:
            if tag in name:
                state = True
                break
        return state

    def lt_to_rt(self, name):
        for i in xrange(len(self.LT_CTRL_TAG)):
            name = name.replace(self.LT_CTRL_TAG[i], self.RT_CTRL_TAG[i])
        return name

    def rt_to_lt(self, name):
        for i in xrange(len(self.LT_CTRL_TAG)):
            name = name.replace(self.RT_CTRL_TAG[i], self.LT_CTRL_TAG[i])
        return name

    def is_translate_attr(self, attr):
        if attr in self.TRANSLATE_ATTR:
            return True
        return False

    def is_rotate_attr(self, attr):
        if attr in self.ROTATE_ATTR:
            return True
        return False

    def switch(self, name):
        if self.is_lt_ctrl(name):
            name = self.lt_to_rt(name)
            return name
        elif self.is_rt_ctrl(name):
            name = self.rt_to_lt(name)
            return name
        else:
            return name

    def is_ik_flip_attr(self, attr):
        if attr in self.IK_FLIP_ATTR:
            return True
        return False

    def is_md_flip_attr(self, attr):
        if attr in self.MD_FLIP_ATTR:
            return True
        return False

    def is_facial_flip_attr(self, attr):
        if attr in self.FACE_FLIP_ATTR:
            return True
        return False
