# -*- coding: utf-8 -*-

import maya.cmds as cmds


class UndoManager(object):

    def on(self):
        cmds.undoInfo(state=True)

    def off(self):
        cmds.undoInfo(state=False)

    @property
    def infinity(self):
        return cmds.undoInfo(q=True, infinity=True)

    @infinity.setter
    def infinity(self, value):
        cmds.undoInfo(state=True, infinity=value)

    def set_length(self, length):
        cmds.undoInfo(state=True, infinity=False, l=length)

    def open_chunk(self):
        cmds.undoInfo(ock=True)

    def close_chunk(self):
        cmds.undoInfo(cck=True)

    def state(self):
        return cmds.undoInfo(q=True, st=True)

    def flush_on(self):
        cmds.undoInfo(swf=True)

    def flush_off(self):
        cmds.undoInfo(swf=False)

    def undo(self):
        cmds.undo()
