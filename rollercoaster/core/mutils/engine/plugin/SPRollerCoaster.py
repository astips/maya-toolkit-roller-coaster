# -*- coding: utf-8 -*-

###########################################################################################
#
# Description: South Park Roller Coaster Toolkit - Pose & Clip Data Cmd Plugin
#
#              Used to paste pose & animation data, blend pose with a percent
#              parse a xml data file, select contains in scene depend on data file,
#              copy pose & paste pose
#
#              Cmd:
#                   SPBlendBuild
#                   SPBlend
#                   SPSelectControl
#                   SPCopyPose
#                   SPPastePose
#                   SPMirrorPose
#                   SPFlipPose
#                   SPMirrorSelect
#                   SPResetControl
#
###########################################################################################
import sys
import json
import xml.etree.cElementTree as et

import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx
import maya.OpenMayaAnim as OpenMayaAnim

from rollercoaster.core.mutils.engine.engine import (
    _travel, _namespace, get_atomic_data, xrig_context
)
from rollercoaster.core.mutils import mplane


########################################################################################
#
#      SPRCPlugin - Global Vars
#
########################################################################################
ANIMLIBRARY_POSE_MULTI_DYN_DATA = {}
ANIMLIBRARY_POSE_CACHE_DATA = {}


########################################################################################
#
#      SPRCPlugin - Common Flags
#
########################################################################################
kAnimLibraryFlagTravelMode = '-m'
kAnimLibraryLongFlagTravelMode = '-mode'

kAnimLibraryFlagChannelBox = '-c'
kAnimLibraryLongFlagChannelBox = '-channelBox'

kAnimLibraryFlagXmlFile = '-f'
kAnimLibraryLongFlagXmlFile = '-file'

kAnimLibraryFlagNamespace = '-n'
kAnimLibraryLongFlagNamespace = '-namespace'

kAnimLibraryFlagApplyMode = '-a'
kAnimLibraryLongFlagApplyMode = '-applyMode'

kAnimLibraryFlagModify = '-i'
kAnimLibraryLongFlagModify = '-modify'

kAnimLibraryFlagKeep = '-k'
kAnimLibraryLongFlagKeep = '-keep'

kAnimLibraryFlagHelp = '-h'
kAnimLibraryLongFlagHelp = '-help'

kAnimLibraryFlagXrig = '-x'
kAnimLibraryLongFlagXrig = '-xrig'


########################################################################################
#
#      SPBlendBuild Cmd
#
########################################################################################
kPluginCmdBlendBuild = 'SPBlendBuild'


