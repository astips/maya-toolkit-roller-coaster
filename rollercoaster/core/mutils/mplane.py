# -*- coding: utf-8 -*-


# import math
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
    if context == 'whd creative':
        OpenMaya.MScriptUtil.createMatrixFromList([-1,  0,  0, 0,
                                                    0, -1,  0, 0,
                                                    0,  0, -1, 0,
                                                    0,  0,  0, 1], helpBMatrix)

    elif context == 'whd rlo':
        OpenMaya.MScriptUtil.createMatrixFromList([-1, 0, 0, 0,
                                                    0, 1, 0, 0,
                                                    0, 0, 1, 0,
                                                    0, 0, 0, 1], helpBMatrix)

    elif context == 'whd biped system':
        OpenMaya.MScriptUtil.createMatrixFromList([-1, 0, 0, 0,
                                                    0, 1, 0, 0,
                                                    0, 0, 1, 0,
                                                    0, 0, 0, 1], helpBMatrix)

    elif context == 'cwt':
        OpenMaya.MScriptUtil.createMatrixFromList([-1, 0, 0, 0,
                                                    0, 1, 0, 0,
                                                    0, 0, 1, 0,
                                                    0, 0, 0, 1], helpBMatrix)

    elif context == 'as malcolm':
        OpenMaya.MScriptUtil.createMatrixFromList([-1, 0, 0, 0,
                                                    0, 1, 0, 0,
                                                    0, 0, 1, 0,
                                                    0, 0, 0, 1], helpBMatrix)

    else:
        raise Exception('Wrong context !')

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


'''
def magic_mirror(src=None, dst=None, plane=None, axis='x', unify=None) :
    """
    src   :   source object name
    dst   :   destination object name
    plane :   mirror plane name
    axis  :   mirror axis
    unify :   conform direction between src & dst
    """

    if unify == None :
        unify = OpenMaya.MVector(1, 1, 1)
    else :
        unify = OpenMaya.MVector(unify[0], unify[1], unify[2])

    # -- deal with translate -- #
    srcPath = name2Path(src)
    srcMatrix = srcPath.inclusiveMatrix()

    planePath = name2Path(plane)
    planeMatrix = planePath.inclusiveMatrix()
    planeNormal = OpenMaya.MVector(1.0, 0.0, 0.0) * planeMatrix

    srcPosition = OpenMaya.MVector(srcMatrix(3, 0), srcMatrix(3, 1), srcMatrix(3, 2))
    planePosition = OpenMaya.MVector(planeMatrix(3, 0), planeMatrix(3, 1), planeMatrix(3, 2))

    dstPath = name2Path(dst)
    dstTransform = OpenMaya.MFnTransform(dstPath)
    dstParentMatrix = dstPath.exclusiveMatrix()
    dstParentMatrixInverse = dstParentMatrix.inverse()

    d = - (planeNormal.x * planePosition.x + planeNormal.y * planePosition.y + planeNormal.z * planePosition.z)
    k = - (planeNormal.x * srcPosition.x + planeNormal.y * srcPosition.y + planeNormal.z * srcPosition.z + d) / \
          (planeNormal.x**2 + planeNormal.y**2 + planeNormal.z**2)

    px = k * planeNormal.x * 2 + srcPosition.x
    py = k * planeNormal.y * 2 + srcPosition.y
    pz = k * planeNormal.z * 2 + srcPosition.z
    p = OpenMaya.MPoint(px, py, pz)

    dstObjectPosition = p * dstParentMatrixInverse

    # dstTransform.setTranslation(OpenMaya.MVector(dstObjectPosition), 1)
    dstTransform.setTranslation(OpenMaya.MVector(p), 4)

    # return {
    #         'translateX': dstObjectPosition[0], 
    #         'translateY': dstObjectPosition[1], 
    #         'translateZ': dstObjectPosition[2]
    #         }
    try :
        cmds.setAttr('{}.tx'.format(dst), dstObjectPosition[0])
        cmds.setAttr('{}.ty'.format(dst), dstObjectPosition[1])
        cmds.setAttr('{}.tz'.format(dst), dstObjectPosition[2])
    except :
        pass

    # -- deal with rotate -- #
    srcRotateOffset = OpenMaya.MVector(0.0, 0.0, 0.0)
    srcRotateOffsetEuler = OpenMaya.MEulerRotation(srcRotateOffset, OpenMaya.MEulerRotation.kXYZ)
    srcRotateOffsetQuater = srcRotateOffsetEuler.asQuaternion()


    srcRotate = cmds.xform(src, q=True, ro=True, ws=True)
    srcRotateVector = OpenMaya.MVector(srcRotate[0], srcRotate[1], srcRotate[2])
    srcRotateEuler = OpenMaya.MEulerRotation(srcRotateVector, OpenMaya.MEulerRotation.kXYZ)
    srcRotateQuater = srcRotateEuler.asQuaternion()


    planeRotate = cmds.xform(plane, q=True, ro=True, ws=True)
    planeRotateVector = OpenMaya.MVector(planeRotate[0], planeRotate[1], planeRotate[2])
    planeRotateEuler = OpenMaya.MEulerRotation(planeRotateVector, OpenMaya.MEulerRotation.kXYZ)
    planeRotateQuater = planeRotateEuler.asQuaternion()

    # r_ws = planeRotateQuater + unify * (srcRotateQuater - planeRotateQuater - srcRotateOffsetQuater)
    x = planeRotateVector.x + unify[0] * (srcRotateVector.x - planeRotateVector.x - srcRotateOffset.x)
    y = planeRotateVector.y + unify[1] * (srcRotateVector.y - planeRotateVector.y - srcRotateOffset.y)
    z = planeRotateVector.z + unify[2] * (srcRotateVector.z - planeRotateVector.z - srcRotateOffset.z)
    
    # print rx_ws, ry_ws, rz_ws


    # euler ==> quaternion
    qx = math.sin(y/2) * math.sin(z/2) * math.cos(x/2) + math.cos(y/2) * math.cos(z/2) * math.sin(x/2)
    qy = math.sin(y/2) * math.cos(z/2) * math.cos(x/2) + math.cos(y/2) * math.sin(z/2) * math.sin(x/2)
    qz = math.cos(y/2) * math.sin(z/2) * math.cos(x/2) - math.sin(y/2) * math.cos(z/2) * math.sin(x/2)
    qw = math.cos(y/2) * math.cos(z/2) * math.cos(x/2) - math.sin(y/2) * math.sin(z/2) * math.sin(x/2)

    q = OpenMaya.MQuaternion(qx, qy, qz, qw)

    # print r_ws.x, r_ws.y, r_ws.z
    # dstWsRotateVector = OpenMaya.MVector(rx_ws, ry_ws, rz_ws)
    # euler = OpenMaya.MEulerRotation(dstWsRotateVector, OpenMaya.MEulerRotation.kXYZ)
    # quater = euler.asQuaternion()
    # dstTransform.setRotation(r_ws, 4)

    # dst = pm.general.PyNode(dst)
    # nr = pm.dt.EulerRotation([rx_ws, ry_ws, rz_ws]) 
    dst.setRotation(q, "world")


# mirror('ARM_R_handIk_CTRL', 'ARM_L_handIk_CTRL', 'mirrorLoc_rotate', unify=[1, -1, 1])
'''



