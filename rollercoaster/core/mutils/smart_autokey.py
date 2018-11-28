# -*- coding: utf-8 -*-

import maya.cmds as cmds


class AutoKeyManager(object):
    def __init__(self):
        self.cache = None

    def on(self):
        cmds.autoKeyframe(state=True)

    def off(self):
        cmds.autoKeyframe(state=False)

    def state(self):
        self.cache = cmds.autoKeyframe(q=True, state=True)
        return self.cache

    def back(self):
        cmds.autoKeyframe(state=self.cache)

    def setkey(self, key=False):
        if key:
            objs = cmds.ls(sl=True)
            if not len(objs):
                return
            cmds.setKeyframe()