class SouthParkBlendBuild(OpenMayaMPx.MPxCommand):

    PRECISION = 3

    def __init__(self):
        OpenMayaMPx.MPxCommand.__init__(self)

    def parseArgs(self, kArguments):
        argData = OpenMaya.MArgParser(self.syntax(), kArguments)
        if argData.isFlagSet(kAnimLibraryFlagTravelMode):
            self.travel_mode = argData.flagArgumentString(kAnimLibraryFlagTravelMode, 0)
        elif argData.isFlagSet(kAnimLibraryLongFlagTravelMode):
            self.travel_mode = argData.flagArgumentString(kAnimLibraryLongFlagTravelMode, 0)
        else:
            self.travel_mode = 'SELECTED'

        if argData.isFlagSet(kAnimLibraryFlagChannelBox):
            self._channel = argData.flagArgumentBool(kAnimLibraryFlagChannelBox, 0)
        elif argData.isFlagSet(kAnimLibraryLongFlagChannelBox):
            self._channel = argData.flagArgumentBool(kAnimLibraryLongFlagChannelBox, 0)
        else:
            self._channel = False

        if argData.isFlagSet(kAnimLibraryFlagXmlFile):
            self._file = argData.flagArgumentString(kAnimLibraryFlagXmlFile, 0)
        elif argData.isFlagSet(kAnimLibraryLongFlagXmlFile):
            self._file = argData.flagArgumentString(kAnimLibraryLongFlagXmlFile, 0)
        else:
            raise Exception('-f (-file) flag needed.')

        if argData.isFlagSet(kAnimLibraryFlagNamespace):
            self._namespace = argData.flagArgumentString(kAnimLibraryFlagNamespace, 0)
        elif argData.isFlagSet(kAnimLibraryLongFlagNamespace):
            self._namespace = argData.flagArgumentString(kAnimLibraryLongFlagNamespace, 0)
        else:
            self._namespace = None

        if argData.isFlagSet(kAnimLibraryFlagApplyMode):
            self.apply_mode = argData.flagArgumentString(kAnimLibraryFlagApplyMode, 0)
        elif argData.isFlagSet(kAnimLibraryLongFlagApplyMode):
            self.apply_mode = argData.flagArgumentString(kAnimLibraryLongFlagApplyMode, 0)
        else:
            self.apply_mode = 'BLEND'

        if argData.isFlagSet(kAnimLibraryFlagModify):
            self._modify = argData.flagArgumentString(kAnimLibraryFlagModify, 0)
        elif argData.isFlagSet(kAnimLibraryLongFlagModify):
            self._modify = argData.flagArgumentString(kAnimLibraryLongFlagModify, 0)
        else:
            self._modify = None

        if argData.isFlagSet(kAnimLibraryFlagXrig):
            self._context = argData.flagArgumentString(kAnimLibraryFlagXrig, 0)
            self._xrig = xrig_context(self._context)
        elif argData.isFlagSet(kAnimLibraryLongFlagXrig):
            self._context = argData.flagArgumentString(kAnimLibraryLongFlagXrig, 0)
            self._xrig = xrig_context(self._context)
        else:
            raise Exception('-x (-xrig) flag needed.')

    def parse(self):
        datas = {}
        xmlTree = et.parse(self._file)
        dataElement = xmlTree.getroot().find('Data')
        for nodeElement in dataElement.getiterator('Node'):
            attrDict = {}
            nodeName = nodeElement.attrib['name']
            for attrElement in nodeElement.getiterator('Attr'):
                attrName = attrElement.attrib['name']
                attrDict[attrName] = {}
                values = []
                for keyElement in attrElement.getiterator('Key'):
                    value = json.loads(keyElement.attrib['value'])
                    values.append(value)
                attrDict[attrName]['value'] = values
            datas[nodeName] = attrDict
        return datas

    def doIt(self, kArguments):
        self.redoIt(kArguments)

    def redoIt(self, kArguments):
        self.parseArgs(kArguments)

        global ANIMLIBRARY_POSE_MULTI_DYN_DATA
        ANIMLIBRARY_POSE_MULTI_DYN_DATA = {}

        if self._namespace is None:
            self._namespace = _namespace()
            if self._namespace is None:
                raise Exception('Select Objects.')

        sceneDatas = get_atomic_data(mode=self.travel_mode, channel_box=self._channel, context=self._context)
        # print ('SCENE DATA', sceneDatas)
        xmlDatas = self.parse()
        # print ('XML DATA', xmlDatas)

        selectionList = OpenMaya.MSelectionList()

        xmlNodes = xmlDatas.keys()
        for nodeName, attrsDict in sceneDatas.iteritems():
            switchNodeName = None

            if self._modify == 'NORMAL':
                switchNodeName = nodeName

            elif self._modify == 'L':
                if not self._xrig.is_lt_ctrl(nodeName.split('|')[-1]):
                    continue
                switchNodeName = nodeName

            elif self._modify == 'R':
                if not self._xrig.is_rt_ctrl(nodeName.split('|')[-1]):
                    continue
                switchNodeName = nodeName

            elif self._modify == 'ML':
                if self._xrig.is_rt_ctrl(nodeName.split('|')[-1]):
                    switchNodeName = self._xrig.rt_to_lt(nodeName)
                else:
                    switchNodeName = nodeName

            elif self._modify == 'MR':
                if self._xrig.is_lt_ctrl(nodeName.split('|')[-1]):
                    switchNodeName = self._xrig.lt_to_rt(nodeName)
                else:
                    switchNodeName = nodeName

            elif self._modify == 'FLIP':
                switchNodeName = self._xrig.switch(nodeName)

            else:
                raise Exception('Invalid Argument.')

            if switchNodeName not in xmlNodes:
                continue

            _name = '|'.join(self._namespace+n for n in nodeName.split('|'))
            try:
                selectionList.add(_name)
            except:
                continue
            mObj = OpenMaya.MObject()
            selectionList.getDependNode(0, mObj)
            dagNodeFn = OpenMaya.MFnDagNode(mObj)
            selectionList.clear()

            _attrs = xmlDatas[switchNodeName].keys()
            for attrName, value in attrsDict.iteritems():
                if not attrName in _attrs:
                    continue

                plug = dagNodeFn.findPlug(attrName)

                if not plug.isKeyable():
                    continue

                if plug.isLocked():
                    continue

                if not plug.isFreeToChange(False, False) == OpenMaya.MPlug.kFreeToChange:
                    continue

                sceneValue = value
                xmlValue = xmlDatas[switchNodeName][attrName]['value'][0][1]
                # print switchNodeName, nodeName
                if not switchNodeName == nodeName:
                    if self._xrig.is_ik_ctrl(switchNodeName.split('|')[-1]):
                        if self._xrig.is_ik_flip_attr(attrName):
                            xmlValue *= -1

                    elif self._xrig.is_fk_ctrl(switchNodeName.split('|')[-1]):
                        if self._xrig.is_translate_attr(attrName):
                            xmlValue *= -1

                    else:
                        if self._xrig.is_facial_flip_attr(attrName):
                            xmlValue *= -1

                else:
                    if self._modify == 'FLIP':
                        if self._xrig.is_md_ctrl(switchNodeName.split('|')[-1]):
                            if self._xrig.is_md_flip_attr(attrName):
                                xmlValue *= -1

                if self.apply_mode == 'BLEND':
                    if round(xmlValue, self.PRECISION) != round(sceneValue, self.PRECISION):
                        dynValue = (float(xmlValue) - float(sceneValue)) / 100
                        ANIMLIBRARY_POSE_MULTI_DYN_DATA[plug] = [sceneValue, xmlValue, dynValue]

                elif self.apply_mode == 'MULTIPLIER':
                    dynValue = float(xmlValue) / 100
                    ANIMLIBRARY_POSE_MULTI_DYN_DATA[plug] = [sceneValue, xmlValue, dynValue]
                    
                else:
                    raise Exception('Invalid Mode(\n1.BLEND \n2.MULTIPLIER).')

    def isUndoable(self):
        return False


def blendBuildCmdCreator():
    return OpenMayaMPx.asMPxPtr(SouthParkBlendBuild())


def blendBuildSyntaxCreator():
    syntax = OpenMaya.MSyntax()
    syntax.addFlag(kAnimLibraryFlagTravelMode, kAnimLibraryLongFlagTravelMode, OpenMaya.MSyntax.kString)
    syntax.addFlag(kAnimLibraryFlagChannelBox, kAnimLibraryLongFlagChannelBox, OpenMaya.MSyntax.kBoolean)
    syntax.addFlag(kAnimLibraryFlagXmlFile, kAnimLibraryLongFlagXmlFile, OpenMaya.MSyntax.kString)
    syntax.addFlag(kAnimLibraryFlagNamespace, kAnimLibraryLongFlagNamespace, OpenMaya.MSyntax.kString)
    syntax.addFlag(kAnimLibraryFlagApplyMode, kAnimLibraryLongFlagApplyMode, OpenMaya.MSyntax.kString)
    syntax.addFlag(kAnimLibraryFlagModify, kAnimLibraryLongFlagModify, OpenMaya.MSyntax.kString)
    syntax.addFlag(kAnimLibraryFlagHelp, kAnimLibraryLongFlagHelp, OpenMaya.MSyntax.kString)
    syntax.addFlag(kAnimLibraryFlagXrig, kAnimLibraryLongFlagXrig, OpenMaya.MSyntax.kString)
    return syntax


########################################################################################
#
#        SPBlend Cmd
#
########################################################################################
kPluginCmdBlend = 'SPBlend'