"""
for sdsdsd in pm.selected() :
    if not sdsdsd.endswith('_CTRL') :
        continue
        

    if '_L_' in sdsdsd.name() :
        qq = mirror(sdsdsd, sdsdsd.replace('_L_', '_R_'), 'mirrorLoc_rotate')
        print qq
    
    if '_R_' in sdsdsd.name() :
        print sdsdsd
        print sdsdsd.replace('_R_', '_L_')
        tt = mirror(sdsdsd, sdsdsd.replace('_R_', '_L_'), 'mirrorLoc_rotate')
        print tt
    
"""


"""
source = pm.general.PyNode("ARM_R_handIk_CTRL")
source_matrix = source.getMatrix(worldSpace=True)
source_pos = source.getTranslation("world")
source_rot = source.getRotation("world")



plane = pm.general.PyNode("mirrorLoc_rotate")
plane_matrix = plane.getMatrix(worldSpace=True)
plane_pos = plane.getTranslation("world")
plane_rot = plane.getRotation("world")
plane_normal = pm.dt.Vector([1, 0, 0]) * plane_matrix



dst = pm.general.PyNode("ARM_L_handIk_CTRL")
dst_matrix = dst.getMatrix(worldSpace=1)
dst_pos = dst.getTranslation("world")
dst_rot = dst.getRotation("world")




d = - (plane_normal.x * plane_pos.x + plane_normal.y * plane_pos.y + plane_normal.z * plane_pos.z)
k = - (plane_normal.x * source_pos.x + plane_normal.y * source_pos.y + plane_normal.z * source_pos.z + d) / (plane_normal.x**2 + plane_normal.y**2 + plane_normal.z**2)


px = k*plane_normal.x*2 + source_pos.x
py = k*plane_normal.y*2 + source_pos.y
pz = k*plane_normal.z*2 + source_pos.z
p = pm.dt.Vector([px, py, pz])

dst_parent = dst.getParent()


dst_matrix.inverse()
ppp = p * dst_matrix


dst_parent_matrix = dst_parent.getMatrix(worldSpace=1)
dst_parent_matrix_inverse = dst_parent_matrix.inverse()


dst.setTranslation(p, "world")


source_rot.asMatrix() * plane_normal

dst.setRotation(nr, "world")

180   -0    0

55.4294620073  69.08240847897001  2.60926012357


55.4294620073 - 180
-124.5705379927 69.08240847897001  2.60926012357




nr = pm.dt.EulerRotation([-124.5705379927, -141.35195875817, -2.60926012357]) 




pl = pm.dt.EulerRotation([0.0, -72.2695502792, 0.0])



x + 124.5705379927 = 0
y + 72.2695502792 = -69.08240847897001
z - 0 = -2.60926012357



x  180-124.5705379927
y  -69.08240847897001-72.2695502792
z 2.60926012357

"""