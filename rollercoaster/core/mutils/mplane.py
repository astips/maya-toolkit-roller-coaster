# -*- coding: utf-8 -*-

import maya.cmds as cmds
import maya.OpenMaya as OpenMaya


PLUGIN_NAME = 'mirrorPlane'


def magicMirror(src=None, dst=None, plane=None, active=False, space='world', context=None):
    """
    src      - source ctrl name
    dst      - destination ctrl name
    plane    - mirror plane name
    active   - bool
    space    - world / object
    context  - xrig context
    """
    srcPath = name2Path(src)
    srcMatrix = srcPath.inclusiveMatrix()
    srcTransformationMatrix = OpenMaya.MTransformationMatrix(srcMatrix)

    planePath = name2Path(plane)
    planeMatrix = planePath.inclusiveMatrix()
    planeMatrixInverse = planeMatrix.inverse()

    dstPath = name2Path(dst)
    dstMatrix = dstPath.inclusiveMatrix()
    dstTransformationMatrix = OpenMaya.MTransformationMatrix(dstMatrix)
    dstParentMatrix = dstPath.exclusiveMatrix()
    dstParentMatrixInverse = dstParentMatrix.inverse()
    dstParentTMatrixInverse = OpenMaya.MTransformationMatrix(dstParentMatrixInverse)
    dstParentInverseQuaternion = dstParentTMatrixInverse.rotation()

    # get default value for undo
    dstTransform = OpenMaya.MFnTransform(dstPath)
    dstOldTranslation = dstTransform.getTranslation(OpenMaya.MSpace.kWorld)
    dstOldRotationQuaternion = OpenMaya.MQuaternion()
    dstTransform.getRotation(dstOldRotationQuaternion, OpenMaya.MSpace.kWorld)

    helpAMatrix = OpenMaya.MMatrix()
    OpenMaya.MScriptUtil.createMatrixFromList(
        [
            -1, 0, 0, 0,
             0, 1, 0, 0,
             0, 0, 1, 0,
             0, 0, 0, 1
        ],
        helpAMatrix
    )

    helpBMatrix = OpenMaya.MMatrix()
    if context == 'creative':
        OpenMaya.MScriptUtil.createMatrixFromList([-1,  0,  0, 0,
                                                    0, -1,  0, 0,
                                                    0,  0, -1, 0,
                                                    0,  0,  0, 1], helpBMatrix)

    elif context == 'rlo':
        OpenMaya.MScriptUtil.createMatrixFromList([-1, 0, 0, 0,
                                                    0, 1, 0, 0,
                                                    0, 0, 1, 0,
                                                    0, 0, 0, 1], helpBMatrix)

    elif context == 'biped system':
        OpenMaya.MScriptUtil.createMatrixFromList([-1, 0, 0, 0,
                                                    0, 1, 0, 0,
                                                    0, 0, 1, 0,
                                                    0, 0, 0, 1], helpBMatrix)

    elif context == 'base':
        OpenMaya.MScriptUtil.createMatrixFromList([-1, 0, 0, 0,
                                                    0, 1, 0, 0,
                                                    0, 0, 1, 0,
                                                    0, 0, 0, 1], helpBMatrix)

    elif context == 'malcolm':
        OpenMaya.MScriptUtil.createMatrixFromList([-1, 0, 0, 0,
                                                    0, 1, 0, 0,
                                                    0, 0, 1, 0,
                                                    0, 0, 0, 1], helpBMatrix)

    else:
        raise Exception('Invalid context !')

    aimMatrix = srcMatrix * planeMatrixInverse * helpAMatrix * planeMatrix
    aimMatrix = helpBMatrix * aimMatrix

    # temp locator
    modifier = OpenMaya.MDagModifier()
    tempLoc = modifier.createNode('locator')
    modifier.doIt()
    tempLocDagFn = OpenMaya.MFnDagNode(tempLoc)
    tempLocDagPath = OpenMaya.MDagPath()
    tempLocDagFn.getPath(tempLocDagPath)

    tempTransformationMatrix = OpenMaya.MTransformationMatrix(aimMatrix)
    tempTransform = OpenMaya.MFnTransform(tempLocDagPath)
    tempTransform.set(tempTransformationMatrix)

    # world space
    aimTranslation = tempTransform.getTranslation(OpenMaya.MSpace.kWorld)
    aimRotationQuaternion = OpenMaya.MQuaternion()
    tempTransform.getRotation(aimRotationQuaternion, OpenMaya.MSpace.kWorld)

    # object space
    aimTranslationPoint = OpenMaya.MPoint(aimTranslation)
    aimTranslates = aimTranslationPoint * dstParentMatrixInverse
    aimRotatesQuaternion = aimRotationQuaternion * dstParentInverseQuaternion
    aimRotatesEuler = aimRotatesQuaternion.asEulerRotation()
    
    # print aimTranslates.x, aimTranslates.y, aimTranslates.z
    # print math.degrees(aimRotatesEuler.x), math.degrees(aimRotatesEuler.y), math.degrees(aimRotatesEuler.z)

    modifier.undoIt()

    dstTransform = OpenMaya.MFnTransform(dstPath)
    if active is True:
        if space == 'world':
            dstTransform.setTranslation(aimTranslation, OpenMaya.MSpace.kWorld)
            dstTransform.setRotation(aimRotationQuaternion, OpenMaya.MSpace.kWorld)
        elif space == 'object':
            dstTransform.setTranslation(OpenMaya.MVector(aimTranslates), OpenMaya.MSpace.kTransform)
            dstTransform.setRotation(aimRotatesQuaternion, OpenMaya.MSpace.kTransform)
    else:
        if space == 'world':
            return dstTransform, aimTranslation, aimRotationQuaternion, dstOldTranslation, dstOldRotationQuaternion
        elif space == 'object':
            return dstTransform, OpenMaya.MVector(aimTranslates), aimRotatesQuaternion

        # return {
        #         'translateX': aimTranslates[0], 
        #         'translateY': aimTranslates[1], 
        #         'translateZ': aimTranslates[2], 
        #         'rotateX': aimRotatesEuler[0], 
        #         'rotateY': aimRotatesEuler[1], 
        #         'rotateZ': aimRotatesEuler[2], 
        #         }