class SouthParkBlend(OpenMayaMPx.MPxCommand):
    
    def __init__(self):
        OpenMayaMPx.MPxCommand.__init__(self)
        self.modifier = OpenMaya.MDGModifier()

    def parseArgs(self, kArguments):
        argData = OpenMaya.MArgParser(self.syntax(), kArguments)
        self.percent = argData.commandArgumentInt(0)

    def doIt(self, kArguments):
        self.parseArgs(kArguments)
        for plug, valueList in ANIMLIBRARY_POSE_MULTI_DYN_DATA.iteritems():
            v = valueList[0] + valueList[2] * self.percent
            self.modifier.newPlugValueFloat(plug, v)

        self.modifier.doIt()

    def redoIt(self):
        self.modifier.doIt()

    def undoIt(self):
        self.modifier.undoIt()

    def isUndoable(self):
        return True


def blendCmdCreator():
    return OpenMayaMPx.asMPxPtr(SouthParkBlend())


def blendSyntaxCreator():
    syntax = OpenMaya.MSyntax()
    syntax.addArg(OpenMaya.MSyntax.kLong)
    return syntax


########################################################################################
#
#        SPSelectControl Cmd
#
########################################################################################
kPluginCmdSelectByXml = 'SPSelectControl'


class SouthParkSelectControl(OpenMayaMPx.MPxCommand):
    
    def __init__(self):
        OpenMayaMPx.MPxCommand.__init__(self)
        self.bufferSelectionList = OpenMaya.MSelectionList()
        OpenMaya.MGlobal.getActiveSelectionList(self.bufferSelectionList)
        
    def parseArgs(self, kArguments):
        argData = OpenMaya.MArgParser(self.syntax(), kArguments)
        if argData.isFlagSet(kAnimLibraryFlagXmlFile):
            self.file = argData.flagArgumentString(kAnimLibraryFlagXmlFile, 0)
        elif argData.isFlagSet(kAnimLibraryLongFlagXmlFile):
            self.file = argData.flagArgumentString(kAnimLibraryLongFlagXmlFile, 0)
        else:
            raise Exception('-f (-file) flag needed.')

        if argData.isFlagSet(kAnimLibraryFlagNamespace):
            self.namespace = argData.flagArgumentString(kAnimLibraryFlagNamespace, 0)
        elif argData.isFlagSet(kAnimLibraryLongFlagNamespace):
            self.namespace = argData.flagArgumentString(kAnimLibraryLongFlagNamespace, 0)
        else:
            self.namespace = None

    def doIt(self, kArguments):
        self.redoIt(kArguments)

    def redoIt(self, kArguments):
        self.parseArgs(kArguments)

        if self.namespace is None:
            self.namespace = _namespace()
            if self.namespace is None:
                raise Exception('Select Objects.')

        xmlTree = et.parse(self.file)
        dataElement = xmlTree.getroot().find('Data')

        selectionList = OpenMaya.MSelectionList()
        for nodeElement in dataElement.getiterator('Node'):
            nodeName = nodeElement.attrib['name']
            _name = '|'.join(self.namespace+n for n in nodeName.split('|'))
            try:
                selectionList.add(_name)
            except:
                continue

        OpenMaya.MGlobal.setActiveSelectionList(selectionList)

    def undoIt(self):
        OpenMaya.MGlobal.setActiveSelectionList(self.bufferSelectionList)

    def isUndoable(self):
        return True


def selectByXmlCmdCreator():
    return OpenMayaMPx.asMPxPtr(SouthParkSelectControl())


def selectByXmlSyntaxCreator():
    syntax = OpenMaya.MSyntax()
    syntax.addFlag(kAnimLibraryFlagXmlFile, kAnimLibraryLongFlagXmlFile, OpenMaya.MSyntax.kString)
    syntax.addFlag(kAnimLibraryFlagNamespace, kAnimLibraryLongFlagNamespace, OpenMaya.MSyntax.kString)
    return syntax


########################################################################################
#
#        SPCopyPose Cmd
#
########################################################################################
kPluginCmdCopyPose = 'SPCopyPose'


class SouthParkCopyPose(OpenMayaMPx.MPxCommand):
    
    def __init__(self):
        OpenMayaMPx.MPxCommand.__init__(self)

    def parseArgs(self, kArguments):
        argData = OpenMaya.MArgParser(self.syntax(), kArguments)
        if argData.isFlagSet(kAnimLibraryFlagTravelMode):
            self.travel_mode = argData.flagArgumentString(kAnimLibraryFlagTravelMode, 0)
        elif argData.isFlagSet(kAnimLibraryLongFlagTravelMode):
            self.travel_mode = argData.flagArgumentString(kAnimLibraryLongFlagTravelMode, 0)
        else:
            raise Exception('-m (-mode) flag needed.')

        if argData.isFlagSet(kAnimLibraryFlagChannelBox):
            self.channelBox = argData.flagArgumentBool(kAnimLibraryFlagChannelBox, 0)
        elif argData.isFlagSet(kAnimLibraryLongFlagChannelBox):
            self.channelBox = argData.flagArgumentBool(kAnimLibraryLongFlagChannelBox, 0)
        else:
            self.channelBox = False

        if argData.isFlagSet(kAnimLibraryFlagXrig):
            self._context = argData.flagArgumentString(kAnimLibraryFlagXrig, 0)
        elif argData.isFlagSet(kAnimLibraryLongFlagXrig):
            self._context = argData.flagArgumentString(kAnimLibraryLongFlagXrig, 0)
        else:
            raise Exception('-x (-xrig) flag needed.')

    def doIt(self, kArguments):
        self.redoIt(kArguments)

    def redoIt(self, kArguments):
        self.parseArgs(kArguments)
        global ANIMLIBRARY_POSE_CACHE_DATA
        ANIMLIBRARY_POSE_CACHE_DATA = get_atomic_data(
            mode=self.travel_mode, channel_box=self.channelBox, context=self._context
        )
        # print ANIMLIBRARY_POSE_CACHE_DATA

    def isUndoable(self):
        return False


def copyPoseCmdCreator():
    return OpenMayaMPx.asMPxPtr(SouthParkCopyPose())


def copyPoseSyntaxCreator():
    syntax = OpenMaya.MSyntax()
    syntax.addFlag(kAnimLibraryFlagTravelMode, kAnimLibraryLongFlagTravelMode, OpenMaya.MSyntax.kString)
    syntax.addFlag(kAnimLibraryFlagChannelBox, kAnimLibraryLongFlagChannelBox, OpenMaya.MSyntax.kBoolean)
    syntax.addFlag(kAnimLibraryFlagXrig, kAnimLibraryLongFlagXrig, OpenMaya.MSyntax.kString)
    return syntax


