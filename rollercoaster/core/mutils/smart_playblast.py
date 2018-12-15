# -*- coding: utf-8 -*-

import traceback
import pymel.core as pm
from . import smart_panel
from . import smart_hud


class SmartPlayblast(object):

    _TYPE = '.mov'

    def __init__(self):
        panels = list(
            set(pm.windows.getPanel(type='modelPanel')).intersection(set(pm.windows.getPanel(visiblePanels=True)))
        )
        self.smart_panel = smart_panel.SmartPanel(panels)
        self.smart_hud = smart_hud.SmartHud()

    def playblast(self, panel_edit=True, hud_edit=True, path='', camera='', quality=100,
                  res=None, sf=0, ef=0, type='qt', compress='png', audio='', **kwargs):

        if res is None:
            res = [960, 540]

        objects = pm.general.selected()
        pm.general.select(cl=True)

        try:
            pm.animation.playbackOptions(edit=True, by=1.0)
        except Exception as e:
            print e
            traceback.print_exc()

        if panel_edit is True:
            self.smart_panel.record()
            self.smart_panel.player()
        if hud_edit is True:
            self.smart_hud.record()
            self.smart_hud.clean()
        if camera:
            try:
                pm.rendering.lookThru(camera)
            except Exception as e:
                print e
                traceback.print_exc()

        if type == 'qt':
            try:
                pm.animation.playblast(
                    format=type, f=path, fo=True, sqt=False, cc=True, v=True, orn=True, os=True, fp=1,
                    p=100, compression=compress, qlt=quality, wh=res, st=sf, et=ef, sound=audio, **kwargs
                )
                if panel_edit is True:
                    self.smart_panel.recovery()
                pm.general.select(objects, r=True)
                return path + self._TYPE
            except Exception as e:
                print e
                if panel_edit is True:
                    self.smart_panel.recovery()
                if hud_edit is True:
                    self.smart_hud.recovery()
                pm.general.select(objects, r=True)
                pm.system.displayError("Can't overwrite, File opened?")
                traceback.print_exc()
                return None
        elif type == 'image':
            try:
                pm.animation.playblast(
                    format=type, f=path, fo=True, sqt=False, cc=True, v=False, orn=True, os=True,
                    fp=1, p=100, compression=compress, qlt=quality, wh=res, st=sf, et=ef, **kwargs
                )
                if panel_edit is True:
                    self.smart_panel.recovery()
                pm.general.select(objects, r=True)
            except Exception as e:
                print e
                if panel_edit is True:
                    self.smart_panel.recovery()
                if hud_edit is True:
                    self.smart_hud.recovery()
                pm.general.select(objects, r=True)
                pm.system.displayError("Can't overwrite, File opened?")
                traceback.print_exc()
                return None
        else:
            return None
