# -*- coding: utf-8 -*-

import traceback
import pymel.core as pm
from . import smart_panel
from . import smart_hud


QUEUER_DIR_NAME = 'queue'


class SmartPlayblast(object):

    _TYPE = '.mov'

    def __init__(self):
        panels = list(
            set(pm.windows.getPanel(type='modelPanel')).intersection(set(pm.windows.getPanel(visiblePanels=True)))
        )
        self.smart_panel = smart_panel.SmartPanel(panels)
        self.smart_hud = smart_hud.SmartHud()

    def playblast(self, panel_edit=True, hud_edit=True, path='', camera='', quality=100,
                  res=None, sf=0, ef=0, type='qt', compress='png', audio='', **kargs):

        if res is None:
            res = [960, 540]

        objs = pm.general.selected()
        pm.general.select(cl=True)

        try:
            pm.animation.playbackOptions(edit=True, by=1.0)
        except:
            traceback.print_exc()
            pass

        if panel_edit is True:
            self.smart_panel.record()
            self.smart_panel.player()
        if hud_edit is True:
            self.smart_hud.record()
            self.smart_hud.clean()
        if camera:
            try:
                pm.rendering.lookThru(camera)
            except:
                traceback.print_exc()

        if type == 'qt':
            try:
                pm.animation.playblast(
                    format=type, f=path, fo=True, sqt=False, cc=True, v=True, orn=True, os=True, fp=1,
                    p=100, compression=compress, qlt=quality, wh=res, st=sf, et=ef, sound=audio, **kargs
                )
                if panel_edit is True:
                    self.smart_panel.reback()
                pm.general.select(objs, r=True)
                return path + self._TYPE
            except:
                if panel_edit is True:
                    self.smart_panel.reback()
                if hud_edit is True:
                    self.smart_hud.recovery()
                pm.general.select(objs, r=True)
                pm.system.displayError('Can not be overwrite, Opened by player ?')
                traceback.print_exc()
                return None
        elif type == 'image':
            try:
                pm.animation.playblast(
                    format=type, f=path, fo=True, sqt=False, cc=True, v=False, orn=True, os=True, fp=1,
                    p=100, compression=compress, qlt=quality, wh=res, st=sf, et=ef, sound=audio, **kargs
                )
                if panel_edit is True:
                    self.smart_panel.reback()
                pm.general.select(objs, r=True)
            except:
                if panel_edit is True:
                    self.smart_panel.reback()
                if hud_edit is True:
                    self.smart_hud.recovery()
                pm.general.select(objs, r=True)
                pm.system.displayError('Can not be overwrite, Opened by player ?')
                traceback.print_exc()
                return None
        else:
            return None