def _loadPlugin():
    try:
        cmds.loadPlugin(PLUGIN_NAME, quiet=True)
        return True
    except:
        import traceback
        print traceback.format_exc()
        return False


def getMirrorPlane(namespace):
    _loadPlugin()
    if len(namespace):
        planes = cmds.ls('{0}*'.format(namespace), type='mirrorPlane', l=True) or []
        if not len(planes):
            OpenMaya.MGlobal.displayWarning('No mirror plane for this asset, just ignore.')
            return None
        elif len(planes) > 1:
            OpenMaya.MGlobal.displayInfo(planes) 
            OpenMaya.MGlobal.displayWarning('More than one mirror plane for this asset, return first one.')
            return planes[0]
        return planes[0]
    else:
        selectionList = OpenMaya.MSelectionList()
        OpenMaya.MGlobal.getActiveSelectionList(selectionList)
        objPath = OpenMaya.MDagPath()
        selectionList.getDagPath(0, objPath)
        root = '|{0}'.format(objPath.fullPathName().split('|')[1])
        planes = cmds.listRelatives(root, ad=True, type='mirrorPlane', f=True) or []
        if not len(planes):
            OpenMaya.MGlobal.displayWarning('No mirror plane for this asset, just ignore.')
            return None
        elif len(planes) > 1:
            OpenMaya.MGlobal.displayInfo(planes) 
            OpenMaya.MGlobal.displayWarning('More than one mirror plane for this asset, return first one.')
            return planes[0]
        return planes[0]


def name2Object(name):
    obj = OpenMaya.MObject()
    tempList = OpenMaya.MSelectionList()
    tempList.add(name)
    tempList.getDependNode(0, obj)
    return obj


def name2Path(name):
    path = OpenMaya.MDagPath()
    tempList = OpenMaya.MSelectionList()
    tempList.add(name)
    tempList.getDagPath(0, path)
    return path
