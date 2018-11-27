# -*- coding: utf-8 -*-


from QtSide import QtWidgets, ui_wrapper
import maya.OpenMayaUI as OpenMayaUI


connector = ui_wrapper.wrapinstance(
    long(OpenMayaUI.MQtUtil.mainWindow()),
    QtWidgets.QMainWindow
)