########################################################################################
#
#        SPPastePose Cmd
#
########################################################################################
kPluginCmdPastePose = 'SPPastePose'


class SouthParkPastePose(OpenMayaMPx.MPxCommand):
    
    def __init__(self):
        OpenMayaMPx.MPxCommand.__init__(self)
        self.modifier = OpenMaya.MDGModifier()

    def parseArgs(self, kArguments):
        argData = OpenMaya.MArgParser(self.syntax(), kArguments)

        if argData.isFlagSet(kAnimLibraryFlagTravelMode):
            self.travel_mode = argData.flagArgumentString(kAnimLibraryFlagTravelMode, 0)
        elif argData.isFlagSet(kAnimLibraryLongFlagTravelMode):
            self.travel_mode = argData.flagArgumentString(kAnimLibraryLongFlagTravelMode, 0)
        else:
            raise Exception('-m (-mode) flag needed.')

        if argData.isFlagSet(kAnimLibraryFlagNamespace):
            self.namespace = argData.flagArgumentString(kAnimLibraryFlagNamespace, 0)
        elif argData.isFlagSet(kAnimLibraryLongFlagNamespace):
            self.namespace = argData.flagArgumentString(kAnimLibraryLongFlagNamespace, 0)
        else:
            self.namespace = None

        if argData.isFlagSet(kAnimLibraryFlagXrig):
            self._context = argData.flagArgumentString(kAnimLibraryFlagXrig, 0)
        elif argData.isFlagSet(kAnimLibraryLongFlagXrig):
            self._context = argData.flagArgumentString(kAnimLibraryLongFlagXrig, 0)
        else:
            self._context = None

    def doIt(self, kArguments):
        self.redoIt(kArguments)

    def redoIt(self, kArguments):
        self.parseArgs(kArguments)

        if self.namespace is None:
            self.namespace = _namespace()
            if self.namespace is None:
                raise Exception('Select Objects.')

        global ANIMLIBRARY_POSE_CACHE_DATA
        nodes = []
        _nodes = _travel(mode=self.travel_mode, context=self._context) or []
        for _node in _nodes:
            tokens = OpenMaya.MFnDagNode(_node).partialPathName().split('|')
            nodes.append('|'.join([token.split(':')[-1] for token in tokens]))

        selectionList = OpenMaya.MSelectionList()
        for nodeName, attrsDict in ANIMLIBRARY_POSE_CACHE_DATA.iteritems():
            if not nodeName in nodes:
                continue

            _name = '|'.join(self.namespace+n for n in nodeName.split('|'))
            selectionList.add(_name)

            mObj = OpenMaya.MObject()
            selectionList.getDependNode(0, mObj)
            dagNodeFn = OpenMaya.MFnDagNode(mObj)

            selectionList.clear()

            for attrName, value in attrsDict.iteritems():
                plug = dagNodeFn.findPlug(attrName)
                if plug.isNull():
                    continue

                if not plug.isKeyable():
                    continue

                if plug.isLocked():
                    continue

                if not plug.isFreeToChange(False, False) == OpenMaya.MPlug.kFreeToChange:
                    continue

                self.modifier.newPlugValueFloat(plug, value)

        self.modifier.doIt()

    def undoIt(self):
        self.modifier.undoIt()

    def isUndoable(self):
        return True


def pastePoseCmdCreator():
    return OpenMayaMPx.asMPxPtr(SouthParkPastePose())


def pastePoseSyntaxCreator():
    syntax = OpenMaya.MSyntax()
    syntax.addFlag(kAnimLibraryFlagTravelMode, kAnimLibraryLongFlagTravelMode, OpenMaya.MSyntax.kString)
    syntax.addFlag(kAnimLibraryFlagNamespace, kAnimLibraryLongFlagNamespace, OpenMaya.MSyntax.kString)
    syntax.addFlag(kAnimLibraryFlagXrig, kAnimLibraryLongFlagXrig, OpenMaya.MSyntax.kString)
    return syntax


########################################################################################
#
#        SPMirrorPose Cmd
#
########################################################################################
kPluginCmdMirrorPose = 'SPMirrorPose'


class SouthParkMirrorPose(OpenMayaMPx.MPxCommand):
    
    def __init__(self):
        OpenMayaMPx.MPxCommand.__init__(self)
        self.modifier = OpenMaya.MDGModifier()
        self.results = None

    def parseArgs(self, kArguments):
        argData = OpenMaya.MArgParser(self.syntax(), kArguments)

        if argData.isFlagSet(kAnimLibraryFlagXrig):
            self._context = argData.flagArgumentString(kAnimLibraryFlagXrig, 0)
            self._xrig = xrig_context(self._context)
        elif argData.isFlagSet(kAnimLibraryLongFlagXrig):
            self._context = argData.flagArgumentString(kAnimLibraryLongFlagXrig, 0)
            self._xrig = xrig_context(self._context)
        else:
            raise Exception('-x (-xrig) flag needed.')

    def doIt(self, kArguments):
        self.redoIt(kArguments)

    def redoIt(self, kArguments):
        self.parseArgs(kArguments)

        namespace = _namespace()
        if namespace is None:
            raise Exception('Select Objects.')

        datas = get_atomic_data(mode='SELECTED', channel_box=False, context=self._context)

        plane = mplane.getMirrorPlane(namespace)

        self.results = []
        selectionList = OpenMaya.MSelectionList()
        for nodeName, attrsDict in datas.iteritems():
            switchNodeName = self._xrig.switch(nodeName)
            _name = '|'.join(namespace+n for n in switchNodeName.split('|'))
            try:
                selectionList.add(_name)
            except:
                continue
            mObj = OpenMaya.MObject()
            selectionList.getDependNode(0, mObj)
            dagNodeFn = OpenMaya.MFnDagNode(mObj)
            selectionList.clear()

            for attrName, value in attrsDict.iteritems():
                if not dagNodeFn.hasAttribute(attrName):
                    continue

                plug = dagNodeFn.findPlug(attrName)

                if not plug.isKeyable():
                    continue

                if plug.isLocked():
                    continue

                if not plug.isFreeToChange(False, False) == OpenMaya.MPlug.kFreeToChange:
                    continue

                if switchNodeName == nodeName:
                    aimValue = value

                    if self._xrig.is_md_ctrl(switchNodeName.split('|')[-1]):
                        if self._xrig.is_md_flip_attr(attrName):
                            aimValue *= -1

                else:
                    aimValue = value

                    if self._xrig.is_ik_ctrl(switchNodeName.split('|')[-1]):
                        if self._xrig.is_translate_attr(attrName):
                            continue
                        if self._xrig.is_rotate_attr(attrName):
                            continue

                    elif self._xrig.is_fk_ctrl(switchNodeName.split('|')[-1]):
                        if self._xrig.is_translate_attr(attrName):
                            aimValue = value * -1

                    else:
                        if self._xrig.is_facial_flip_attr(attrName):
                            aimValue = value * -1

                self.modifier.newPlugValueFloat(plug, aimValue)

            if self._xrig.is_ik_ctrl(switchNodeName.split('|')[-1]):
                if plane is None:
                    continue
                result = mplane.magicMirror(src='|'.join(namespace+n for n in nodeName.split('|')), 
                                            dst='|'.join(namespace+n for n in switchNodeName.split('|')), 
                                            plane=plane, 
                                            active=False, 
                                            space='world', 
                                            context=self._context
                                            )
                result[0].setTranslation(result[1], OpenMaya.MSpace.kWorld)
                result[0].setRotation(result[2], OpenMaya.MSpace.kWorld)
                self.results.append(result)

        self.modifier.doIt()

    def undoIt(self):
        self.modifier.undoIt()
        for result in self.results:
            result[0].setTranslation(result[3], OpenMaya.MSpace.kWorld)
            result[0].setRotation(result[4], OpenMaya.MSpace.kWorld)

    def isUndoable(self):
        return True


