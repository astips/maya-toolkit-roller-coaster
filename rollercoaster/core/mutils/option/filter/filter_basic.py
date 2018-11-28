# -*- coding: utf-8 -*-

import maya.OpenMaya as OpenMaya


def _filter():
    int_array = OpenMaya.MIntArray()
    int_array.append(OpenMaya.MFn().kNurbsCurve)
    int_array.append(OpenMaya.MFn().kCamera)
    int_array.append(OpenMaya.MFn().kStereoCameraMaster)
    # int_array.append(OpenMaya.MFn().kPluginCameraSet)
    # int_array.append(OpenMaya.MFn().kCameraSet)
    # int_array.append(OpenMaya.MFn().kMesh)
    iterator_type = OpenMaya.MIteratorType()
    iterator_type.setFilterList(int_array)
    return iterator_type
