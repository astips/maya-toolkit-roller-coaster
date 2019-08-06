# -*- coding: utf-8 -*-

import pymel.core as pm


MODELPANEL = 'modelPanel4'


def get_all_cameras():
    return pm.rendering.listCameras(p=True, o=True)


def get_current_camera(panel=None):
    if panel is None:
        panel = MODELPANEL
    return pm.windows.modelPanel(panel, q=True, cam=True)