def mirrorPoseCmdCreator():
    return OpenMayaMPx.asMPxPtr(SouthParkMirrorPose())


def mirrorPoseSyntaxCreator():
    syntax = OpenMaya.MSyntax()
    syntax.addFlag(kAnimLibraryFlagXrig, kAnimLibraryLongFlagXrig, OpenMaya.MSyntax.kString)
    return syntax


########################################################################################
#
#        SPFlipPose Cmd
#
########################################################################################
kPluginCmdFlipPose = 'SPFlipPose'


class SouthParkFlipPose(OpenMayaMPx.MPxCommand):
    
    def __init__(self):
        OpenMayaMPx.MPxCommand.__init__(self)
        self.modifier = OpenMaya.MDGModifier()
        self.results = None

    def parseArgs(self, kArguments):
        argData = OpenMaya.MArgParser(self.syntax(), kArguments)
        if argData.isFlagSet(kAnimLibraryFlagXrig):
            self._context = argData.flagArgumentString(kAnimLibraryFlagXrig, 0)
            self._xrig = xrig_context(self._context)
        elif argData.isFlagSet(kAnimLibraryLongFlagXrig):
            self._context = argData.flagArgumentString(kAnimLibraryLongFlagXrig, 0)
            self._xrig = xrig_context(self._context)
        else:
            raise Exception('-x (-xrig) flag needed.')

    def doIt(self, kArguments):
        self.redoIt(kArguments)

    def redoIt(self, kArguments):
        self.parseArgs(kArguments)

        namespace = _namespace()
        if namespace is None:
            raise Exception('Select Objects.')

        datas = get_atomic_data(mode='SELECTED', channel_box=False, context=self._context)

        plane = mplane.getMirrorPlane(namespace)

        selectionList = OpenMaya.MSelectionList()
        self.results = []
        for nodeName, attrsDict in datas.iteritems():
            selectionList.clear()

            switchNodeName = self._xrig.switch(nodeName)

            this_name = '|'.join(namespace+n for n in nodeName.split('|'))
            that_name = '|'.join(namespace+n for n in switchNodeName.split('|'))

            if this_name == that_name:
                """
                maybe this is a M_xxx_ctrl.
                ignore it for now.
                maybe future we can flip some rotate value.
                """
                if not self._xrig.is_md_ctrl(switchNodeName.split('|')[-1]):
                    continue

                try:
                    selectionList.add(this_name)
                except:
                    continue

                mobj = OpenMaya.MObject()
                selectionList.getDependNode(0, mobj)
                dagNodeFn = OpenMaya.MFnDagNode(mobj)

                for attrName, value in attrsDict.iteritems():
                    if not dagNodeFn.hasAttribute(attrName):
                        continue

                    plug = dagNodeFn.findPlug(attrName)
                    if not plug.isKeyable():
                        continue
                    if plug.isLocked():
                        continue
                    if not plug.isFreeToChange(False, False) == OpenMaya.MPlug.kFreeToChange:
                        continue

                    aimValue = plug.asFloat()
                    if self._xrig.is_md_flip_attr(attrName):
                        aimValue *= -1

                    self.modifier.newPlugValueFloat(plug, aimValue)
                continue

            try:
                selectionList.add(this_name)
                selectionList.add(that_name)
            except:
                continue

            this_mobj = OpenMaya.MObject()
            that_mobj = OpenMaya.MObject()
            selectionList.getDependNode(0, this_mobj)
            selectionList.getDependNode(1, that_mobj)

            this_dagNodeFn = OpenMaya.MFnDagNode(this_mobj)
            that_dagNodeFn = OpenMaya.MFnDagNode(that_mobj)

            for attrName, value in attrsDict.iteritems():
                if not that_dagNodeFn.hasAttribute(attrName):
                    continue

                this_plug = this_dagNodeFn.findPlug(attrName)
                that_plug = that_dagNodeFn.findPlug(attrName)

                if not that_plug.isKeyable():
                    continue

                if that_plug.isLocked():
                    continue

                if not that_plug.isFreeToChange(False, False) == OpenMaya.MPlug.kFreeToChange:
                    continue

                that_value = that_plug.asFloat()

                if switchNodeName == nodeName:
                    this_aimValue = that_value
                    that_aimValue = value

                else:
                    this_aimValue = that_value
                    that_aimValue = value

                    if self._xrig.is_ik_ctrl(switchNodeName.split('|')[-1]):
                        if self._xrig.is_translate_attr(attrName):
                            continue
                        if self._xrig.is_rotate_attr(attrName):
                            continue

                    elif self._xrig.is_fk_ctrl(switchNodeName.split('|')[-1]):
                        if self._xrig.is_translate_attr(attrName):
                            this_aimValue = that_value * -1
                            that_aimValue = value * -1
                    else:
                        if self._xrig.is_facial_flip_attr(attrName):
                            this_aimValue = that_value * -1
                            that_aimValue = value * -1
                                
                self.modifier.newPlugValueFloat(this_plug, this_aimValue)
                self.modifier.newPlugValueFloat(that_plug, that_aimValue)

            if self._xrig.is_ik_ctrl(switchNodeName.split('|')[-1]):
                if plane is None:
                    continue

                this_results = mplane.magicMirror(src=this_name, 
                                                  dst=that_name, 
                                                  plane=plane, 
                                                  active=False, 
                                                  space='world', 
                                                  context=self._context
                                                  )
                that_results = mplane.magicMirror(src=that_name, 
                                                  dst=this_name, 
                                                  plane=plane, 
                                                  active=False, 
                                                  space='world', 
                                                  context=self._context
                                                  )

                this_results[0].setTranslation(this_results[1], OpenMaya.MSpace.kWorld)
                this_results[0].setRotation(this_results[2], OpenMaya.MSpace.kWorld)
                that_results[0].setTranslation(that_results[1], OpenMaya.MSpace.kWorld)
                that_results[0].setRotation(that_results[2], OpenMaya.MSpace.kWorld)

                self.results.append([this_results, that_results])

        self.modifier.doIt()

    def undoIt(self):
        self.modifier.undoIt()
        for result in self.results:
            result[0][0].setTranslation(result[0][3], OpenMaya.MSpace.kWorld)
            result[0][0].setRotation(result[0][4], OpenMaya.MSpace.kWorld)
            result[1][0].setTranslation(result[1][3], OpenMaya.MSpace.kWorld)
            result[1][0].setRotation(result[1][4], OpenMaya.MSpace.kWorld)

    def isUndoable(self):
        return True


