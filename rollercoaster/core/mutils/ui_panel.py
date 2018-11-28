# -*- coding: utf-8 -*-

import string
import random
import pymel.core as pm
import maya.OpenMayaUI as OpenMayaUI
from QtSide import QtCore, QtWidgets, ui_wrapper


MODELPANEL = 'modelPanel4'


class IndividualModelPanel(object):
    def __init__(self):
        self.panel = None

    def set_name(self, length):
        return ''.join(random.choice(string.ascii_letters) for i in xrange(length))

    def create(self, parent):
        layout = OpenMayaUI.MQtUtil.fullName(long(ui_wrapper.unwrapinstance(parent)))
        pm.setParent(layout)
        self.panel = pm.windows.modelPanel(
            self.set_name(20), label='IndividualModelPanel', parent=layout
        )
        self.set_model_panel_options()
        self.hide_bar_layout()
        self.hide_menu_bar()
        camera = self.get_camera()
        self.set_camera(self.panel, camera)

    def qwidget(self):
        ptr = OpenMayaUI.MQtUtil.findControl(self.panel)
        return ui_wrapper.wrapinstance(long(ptr), QtWidgets.QWidget)

    def setFixedSize(self, w, h):
        qtwidget = self.qwidget()
        qtwidget.setFixedSize(w, h)

    def get_current_panel(self):
        current_panel = pm.windows.getPanel(withFocus=True)
        if not current_panel:
            return None
        _type = pm.windows.getPanel(typeOf=current_panel)
        if _type not in ('modelPanel',):
            return None
        return current_panel

    def set_model_panel_options(self, panel=None):
        if panel is None:
            panel = self.panel
        pm.windows.modelEditor(panel, edit=True, allObjects=False)
        pm.windows.modelEditor(panel, edit=True, dynamics=False)
        pm.windows.modelEditor(panel, edit=True, activeOnly=False)
        pm.windows.modelEditor(panel, edit=True, headsUpDisplay=False)
        pm.windows.modelEditor(panel, edit=True, polymeshes=True)
        pm.windows.modelEditor(panel, edit=True, nurbsSurfaces=True)
        pm.windows.modelEditor(panel, edit=True, subdivSurfaces=True)
        pm.windows.modelEditor(panel, edit=True, displayTextures=True)
        pm.windows.modelEditor(panel, edit=True, displayAppearance='smoothShaded')
        # pm.windows.modelEditor(panel, edit=True, grid=False)
        # pm.windows.modelEditor(panel, edit=True, manipulators=False)
        # pm.windows.modelEditor(panel, edit=True, selectionHiliteDisplay=False)
        current_panel = self.get_current_panel()
        if current_panel:
            camera = pm.windows.modelEditor(current_panel, query=True, camera=True)
            display_lights = pm.windows.modelEditor(current_panel, query=True, displayLights=True)
            display_textures = pm.windows.modelEditor(current_panel, query=True, displayTextures=True)
            pm.windows.modelEditor(panel, edit=True, camera=camera)
            pm.windows.modelEditor(panel, edit=True, displayLights=display_lights)
            pm.windows.modelEditor(panel, edit=True, displayTextures=display_textures)

    def bar_layout(self, panel):
        name = pm.windows.modelPanel(panel, query=True, barLayout=True)
        ptr = OpenMayaUI.MQtUtil.findControl(name)
        return ui_wrapper.wrapinstance(long(ptr), QtCore.QObject)

    def hide_bar_layout(self, panel=None):
        if panel is None:
            panel = self.panel
        self.bar_layout(panel).hide()

    def hide_menu_bar(self, panel=None):
        if panel is None:
            panel = self.panel
        pm.windows.modelPanel(panel, edit=True, menuBarVisible=False)

    def set_camera(self, panel=None, camera=None):
        if panel is None:
            panel = self.panel
        panel.setCamera(camera)

    def get_camera(self, panel=None, select=False):
        if panel is None:
            panel = MODELPANEL
        camera = pm.windows.modelPanel(panel, q=True, camera=True)
        if select:
            pm.general.select(camera, r=True)
        return camera

    def delete_panel(self, panel=None):
        if panel is None:
            panel = self.panel
        try:
            pm.windows.deleteUI(panel, panel=True)
        except:
            pass

    def toggle_grid(self, panel=None):
        if panel is None:
            panel = self.panel
        if pm.windows.modelEditor(panel, q=True, grid=True):
            pm.windows.modelEditor(panel, edit=True, grid=False)
        else:
            pm.windows.modelEditor(panel, edit=True, grid=True)

    def toggle_texture(self, panel=None):
        if panel is None:
            panel = self.panel
        if pm.windows.modelEditor(panel, query=True, displayTextures=True):
            pm.windows.modelEditor(panel, edit=True, displayTextures=False)
        else:
            pm.windows.modelEditor(panel, edit=True, displayTextures=True)
