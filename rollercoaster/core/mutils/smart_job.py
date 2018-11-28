# -*- coding: utf-8 -*-

import maya.cmds as cmds


class ScriptJob(object):
    """
    USAGE :
        script_job = ScriptJob(e=['SelectionChanged', self.selectionChanged])
    """
    def __init__(self, *args, **kwargs):
        self.id = cmds.scriptJob(*args, **kwargs)

    def kill(self):
        if self.id:
            cmds.scriptJob(kill=self.id, force=True)
            self.id = None

    def __enter__(self):
        return self

    def __exit__(self, t, v, tb):
        if t is not None:
            self.kill()