def flipPoseCmdCreator():
    return OpenMayaMPx.asMPxPtr(SouthParkFlipPose())


def flipPoseSyntaxCreator():
    syntax = OpenMaya.MSyntax()
    syntax.addFlag(kAnimLibraryFlagXrig, kAnimLibraryLongFlagXrig, OpenMaya.MSyntax.kString)
    return syntax


########################################################################################
#
#        SPMirrorSelect Cmd
#
########################################################################################
kPluginCmdMirrorSelect = 'SPMirrorSelect'


class SouthParkMirrorSelect(OpenMayaMPx.MPxCommand):
    
    def __init__(self):
        OpenMayaMPx.MPxCommand.__init__(self)
        self.bufferSelectionList = OpenMaya.MSelectionList()
        OpenMaya.MGlobal.getActiveSelectionList(self.bufferSelectionList)

    def parseArgs(self, kArguments):
        argData = OpenMaya.MArgParser(self.syntax(), kArguments)
        if argData.isFlagSet(kAnimLibraryFlagKeep):
            self.keep = argData.flagArgumentBool(kAnimLibraryFlagKeep, 0)
        elif argData.isFlagSet(kAnimLibraryLongFlagKeep):
            self.keep = argData.flagArgumentBool(kAnimLibraryLongFlagKeep, 0)
        else:
            self.keep = True

        if argData.isFlagSet(kAnimLibraryFlagXrig):
            self._context = argData.flagArgumentString(kAnimLibraryFlagXrig, 0)
            self._xrig = xrig_context(self._context)
        elif argData.isFlagSet(kAnimLibraryLongFlagXrig):
            self._context = argData.flagArgumentString(kAnimLibraryLongFlagXrig, 0)
            self._xrig = xrig_context(self._context)
        else:
            raise Exception('-x (-xrig) flag needed.')

    def doIt(self, kArguments):
        self.redoIt(kArguments)

    def redoIt(self, kArguments):
        self.parseArgs(kArguments)

        namespace = _namespace()
        if namespace is None:
            raise Exception('Select Objects.')

        nodes = _travel(mode='SELECTED', context=self._context)
        selectionList = OpenMaya.MSelectionList()
        selectionList.clear()
        for node in nodes:
            dagNodeFn = OpenMaya.MFnDagNode(node)
            nodeName = '|'.join([token.split(':')[-1] for token in dagNodeFn.partialPathName().split('|')])

            switchNodeName = self._xrig.switch(nodeName)
            _name = '|'.join(namespace+n for n in switchNodeName.split('|'))
            if self.keep:
                selectionList.add(dagNodeFn.fullPathName(), False)
                
            try:
                selectionList.add(_name, False)
            except:
                continue

        OpenMaya.MGlobal.setActiveSelectionList(selectionList, OpenMaya.MGlobal.kReplaceList)

    def undoIt(self):
        OpenMaya.MGlobal.setActiveSelectionList(self.bufferSelectionList)

    def isUndoable(self):
        return True


def mirrorSelectCmdCreator():
    return OpenMayaMPx.asMPxPtr(SouthParkMirrorSelect())


def mirrorSelectSyntaxCreator():
    syntax = OpenMaya.MSyntax()
    syntax.addFlag(kAnimLibraryFlagKeep, kAnimLibraryLongFlagKeep, OpenMaya.MSyntax.kBoolean)
    syntax.addFlag(kAnimLibraryFlagXrig, kAnimLibraryLongFlagXrig, OpenMaya.MSyntax.kString)
    return syntax


########################################################################################
#
#        SPResetControl Cmd
#
########################################################################################
kPluginCmdReset = 'SPResetControl'


class SouthParkReset(OpenMayaMPx.MPxCommand):
    """
    reset objs' all keyable attr to default value
    """
    def __init__(self):
        OpenMayaMPx.MPxCommand.__init__(self)
        self.modifier = OpenMaya.MDGModifier()

    def parseArgs(self, kArguments):
        argData = OpenMaya.MArgParser(self.syntax(), kArguments)
        if argData.isFlagSet(kAnimLibraryFlagTravelMode):
            self.travel_mode = argData.flagArgumentString(kAnimLibraryFlagTravelMode, 0)
        elif argData.isFlagSet(kAnimLibraryLongFlagTravelMode):
            self.travel_mode = argData.flagArgumentString(kAnimLibraryLongFlagTravelMode, 0)
        else:
            self.travel_mode = 'SELECTED'

        if argData.isFlagSet(kAnimLibraryFlagXrig):
            self._context = argData.flagArgumentString(kAnimLibraryFlagXrig, 0)
            self._xrig = xrig_context(self._context)
        elif argData.isFlagSet(kAnimLibraryLongFlagXrig):
            self._context = argData.flagArgumentString(kAnimLibraryLongFlagXrig, 0)
            self._xrig = xrig_context(self._context)
        else:
            raise Exception('-x (-xrig) flag needed.')

    def __reset(self, plug):
        scriptUtil = OpenMaya.MScriptUtil()
        attr = plug.attribute()
        if attr.hasFn(OpenMaya.MFn.kUnitAttribute):
            attrFn = OpenMaya.MFnUnitAttribute(attr)
            unitType = attrFn.unitType()

            if unitType == OpenMaya.MFnUnitAttribute.kAngle or \
               unitType == OpenMaya.MFnUnitAttribute.kDistance:
                ptr = scriptUtil.asDoublePtr()
                attrFn.getDefault(ptr)
                value = scriptUtil.getDouble(ptr)

                self.modifier.newPlugValueDouble(plug, value)

            elif unitType == OpenMaya.MFnUnitAttribute.kTime:
                ptr = scriptUtil.asDoublePtr()
                attrFn.getDefault(ptr)
                value = scriptUtil.getDouble(ptr)

                t = OpenMaya.MTime(value)
                self.modifier.newPlugValueMTime(plug, t)
            else:
                pass

        elif attr.hasFn(OpenMaya.MFn.kNumericAttribute):
            attrFn = OpenMaya.MFnNumericAttribute(attr)
            unitType = attrFn.unitType()

            if unitType == OpenMaya.MFnNumericData.kBoolean:
                ptr = scriptUtil.asBoolPtr()
                attrFn.getDefault(ptr)
                value = scriptUtil.getBool(ptr)
                self.modifier.newPlugValueBool(plug, value)

            elif unitType == OpenMaya.MFnNumericData.kByte or \
                 unitType == OpenMaya.MFnNumericData.kChar:
                ptr = scriptUtil.asCharPtr()
                attrFn.getDefault(ptr)
                value = scriptUtil.getChar(ptr)
                self.modifier.newPlugValueChar(plug, value)

            elif unitType == OpenMaya.MFnNumericData.kShort:
                ptr = scriptUtil.asShortPtr()
                attrFn.getDefault(ptr)
                value = scriptUtil.getShort(ptr)
                self.modifier.newPlugValueShort(plug, value)

            elif unitType == OpenMaya.MFnNumericData.kLong:
                ptr = scriptUtil.asIntPtr()
                attrFn.getDefault(ptr)
                value = scriptUtil.getInt(ptr)
                self.modifier.newPlugValueInt(plug, value)

            elif unitType == OpenMaya.MFnNumericData.kFloat:
                ptr = scriptUtil.asDoublePtr()
                attrFn.getDefault(ptr)
                value = scriptUtil.getDouble(ptr)
                self.modifier.newPlugValueFloat(plug, float(value))

            elif unitType == OpenMaya.MFnNumericData.kDouble:
                ptr = scriptUtil.asDoublePtr()
                attrFn.getDefault(ptr)
                value = scriptUtil.getDouble(ptr)
                self.modifier.newPlugValueDouble(plug, value)

            else:
                pass

        elif attr.hasFn(OpenMaya.MFn.kEnumAttribute):
            attrFn = OpenMaya.MFnEnumAttribute(attr)
            ptr = scriptUtil.asShortPtr()
            attrFn.getDefault(ptr)
            value = scriptUtil.getShort(ptr)

            self.modifier.newPlugValueShort(plug, value)

        else:
            pass
        
    def doIt(self, kArguments):
        self.parseArgs(kArguments)

        nodes = _travel(mode=self.travel_mode, context=self._context) or []
        if not len(nodes):
            return

        plugArray = OpenMaya.MPlugArray()

        selectionList = OpenMaya.MSelectionList()
        for node in nodes:
            plugArray.clear()
            selectionList.clear()
            selectionList.add(node)

            OpenMayaAnim.MAnimUtil.findAnimatablePlugs(selectionList, plugArray)

            for i in xrange(plugArray.length()):
                if not plugArray[i].isKeyable():
                    continue

                if plugArray[i].isLocked():
                    continue

                if not plugArray[i].isFreeToChange(False, False) == OpenMaya.MPlug.kFreeToChange:
                    continue

                linkPlugArray = OpenMaya.MPlugArray()
                plugArray[i].connectedTo(linkPlugArray, True, False)
                if linkPlugArray.length():
                    connectedNode = linkPlugArray[0].node()

                    if (connectedNode.hasFn(OpenMaya.MFn.kAnimCurveTimeToAngular) or
                        connectedNode.hasFn(OpenMaya.MFn.kAnimCurveTimeToDistance) or
                        connectedNode.hasFn(OpenMaya.MFn.kAnimCurveTimeToTime) or
                        connectedNode.hasFn(OpenMaya.MFn.kAnimCurveTimeToUnitless)
                        ):

                        self.__reset(plugArray[i])

                    elif (connectedNode.hasFn(OpenMaya.MFn.kAimConstraint) or
                          connectedNode.hasFn(OpenMaya.MFn.kOrientConstraint) or
                          connectedNode.hasFn(OpenMaya.MFn.kPointConstraint) or
                          connectedNode.hasFn(OpenMaya.MFn.kParentConstraint) or
                          connectedNode.hasFn(OpenMaya.MFn.kScaleConstraint) or
                          connectedNode.hasFn(OpenMaya.MFn.kTangentConstraint) or
                          connectedNode.hasFn(OpenMaya.MFn.kPoleVectorConstraint) or
                          connectedNode.hasFn(OpenMaya.MFn.kSymmetryConstraint)
                          ):
                        """
                        do nothing, constrainted attr don't reset.
                        """
                        pass

                    else:
                        pass

                else:
                    self.__reset(plugArray[i])
        self.modifier.doIt()

    def redoIt(self):
        self.modifier.doIt()

    def undoIt(self):
        self.modifier.undoIt()

    def isUndoable(self):
        return True


def resetCmdCreator():
    return OpenMayaMPx.asMPxPtr(SouthParkReset())


def resetSyntaxCreator():
    syntax = OpenMaya.MSyntax()
    syntax.addFlag(kAnimLibraryFlagTravelMode, kAnimLibraryLongFlagTravelMode, OpenMaya.MSyntax.kString)
    syntax.addFlag(kAnimLibraryFlagXrig, kAnimLibraryLongFlagXrig, OpenMaya.MSyntax.kString)
    return syntax


########################################################################################
#
#    initializePlugin / uninitializePlugin
#
########################################################################################
def initializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject, 'astips', '1.0.0', 'Any')

    try:
        mplugin.registerCommand(kPluginCmdBlendBuild, blendBuildCmdCreator, blendBuildSyntaxCreator)
    except:
        sys.stderr.write('Failed to register command: {0}'.format(kPluginCmdBlendBuild))
        raise Exception('Failed to register command: {0}'.format(kPluginCmdBlendBuild))

    try:
        mplugin.registerCommand(kPluginCmdBlend, blendCmdCreator, blendSyntaxCreator)
    except:
        sys.stderr.write('Failed to register command: {0}'.format(kPluginCmdBlend))
        raise Exception('Failed to register command: {0}'.format(kPluginCmdBlend))

    try:
        mplugin.registerCommand(kPluginCmdSelectByXml, selectByXmlCmdCreator, selectByXmlSyntaxCreator)
    except:
        sys.stderr.write('Failed to register command: {0}'.format(kPluginCmdSelectByXml))
        raise Exception('Failed to register command: {0}'.format(kPluginCmdSelectByXml))

    try:
        mplugin.registerCommand(kPluginCmdCopyPose, copyPoseCmdCreator, copyPoseSyntaxCreator)
    except:
        sys.stderr.write('Failed to register command: {0}'.format(kPluginCmdCopyPose))
        raise Exception('Failed to register command: {0}'.format(kPluginCmdCopyPose))

    try:
        mplugin.registerCommand(kPluginCmdPastePose, pastePoseCmdCreator, pastePoseSyntaxCreator)
    except:
        sys.stderr.write('Failed to register command: {0}'.format(kPluginCmdPastePose))
        raise Exception('Failed to register command: {0}'.format(kPluginCmdPastePose))

    try:
        mplugin.registerCommand(kPluginCmdMirrorPose, mirrorPoseCmdCreator, mirrorPoseSyntaxCreator)
    except:
        sys.stderr.write('Failed to register command: {0}'.format(kPluginCmdMirrorPose))
        raise Exception('Failed to register command: {0}'.format(kPluginCmdMirrorPose))

    try:
        mplugin.registerCommand(kPluginCmdFlipPose, flipPoseCmdCreator, flipPoseSyntaxCreator)
    except:
        sys.stderr.write('Failed to register command: {0}'.format(kPluginCmdFlipPose))
        raise Exception('Failed to register command: {0}'.format(kPluginCmdFlipPose))

    try:
        mplugin.registerCommand(kPluginCmdMirrorSelect, mirrorSelectCmdCreator, mirrorSelectSyntaxCreator)
    except:
        sys.stderr.write('Failed to register command: {0}'.format(kPluginCmdMirrorSelect))
        raise Exception('Failed to register command: {0}'.format(kPluginCmdMirrorSelect))

    try:
        mplugin.registerCommand(kPluginCmdReset, resetCmdCreator, resetSyntaxCreator)
    except:
        sys.stderr.write('Failed to register command: {0}'.format(kPluginCmdReset))
        raise Exception('Failed to register command: {0}'.format(kPluginCmdReset))


def uninitializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)

    try:
        mplugin.deregisterCommand(kPluginCmdBlendBuild)  
    except:
        sys.stderr.write('Failed to un-register command: {0}'.format(kPluginCmdBlendBuild))
        raise Exception('Failed to un-register command: {0}'.format(kPluginCmdBlendBuild))

    try:
        mplugin.deregisterCommand(kPluginCmdBlend)
    except:
        sys.stderr.write('Failed to un-register command: {0}'.format(kPluginCmdBlend))
        raise Exception('Failed to un-register command: {0}'.format(kPluginCmdBlend))

    try:
        mplugin.deregisterCommand(kPluginCmdSelectByXml)
    except:
        sys.stderr.write('Failed to un-register command: {0}'.format(kPluginCmdSelectByXml))
        raise Exception('Failed to un-register command: {0}'.format(kPluginCmdSelectByXml))

    try:
        mplugin.deregisterCommand(kPluginCmdCopyPose)
    except:
        sys.stderr.write('Failed to un-register command: {0}'.format(kPluginCmdCopyPose))
        raise Exception('Failed to un-register command: {0}'.format(kPluginCmdCopyPose))

    try:
        mplugin.deregisterCommand(kPluginCmdPastePose)
    except:
        sys.stderr.write('Failed to un-register command: {0}'.format(kPluginCmdPastePose))
        raise Exception('Failed to un-register command: {0}'.format(kPluginCmdPastePose))

    try:
        mplugin.deregisterCommand(kPluginCmdMirrorPose)
    except:
        sys.stderr.write('Failed to un-register command: {0}'.format(kPluginCmdMirrorPose))
        raise Exception('Failed to un-register command: {0}'.format(kPluginCmdMirrorPose))

    try:
        mplugin.deregisterCommand(kPluginCmdFlipPose)
    except:
        sys.stderr.write('Failed to un-register command: {0}'.format(kPluginCmdFlipPose))
        raise Exception('Failed to un-register command: {0}'.format(kPluginCmdFlipPose))

    try:
        mplugin.deregisterCommand(kPluginCmdMirrorSelect)
    except:
        sys.stderr.write('Failed to un-register command: {0}'.format(kPluginCmdMirrorSelect))
        raise Exception('Failed to un-register command: {0}'.format(kPluginCmdMirrorSelect))

    try:
        mplugin.deregisterCommand(kPluginCmdReset)
    except:
        sys.stderr.write('Failed to un-register command: {0}'.format(kPluginCmdReset))
        raise Exception('Failed to un-register command: {0}'.format(kPluginCmdReset))
