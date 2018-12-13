# -*- coding: utf-8 -*-

###########################################################################################
#
# Description: South Park Roller Coaster Toolkit - Pose & Clip Cmd Plugin
#
#              Used to paste pose & animation data, blend pose with a percent
#              parse a xml data file, select contains in scene depend on data file,
#              copy pose & paste pose
#
#              Cmd:
#                   SPRCBlendBuild
#                   SPRCBlend
#                   SPRCSelectControl
#                   SPRCCopyPose
#                   SPRCPastePose
#                   SPRCMirrorPose
#                   SPRCFlipPose
#                   SPRCMirrorSelect
#                   SPRCResetControl
#
###########################################################################################
import sys
import json
import xml.etree.cElementTree as et

import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx
import maya.OpenMayaAnim as OpenMayaAnim

from rollercoaster.core.const import (
    TRAVEL_MODE, POSE_APPLY_MODE, POSE_APPLY_MODIFY
)
from rollercoaster.core.mutils.engine import mplane
from rollercoaster.core.mutils.engine.engine import (
    _travel, _namespace, get_atomic_data, xrig_context
)

########################################################################################
#
#      SPRCPlugin - Global Vars
#
########################################################################################
SPRC_POSE_MULTI_DYN_DATA = {}
SPRC_POSE_CACHE_DATA = {}


########################################################################################
#
#      SPRCPlugin - Common Flags
#
########################################################################################
SPRC_TravelModeFlag = '-m'
SPRC_TravelModeFlagLong = '-mode'

SPRC_ChannelBoxFlag = '-c'
SPRC_ChannelBoxFlagLong = '-channelBox'

SPRC_FlagDataFile = '-f'
SPRC_DataFileFlagLong = '-file'

SPRC_NamespaceFlag = '-n'
SPRC_NamespaceFlagLong = '-namespace'

SPRC_ApplyModeFlag = '-a'
SPRC_ApplyModeFlagLong = '-applyMode'

SPRC_ModifyFlag = '-i'
SPRC_ModifyFlagLong = '-modify'

SPRC_KeepFlag = '-k'
SPRC_KeepFlagLong = '-keep'

SPRC_HelpFlag = '-h'
SPRC_HelpFlagLong = '-help'

SPRC_XRIGFlag = '-x'
SPRC_XRIGFlagLong = '-xrig'


########################################################################################
#
#      SPRCBlendBuild Cmd
#
########################################################################################
kPluginCmdBlendBuild = 'SPRCBlendBuild'


class SouthParkBlendBuild(OpenMayaMPx.MPxCommand):

    PRECISION = 3

    def __init__(self):
        OpenMayaMPx.MPxCommand.__init__(self)

    def parseArgs(self, kArguments):
        arg_data = OpenMaya.MArgParser(self.syntax(), kArguments)
        if arg_data.isFlagSet(SPRC_TravelModeFlag):
            self.travel_mode = arg_data.flagArgumentString(SPRC_TravelModeFlag, 0)
        elif arg_data.isFlagSet(SPRC_TravelModeFlagLong):
            self.travel_mode = arg_data.flagArgumentString(SPRC_TravelModeFlagLong, 0)
        else:
            self.travel_mode = TRAVEL_MODE.selected

        if arg_data.isFlagSet(SPRC_ChannelBoxFlag):
            self._channel = arg_data.flagArgumentBool(SPRC_ChannelBoxFlag, 0)
        elif arg_data.isFlagSet(SPRC_ChannelBoxFlagLong):
            self._channel = arg_data.flagArgumentBool(SPRC_ChannelBoxFlagLong, 0)
        else:
            self._channel = False

        if arg_data.isFlagSet(SPRC_FlagDataFile):
            self._file = arg_data.flagArgumentString(SPRC_FlagDataFile, 0)
        elif arg_data.isFlagSet(SPRC_DataFileFlagLong):
            self._file = arg_data.flagArgumentString(SPRC_DataFileFlagLong, 0)
        else:
            raise Exception('-f (-file) flag needed.')

        if arg_data.isFlagSet(SPRC_NamespaceFlag):
            self._namespace = arg_data.flagArgumentString(SPRC_NamespaceFlag, 0)
        elif arg_data.isFlagSet(SPRC_NamespaceFlagLong):
            self._namespace = arg_data.flagArgumentString(SPRC_NamespaceFlagLong, 0)
        else:
            self._namespace = None

        if arg_data.isFlagSet(SPRC_ApplyModeFlag):
            self.apply_mode = arg_data.flagArgumentString(SPRC_ApplyModeFlag, 0)
        elif arg_data.isFlagSet(SPRC_ApplyModeFlagLong):
            self.apply_mode = arg_data.flagArgumentString(SPRC_ApplyModeFlagLong, 0)
        else:
            self.apply_mode = POSE_APPLY_MODE.blend

        if arg_data.isFlagSet(SPRC_ModifyFlag):
            self._modify = arg_data.flagArgumentString(SPRC_ModifyFlag, 0)
        elif arg_data.isFlagSet(SPRC_ModifyFlagLong):
            self._modify = arg_data.flagArgumentString(SPRC_ModifyFlagLong, 0)
        else:
            self._modify = None

        if arg_data.isFlagSet(SPRC_XRIGFlag):
            self._context = arg_data.flagArgumentString(SPRC_XRIGFlag, 0)
            self._xrig = xrig_context(self._context)
        elif arg_data.isFlagSet(SPRC_XRIGFlagLong):
            self._context = arg_data.flagArgumentString(SPRC_XRIGFlagLong, 0)
            self._xrig = xrig_context(self._context)
        else:
            raise Exception('-x (-xrig) flag needed.')

    def parse(self):
        data = {}
        tree = et.parse(self._file)
        data_element = tree.getroot().find('Data')
        for nodeElement in data_element.getiterator('Node'):
            attr_dict = {}
            node_name = nodeElement.attrib['name']
            for attr_element in nodeElement.getiterator('Attr'):
                attr_name = attr_element.attrib['name']
                attr_dict[attr_name] = {}
                values = []
                for keyElement in attr_element.getiterator('Key'):
                    value = json.loads(keyElement.attrib['value'])
                    values.append(value)
                attr_dict[attr_name]['value'] = values
            data[node_name] = attr_dict
        return data

    def doIt(self, kArguments):
        self.redoIt(kArguments)

    def redoIt(self, kArguments):
        self.parseArgs(kArguments)

        global SPRC_POSE_MULTI_DYN_DATA
        SPRC_POSE_MULTI_DYN_DATA = {}

        if self._namespace is None:
            self._namespace = _namespace()
            if self._namespace is None:
                raise Exception('Select Objects.')

        scene_data = get_atomic_data(mode=self.travel_mode, channel_box=self._channel, context=self._context)
        # print ('SCENE DATA', scene_data)
        xml_data = self.parse()
        # print ('XML DATA', xml_data)

        selection_list = OpenMaya.MSelectionList()
        xml_nodes = xml_data.keys()
        for node_name, attr_dict in scene_data.iteritems():
            if self._modify == POSE_APPLY_MODIFY.normal:
                switch_name = node_name

            elif self._modify == POSE_APPLY_MODIFY.filter_l:
                if not self._xrig.is_lt_ctrl(node_name.split('|')[-1]):
                    continue
                switch_name = node_name

            elif self._modify == POSE_APPLY_MODIFY.filter_r:
                if not self._xrig.is_rt_ctrl(node_name.split('|')[-1]):
                    continue
                switch_name = node_name

            elif self._modify == POSE_APPLY_MODIFY.mirror_l:
                if self._xrig.is_rt_ctrl(node_name.split('|')[-1]):
                    switch_name = self._xrig.rt_to_lt(node_name)
                else:
                    switch_name = node_name

            elif self._modify == POSE_APPLY_MODIFY.mirror_r:
                if self._xrig.is_lt_ctrl(node_name.split('|')[-1]):
                    switch_name = self._xrig.lt_to_rt(node_name)
                else:
                    switch_name = node_name

            elif self._modify == POSE_APPLY_MODIFY.flip:
                switch_name = self._xrig.switch(node_name)

            else:
                raise Exception('Invalid Argument.')

            if switch_name not in xml_nodes:
                continue

            _name = '|'.join(self._namespace+n for n in node_name.split('|'))
            try:
                selection_list.add(_name)
            except:
                continue
            obj = OpenMaya.MObject()
            selection_list.getDependNode(0, obj)
            dag_node_fn = OpenMaya.MFnDagNode(obj)
            selection_list.clear()

            _attrs = xml_data[switch_name].keys()
            for attr_name, value in attr_dict.iteritems():
                if attr_name not in _attrs:
                    continue
                plug = dag_node_fn.findPlug(attr_name)
                if not plug.isKeyable():
                    continue
                if plug.isLocked():
                    continue
                if not plug.isFreeToChange(False, False) == OpenMaya.MPlug.kFreeToChange:
                    continue

                scene_value = value
                xml_value = xml_data[switch_name][attr_name]['value'][0][1]
                # print switch_name, node_name
                if not switch_name == node_name:
                    if self._xrig.is_ik_ctrl(switch_name.split('|')[-1]):
                        if self._xrig.is_ik_flip_attr(attr_name):
                            xml_value *= -1
                    elif self._xrig.is_fk_ctrl(switch_name.split('|')[-1]):
                        if self._xrig.is_translate_attr(attr_name):
                            xml_value *= -1
                    else:
                        if self._xrig.is_facial_flip_attr(attr_name):
                            xml_value *= -1

                else:
                    if self._modify == 'FLIP':
                        if self._xrig.is_md_ctrl(switch_name.split('|')[-1]):
                            if self._xrig.is_md_flip_attr(attr_name):
                                xml_value *= -1

                if self.apply_mode == POSE_APPLY_MODE.blend:
                    if round(xml_value, self.PRECISION) != round(scene_value, self.PRECISION):
                        dyn_value = (float(xml_value) - float(scene_value)) / 100
                        SPRC_POSE_MULTI_DYN_DATA[plug] = [scene_value, xml_value, dyn_value]

                elif self.apply_mode == POSE_APPLY_MODE.multiplier:
                    dyn_value = float(xml_value) / 100
                    SPRC_POSE_MULTI_DYN_DATA[plug] = [scene_value, xml_value, dyn_value]
                    
                else:
                    raise Exception('Invalid Mode(\n1.BLEND \n2.MULTIPLIER).')

    def isUndoable(self):
        return False


def blendBuildCmdCreator():
    return OpenMayaMPx.asMPxPtr(SouthParkBlendBuild())


def blendBuildSyntaxCreator():
    syntax = OpenMaya.MSyntax()
    syntax.addFlag(SPRC_TravelModeFlag, SPRC_TravelModeFlagLong, OpenMaya.MSyntax.kString)
    syntax.addFlag(SPRC_ChannelBoxFlag, SPRC_ChannelBoxFlagLong, OpenMaya.MSyntax.kBoolean)
    syntax.addFlag(SPRC_FlagDataFile, SPRC_DataFileFlagLong, OpenMaya.MSyntax.kString)
    syntax.addFlag(SPRC_NamespaceFlag, SPRC_NamespaceFlagLong, OpenMaya.MSyntax.kString)
    syntax.addFlag(SPRC_ApplyModeFlag, SPRC_ApplyModeFlagLong, OpenMaya.MSyntax.kString)
    syntax.addFlag(SPRC_ModifyFlag, SPRC_ModifyFlagLong, OpenMaya.MSyntax.kString)
    syntax.addFlag(SPRC_HelpFlag, SPRC_HelpFlagLong, OpenMaya.MSyntax.kString)
    syntax.addFlag(SPRC_XRIGFlag, SPRC_XRIGFlagLong, OpenMaya.MSyntax.kString)
    return syntax


########################################################################################
#
#        SPRCBlend Cmd
#
########################################################################################
kPluginCmdBlend = 'SPRCBlend'


class SouthParkBlend(OpenMayaMPx.MPxCommand):
    
    def __init__(self):
        OpenMayaMPx.MPxCommand.__init__(self)
        self.modifier = OpenMaya.MDGModifier()

    def parseArgs(self, kArguments):
        arg_data = OpenMaya.MArgParser(self.syntax(), kArguments)
        self.percent = arg_data.commandArgumentInt(0)

    def doIt(self, kArguments):
        self.parseArgs(kArguments)
        for plug, value_list in SPRC_POSE_MULTI_DYN_DATA.iteritems():
            v = value_list[0] + value_list[2] * self.percent
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
#        SPRCSelectControl Cmd
#
########################################################################################
kPluginCmdSelectByXml = 'SPRCSelectControl'


class SouthParkSelectControl(OpenMayaMPx.MPxCommand):
    
    def __init__(self):
        OpenMayaMPx.MPxCommand.__init__(self)
        self.bufferSelectionList = OpenMaya.MSelectionList()
        OpenMaya.MGlobal.getActiveSelectionList(self.bufferSelectionList)
        
    def parseArgs(self, kArguments):
        arg_data = OpenMaya.MArgParser(self.syntax(), kArguments)
        if arg_data.isFlagSet(SPRC_FlagDataFile):
            self.file = arg_data.flagArgumentString(SPRC_FlagDataFile, 0)
        elif arg_data.isFlagSet(SPRC_DataFileFlagLong):
            self.file = arg_data.flagArgumentString(SPRC_DataFileFlagLong, 0)
        else:
            raise Exception('-f (-file) flag needed.')

        if arg_data.isFlagSet(SPRC_NamespaceFlag):
            self.namespace = arg_data.flagArgumentString(SPRC_NamespaceFlag, 0)
        elif arg_data.isFlagSet(SPRC_NamespaceFlagLong):
            self.namespace = arg_data.flagArgumentString(SPRC_NamespaceFlagLong, 0)
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

        tree = et.parse(self.file)
        data_element = tree.getroot().find('Data')
        selection_list = OpenMaya.MSelectionList()
        for node_element in data_element.getiterator('Node'):
            node_name = node_element.attrib['name']
            _name = '|'.join(self.namespace+n for n in node_name.split('|'))
            try:
                selection_list.add(_name)
            except:
                continue
        OpenMaya.MGlobal.setActiveSelectionList(selection_list)

    def undoIt(self):
        OpenMaya.MGlobal.setActiveSelectionList(self.bufferSelectionList)

    def isUndoable(self):
        return True


def selectByXmlCmdCreator():
    return OpenMayaMPx.asMPxPtr(SouthParkSelectControl())


def selectByXmlSyntaxCreator():
    syntax = OpenMaya.MSyntax()
    syntax.addFlag(SPRC_FlagDataFile, SPRC_DataFileFlagLong, OpenMaya.MSyntax.kString)
    syntax.addFlag(SPRC_NamespaceFlag, SPRC_NamespaceFlagLong, OpenMaya.MSyntax.kString)
    return syntax


########################################################################################
#
#        SPRCCopyPose Cmd
#
########################################################################################
kPluginCmdCopyPose = 'SPRCCopyPose'


class SouthParkCopyPose(OpenMayaMPx.MPxCommand):
    
    def __init__(self):
        OpenMayaMPx.MPxCommand.__init__(self)

    def parseArgs(self, kArguments):
        arg_data = OpenMaya.MArgParser(self.syntax(), kArguments)
        if arg_data.isFlagSet(SPRC_TravelModeFlag):
            self.travel_mode = arg_data.flagArgumentString(SPRC_TravelModeFlag, 0)
        elif arg_data.isFlagSet(SPRC_TravelModeFlagLong):
            self.travel_mode = arg_data.flagArgumentString(SPRC_TravelModeFlagLong, 0)
        else:
            raise Exception('-m (-mode) flag needed.')

        if arg_data.isFlagSet(SPRC_ChannelBoxFlag):
            self.channelBox = arg_data.flagArgumentBool(SPRC_ChannelBoxFlag, 0)
        elif arg_data.isFlagSet(SPRC_ChannelBoxFlagLong):
            self.channelBox = arg_data.flagArgumentBool(SPRC_ChannelBoxFlagLong, 0)
        else:
            self.channelBox = False

        if arg_data.isFlagSet(SPRC_XRIGFlag):
            self._context = arg_data.flagArgumentString(SPRC_XRIGFlag, 0)
        elif arg_data.isFlagSet(SPRC_XRIGFlagLong):
            self._context = arg_data.flagArgumentString(SPRC_XRIGFlagLong, 0)
        else:
            raise Exception('-x (-xrig) flag needed.')

    def doIt(self, kArguments):
        self.redoIt(kArguments)

    def redoIt(self, kArguments):
        self.parseArgs(kArguments)
        global SPRC_POSE_CACHE_DATA
        SPRC_POSE_CACHE_DATA = get_atomic_data(
            mode=self.travel_mode, channel_box=self.channelBox, context=self._context
        )
        # print SPRC_POSE_CACHE_DATA

    def isUndoable(self):
        return False


def copyPoseCmdCreator():
    return OpenMayaMPx.asMPxPtr(SouthParkCopyPose())


def copyPoseSyntaxCreator():
    syntax = OpenMaya.MSyntax()
    syntax.addFlag(SPRC_TravelModeFlag, SPRC_TravelModeFlagLong, OpenMaya.MSyntax.kString)
    syntax.addFlag(SPRC_ChannelBoxFlag, SPRC_ChannelBoxFlagLong, OpenMaya.MSyntax.kBoolean)
    syntax.addFlag(SPRC_XRIGFlag, SPRC_XRIGFlagLong, OpenMaya.MSyntax.kString)
    return syntax


########################################################################################
#
#        SPRCPastePose Cmd
#
########################################################################################
kPluginCmdPastePose = 'SPRCPastePose'


class SouthParkPastePose(OpenMayaMPx.MPxCommand):
    
    def __init__(self):
        OpenMayaMPx.MPxCommand.__init__(self)
        self.modifier = OpenMaya.MDGModifier()

    def parseArgs(self, kArguments):
        arg_Data = OpenMaya.MArgParser(self.syntax(), kArguments)

        if arg_Data.isFlagSet(SPRC_TravelModeFlag):
            self.travel_mode = arg_Data.flagArgumentString(SPRC_TravelModeFlag, 0)
        elif arg_Data.isFlagSet(SPRC_TravelModeFlagLong):
            self.travel_mode = arg_Data.flagArgumentString(SPRC_TravelModeFlagLong, 0)
        else:
            raise Exception('-m (-mode) flag needed.')

        if arg_Data.isFlagSet(SPRC_NamespaceFlag):
            self.namespace = arg_Data.flagArgumentString(SPRC_NamespaceFlag, 0)
        elif arg_Data.isFlagSet(SPRC_NamespaceFlagLong):
            self.namespace = arg_Data.flagArgumentString(SPRC_NamespaceFlagLong, 0)
        else:
            self.namespace = None

        if arg_Data.isFlagSet(SPRC_XRIGFlag):
            self._context = arg_Data.flagArgumentString(SPRC_XRIGFlag, 0)
        elif arg_Data.isFlagSet(SPRC_XRIGFlagLong):
            self._context = arg_Data.flagArgumentString(SPRC_XRIGFlagLong, 0)
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

        global SPRC_POSE_CACHE_DATA
        nodes = []
        _nodes = _travel(mode=self.travel_mode, context=self._context) or []
        for _node in _nodes:
            tokens = OpenMaya.MFnDagNode(_node).partialPathName().split('|')
            nodes.append('|'.join([token.split(':')[-1] for token in tokens]))

        selection_list = OpenMaya.MSelectionList()
        for node_name, attr_dict in SPRC_POSE_CACHE_DATA.iteritems():
            if node_name not in nodes:
                continue
            _name = '|'.join(self.namespace+n for n in node_name.split('|'))
            selection_list.add(_name)
            obj = OpenMaya.MObject()
            selection_list.getDependNode(0, obj)
            dag_node_fn = OpenMaya.MFnDagNode(obj)
            selection_list.clear()

            for attrName, value in attr_dict.iteritems():
                plug = dag_node_fn.findPlug(attrName)
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
    syntax.addFlag(SPRC_TravelModeFlag, SPRC_TravelModeFlagLong, OpenMaya.MSyntax.kString)
    syntax.addFlag(SPRC_NamespaceFlag, SPRC_NamespaceFlagLong, OpenMaya.MSyntax.kString)
    syntax.addFlag(SPRC_XRIGFlag, SPRC_XRIGFlagLong, OpenMaya.MSyntax.kString)
    return syntax


########################################################################################
#
#        SPRCMirrorPose Cmd
#
########################################################################################
kPluginCmdMirrorPose = 'SPRCMirrorPose'


class SouthParkMirrorPose(OpenMayaMPx.MPxCommand):
    
    def __init__(self):
        OpenMayaMPx.MPxCommand.__init__(self)
        self.modifier = OpenMaya.MDGModifier()
        self.results = None

    def parseArgs(self, kArguments):
        arg_data = OpenMaya.MArgParser(self.syntax(), kArguments)

        if arg_data.isFlagSet(SPRC_XRIGFlag):
            self._context = arg_data.flagArgumentString(SPRC_XRIGFlag, 0)
            self._xrig = xrig_context(self._context)
        elif arg_data.isFlagSet(SPRC_XRIGFlagLong):
            self._context = arg_data.flagArgumentString(SPRC_XRIGFlagLong, 0)
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

        data = get_atomic_data(mode=TRAVEL_MODE.selected, channel_box=False, context=self._context)
        plane = mplane.get_mirror_plane(namespace)
        self.results = []
        selection_list = OpenMaya.MSelectionList()
        for node_name, attr_dict in data.iteritems():
            switch_name = self._xrig.switch(node_name)
            this_name = '|'.join(namespace+n for n in node_name.split('|'))
            that_name = '|'.join(namespace+n for n in switch_name.split('|'))

            try:
                selection_list.add(that_name)
            except:
                continue
            obj = OpenMaya.MObject()
            selection_list.getDependNode(0, obj)
            dag_node_fn = OpenMaya.MFnDagNode(obj)
            selection_list.clear()

            for attr_name, value in attr_dict.iteritems():
                if not dag_node_fn.hasAttribute(attr_name):
                    continue
                plug = dag_node_fn.findPlug(attr_name)
                if not plug.isKeyable():
                    continue
                if plug.isLocked():
                    continue
                if not plug.isFreeToChange(False, False) == OpenMaya.MPlug.kFreeToChange:
                    continue
                if switch_name == node_name:
                    aim_value = value
                    if self._xrig.is_wt_ctrl(switch_name.split('|')[-1]):
                        if self._xrig.is_translate_attr(attr_name):
                            continue
                        if self._xrig.is_rotate_attr(attr_name):
                            continue
                    if self._xrig.is_md_ctrl(switch_name.split('|')[-1]):
                        if self._xrig.is_md_flip_attr(attr_name):
                            aim_value *= -1
                else:
                    aim_value = value
                    if self._xrig.is_ik_ctrl(switch_name.split('|')[-1]) or \
                            self._xrig.is_pole_ctrl(node_name.split('|')[-1]):
                        if self._xrig.is_translate_attr(attr_name):
                            continue
                        if self._xrig.is_rotate_attr(attr_name):
                            continue

                    elif self._xrig.is_fk_ctrl(switch_name.split('|')[-1]):
                        if self._xrig.is_translate_attr(attr_name):
                            aim_value = value * -1

                    else:
                        if self._xrig.is_facial_flip_attr(attr_name):
                            aim_value = value * -1

                self.modifier.newPlugValueFloat(plug, aim_value)

            if self._xrig.is_ik_ctrl(node_name.split('|')[-1]) or \
                    self._xrig.is_pole_ctrl(node_name.split('|')[-1]) or \
                    self._xrig.is_wt_ctrl(node_name.split('|')[-1]):
                if plane is None:
                    continue
                result = mplane.magic_mirror(
                    src=this_name, dst=that_name, plane=plane,
                    active=False, space='world', context=self._context
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
    syntax.addFlag(SPRC_XRIGFlag, SPRC_XRIGFlagLong, OpenMaya.MSyntax.kString)
    return syntax


########################################################################################
#
#        SPRCFlipPose Cmd
#
########################################################################################
kPluginCmdFlipPose = 'SPRCFlipPose'


class SouthParkFlipPose(OpenMayaMPx.MPxCommand):
    
    def __init__(self):
        OpenMayaMPx.MPxCommand.__init__(self)
        self.modifier = OpenMaya.MDGModifier()
        self.results = None

    def parseArgs(self, kArguments):
        arg_data = OpenMaya.MArgParser(self.syntax(), kArguments)
        if arg_data.isFlagSet(SPRC_XRIGFlag):
            self._context = arg_data.flagArgumentString(SPRC_XRIGFlag, 0)
            self._xrig = xrig_context(self._context)
        elif arg_data.isFlagSet(SPRC_XRIGFlagLong):
            self._context = arg_data.flagArgumentString(SPRC_XRIGFlagLong, 0)
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
        data = get_atomic_data(mode=TRAVEL_MODE.selected, channel_box=False, context=self._context)
        plane = mplane.get_mirror_plane(namespace)

        selection_list = OpenMaya.MSelectionList()
        self.results = []
        for node_name, attr_dict in data.iteritems():
            selection_list.clear()
            switch_name = self._xrig.switch(node_name)

            this_name = '|'.join(namespace+n for n in node_name.split('|'))
            that_name = '|'.join(namespace+n for n in switch_name.split('|'))

            if this_name == that_name:
                if self._xrig.is_wt_ctrl(switch_name.split('|')[-1]):
                    if plane is None:
                        continue
                    this_results = mplane.magic_mirror(
                        src=this_name, dst=that_name, plane=plane,
                        active=False, space='world', context=self._context
                    )
                    this_results[0].setTranslation(this_results[1], OpenMaya.MSpace.kWorld)
                    this_results[0].setRotation(this_results[2], OpenMaya.MSpace.kWorld)
                    self.results.append([this_results, this_results])
                    continue
                elif self._xrig.is_md_ctrl(switch_name.split('|')[-1]):
                    try:
                        selection_list.add(this_name)
                    except:
                        continue
                    obj = OpenMaya.MObject()
                    selection_list.getDependNode(0, obj)
                    dag_node_fn = OpenMaya.MFnDagNode(obj)
                    for attrName, value in attr_dict.iteritems():
                        if not dag_node_fn.hasAttribute(attrName):
                            continue
                        plug = dag_node_fn.findPlug(attrName)
                        if not plug.isKeyable():
                            continue
                        if plug.isLocked():
                            continue
                        if not plug.isFreeToChange(False, False) == OpenMaya.MPlug.kFreeToChange:
                            continue
                        aim_value = plug.asFloat()
                        if self._xrig.is_md_flip_attr(attrName):
                            aim_value *= -1
                        self.modifier.newPlugValueFloat(plug, aim_value)
                    continue
                else:
                    continue

            try:
                selection_list.add(this_name)
                selection_list.add(that_name)
            except:
                continue

            this_obj = OpenMaya.MObject()
            that_obj = OpenMaya.MObject()
            selection_list.getDependNode(0, this_obj)
            selection_list.getDependNode(1, that_obj)

            this_dag_node_fn = OpenMaya.MFnDagNode(this_obj)
            that_dag_node_fn = OpenMaya.MFnDagNode(that_obj)

            for attr_name, value in attr_dict.iteritems():
                if not that_dag_node_fn.hasAttribute(attr_name):
                    continue

                this_plug = this_dag_node_fn.findPlug(attr_name)
                that_plug = that_dag_node_fn.findPlug(attr_name)

                if not that_plug.isKeyable():
                    continue
                if that_plug.isLocked():
                    continue
                if not that_plug.isFreeToChange(False, False) == OpenMaya.MPlug.kFreeToChange:
                    continue

                that_value = that_plug.asFloat()

                this_aim_value = that_value
                that_aim_value = value

                if self._xrig.is_ik_ctrl(node_name.split('|')[-1]) or \
                        self._xrig.is_pole_ctrl(node_name.split('|')[-1]):
                    if self._xrig.is_translate_attr(attr_name):
                        continue
                    if self._xrig.is_rotate_attr(attr_name):
                        continue
                elif self._xrig.is_fk_ctrl(node_name.split('|')[-1]):
                    if self._xrig.is_translate_attr(attr_name):
                        this_aim_value = that_value * -1
                        that_aim_value = value * -1
                else:
                    if self._xrig.is_facial_flip_attr(attr_name):
                        this_aim_value = that_value * -1
                        that_aim_value = value * -1
                                
                self.modifier.newPlugValueFloat(this_plug, this_aim_value)
                self.modifier.newPlugValueFloat(that_plug, that_aim_value)

            if self._xrig.is_ik_ctrl(node_name.split('|')[-1]) or self._xrig.is_pole_ctrl(node_name.split('|')[-1]):
                if plane is None:
                    continue
                this_results = mplane.magic_mirror(
                    src=this_name, dst=that_name, plane=plane, active=False, space='world', context=self._context
                )
                that_results = mplane.magic_mirror(
                    src=that_name, dst=this_name, plane=plane, active=False, space='world', context=self._context
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
    syntax.addFlag(SPRC_XRIGFlag, SPRC_XRIGFlagLong, OpenMaya.MSyntax.kString)
    return syntax


########################################################################################
#
#        SPRCMirrorSelect Cmd
#
########################################################################################
kPluginCmdMirrorSelect = 'SPRCMirrorSelect'


class SouthParkMirrorSelect(OpenMayaMPx.MPxCommand):
    
    def __init__(self):
        OpenMayaMPx.MPxCommand.__init__(self)
        self.bufferSelectionList = OpenMaya.MSelectionList()
        OpenMaya.MGlobal.getActiveSelectionList(self.bufferSelectionList)

    def parseArgs(self, kArguments):
        argData = OpenMaya.MArgParser(self.syntax(), kArguments)
        if argData.isFlagSet(SPRC_KeepFlag):
            self.keep = argData.flagArgumentBool(SPRC_KeepFlag, 0)
        elif argData.isFlagSet(SPRC_KeepFlagLong):
            self.keep = argData.flagArgumentBool(SPRC_KeepFlagLong, 0)
        else:
            self.keep = True

        if argData.isFlagSet(SPRC_XRIGFlag):
            self._context = argData.flagArgumentString(SPRC_XRIGFlag, 0)
            self._xrig = xrig_context(self._context)
        elif argData.isFlagSet(SPRC_XRIGFlagLong):
            self._context = argData.flagArgumentString(SPRC_XRIGFlagLong, 0)
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

        nodes = _travel(mode=TRAVEL_MODE.selected, context=self._context)
        selection_list = OpenMaya.MSelectionList()
        selection_list.clear()
        for node in nodes:
            dag_node_fn = OpenMaya.MFnDagNode(node)
            node_name = '|'.join([token.split(':')[-1] for token in dag_node_fn.partialPathName().split('|')])

            switch_name = self._xrig.switch(node_name)
            _name = '|'.join(namespace+n for n in switch_name.split('|'))
            if self.keep:
                selection_list.add(dag_node_fn.fullPathName(), False)
                
            try:
                selection_list.add(_name, False)
            except:
                continue

        OpenMaya.MGlobal.setActiveSelectionList(selection_list, OpenMaya.MGlobal.kReplaceList)

    def undoIt(self):
        OpenMaya.MGlobal.setActiveSelectionList(self.bufferSelectionList)

    def isUndoable(self):
        return True


def mirrorSelectCmdCreator():
    return OpenMayaMPx.asMPxPtr(SouthParkMirrorSelect())


def mirrorSelectSyntaxCreator():
    syntax = OpenMaya.MSyntax()
    syntax.addFlag(SPRC_KeepFlag, SPRC_KeepFlagLong, OpenMaya.MSyntax.kBoolean)
    syntax.addFlag(SPRC_XRIGFlag, SPRC_XRIGFlagLong, OpenMaya.MSyntax.kString)
    return syntax


########################################################################################
#
#        SPRCResetControl Cmd
#
########################################################################################
kPluginCmdReset = 'SPRCResetControl'


class SouthParkReset(OpenMayaMPx.MPxCommand):
    """
    reset objs' all keyable attr to default value
    """
    def __init__(self):
        OpenMayaMPx.MPxCommand.__init__(self)
        self.modifier = OpenMaya.MDGModifier()

    def parseArgs(self, kArguments):
        arg_data = OpenMaya.MArgParser(self.syntax(), kArguments)
        if arg_data.isFlagSet(SPRC_TravelModeFlag):
            self.travel_mode = arg_data.flagArgumentString(SPRC_TravelModeFlag, 0)
        elif arg_data.isFlagSet(SPRC_TravelModeFlagLong):
            self.travel_mode = arg_data.flagArgumentString(SPRC_TravelModeFlagLong, 0)
        else:
            self.travel_mode = TRAVEL_MODE.selected

        if arg_data.isFlagSet(SPRC_XRIGFlag):
            self._context = arg_data.flagArgumentString(SPRC_XRIGFlag, 0)
            self._xrig = xrig_context(self._context)
        elif arg_data.isFlagSet(SPRC_XRIGFlagLong):
            self._context = arg_data.flagArgumentString(SPRC_XRIGFlagLong, 0)
            self._xrig = xrig_context(self._context)
        else:
            raise Exception('-x (-xrig) flag needed.')

    def __reset(self, plug):
        script_util = OpenMaya.MScriptUtil()
        attr = plug.attribute()
        if attr.hasFn(OpenMaya.MFn.kUnitAttribute):
            attr_fn = OpenMaya.MFnUnitAttribute(attr)
            unit_type = attr_fn.unitType()

            if unit_type == OpenMaya.MFnUnitAttribute.kAngle or unit_type == OpenMaya.MFnUnitAttribute.kDistance:
                ptr = script_util.asDoublePtr()
                attr_fn.getDefault(ptr)
                value = script_util.getDouble(ptr)

                self.modifier.newPlugValueDouble(plug, value)

            elif unit_type == OpenMaya.MFnUnitAttribute.kTime:
                ptr = script_util.asDoublePtr()
                attr_fn.getDefault(ptr)
                value = script_util.getDouble(ptr)

                t = OpenMaya.MTime(value)
                self.modifier.newPlugValueMTime(plug, t)
            else:
                pass

        elif attr.hasFn(OpenMaya.MFn.kNumericAttribute):
            attr_fn = OpenMaya.MFnNumericAttribute(attr)
            unit_type = attr_fn.unitType()

            if unit_type == OpenMaya.MFnNumericData.kBoolean:
                ptr = script_util.asBoolPtr()
                attr_fn.getDefault(ptr)
                value = script_util.getBool(ptr)
                self.modifier.newPlugValueBool(plug, value)

            elif unit_type == OpenMaya.MFnNumericData.kByte or unit_type == OpenMaya.MFnNumericData.kChar:
                ptr = script_util.asCharPtr()
                attr_fn.getDefault(ptr)
                value = script_util.getChar(ptr)
                self.modifier.newPlugValueChar(plug, value)

            elif unit_type == OpenMaya.MFnNumericData.kShort:
                ptr = script_util.asShortPtr()
                attr_fn.getDefault(ptr)
                value = script_util.getShort(ptr)
                self.modifier.newPlugValueShort(plug, value)

            elif unit_type == OpenMaya.MFnNumericData.kLong:
                ptr = script_util.asIntPtr()
                attr_fn.getDefault(ptr)
                value = script_util.getInt(ptr)
                self.modifier.newPlugValueInt(plug, value)

            elif unit_type == OpenMaya.MFnNumericData.kFloat:
                ptr = script_util.asDoublePtr()
                attr_fn.getDefault(ptr)
                value = script_util.getDouble(ptr)
                self.modifier.newPlugValueFloat(plug, float(value))

            elif unit_type == OpenMaya.MFnNumericData.kDouble:
                ptr = script_util.asDoublePtr()
                attr_fn.getDefault(ptr)
                value = script_util.getDouble(ptr)
                self.modifier.newPlugValueDouble(plug, value)

            else:
                pass

        elif attr.hasFn(OpenMaya.MFn.kEnumAttribute):
            attr_fn = OpenMaya.MFnEnumAttribute(attr)
            ptr = script_util.asShortPtr()
            attr_fn.getDefault(ptr)
            value = script_util.getShort(ptr)

            self.modifier.newPlugValueShort(plug, value)

        else:
            pass
        
    def doIt(self, kArguments):
        self.parseArgs(kArguments)

        nodes = _travel(mode=self.travel_mode, context=self._context) or []
        if not len(nodes):
            return

        plug_array = OpenMaya.MPlugArray()
        selection_list = OpenMaya.MSelectionList()
        for node in nodes:
            plug_array.clear()
            selection_list.clear()
            selection_list.add(node)
            OpenMayaAnim.MAnimUtil.findAnimatablePlugs(selection_list, plug_array)

            for i in xrange(plug_array.length()):
                if not plug_array[i].isKeyable():
                    continue

                if plug_array[i].isLocked():
                    continue

                if not plug_array[i].isFreeToChange(False, False) == OpenMaya.MPlug.kFreeToChange:
                    continue

                link_plug_array = OpenMaya.MPlugArray()
                plug_array[i].connectedTo(link_plug_array, True, False)
                if link_plug_array.length():
                    connected_node = link_plug_array[0].node()

                    if (connected_node.hasFn(OpenMaya.MFn.kAnimCurveTimeToAngular) or
                        connected_node.hasFn(OpenMaya.MFn.kAnimCurveTimeToDistance) or
                        connected_node.hasFn(OpenMaya.MFn.kAnimCurveTimeToTime) or
                        connected_node.hasFn(OpenMaya.MFn.kAnimCurveTimeToUnitless)
                        ):
                        self.__reset(plug_array[i])

                    elif (connected_node.hasFn(OpenMaya.MFn.kAimConstraint) or
                          connected_node.hasFn(OpenMaya.MFn.kOrientConstraint) or
                          connected_node.hasFn(OpenMaya.MFn.kPointConstraint) or
                          connected_node.hasFn(OpenMaya.MFn.kParentConstraint) or
                          connected_node.hasFn(OpenMaya.MFn.kScaleConstraint) or
                          connected_node.hasFn(OpenMaya.MFn.kTangentConstraint) or
                          connected_node.hasFn(OpenMaya.MFn.kPoleVectorConstraint) or
                          connected_node.hasFn(OpenMaya.MFn.kSymmetryConstraint)
                          ):
                        """
                        do nothing, constrainted attr don't reset.
                        """
                        pass

                    else:
                        pass

                else:
                    self.__reset(plug_array[i])
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
    syntax.addFlag(SPRC_TravelModeFlag, SPRC_TravelModeFlagLong, OpenMaya.MSyntax.kString)
    syntax.addFlag(SPRC_XRIGFlag, SPRC_XRIGFlagLong, OpenMaya.MSyntax.kString)
    return syntax


########################################################################################
#
#    initializePlugin / un-initializePlugin
#
########################################################################################
def initializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject, 'astips', '1.0.0', 'Any')

    try:
        mplugin.registerCommand(kPluginCmdBlendBuild, blendBuildCmdCreator, blendBuildSyntaxCreator)
    except OSError:
        sys.stderr.write('Failed to register command: {0}'.format(kPluginCmdBlendBuild))
        raise Exception('Failed to register command: {0}'.format(kPluginCmdBlendBuild))

    try:
        mplugin.registerCommand(kPluginCmdBlend, blendCmdCreator, blendSyntaxCreator)
    except OSError:
        sys.stderr.write('Failed to register command: {0}'.format(kPluginCmdBlend))
        raise Exception('Failed to register command: {0}'.format(kPluginCmdBlend))

    try:
        mplugin.registerCommand(kPluginCmdSelectByXml, selectByXmlCmdCreator, selectByXmlSyntaxCreator)
    except OSError:
        sys.stderr.write('Failed to register command: {0}'.format(kPluginCmdSelectByXml))
        raise Exception('Failed to register command: {0}'.format(kPluginCmdSelectByXml))

    try:
        mplugin.registerCommand(kPluginCmdCopyPose, copyPoseCmdCreator, copyPoseSyntaxCreator)
    except OSError:
        sys.stderr.write('Failed to register command: {0}'.format(kPluginCmdCopyPose))
        raise Exception('Failed to register command: {0}'.format(kPluginCmdCopyPose))

    try:
        mplugin.registerCommand(kPluginCmdPastePose, pastePoseCmdCreator, pastePoseSyntaxCreator)
    except OSError:
        sys.stderr.write('Failed to register command: {0}'.format(kPluginCmdPastePose))
        raise Exception('Failed to register command: {0}'.format(kPluginCmdPastePose))

    try:
        mplugin.registerCommand(kPluginCmdMirrorPose, mirrorPoseCmdCreator, mirrorPoseSyntaxCreator)
    except OSError:
        sys.stderr.write('Failed to register command: {0}'.format(kPluginCmdMirrorPose))
        raise Exception('Failed to register command: {0}'.format(kPluginCmdMirrorPose))

    try:
        mplugin.registerCommand(kPluginCmdFlipPose, flipPoseCmdCreator, flipPoseSyntaxCreator)
    except OSError:
        sys.stderr.write('Failed to register command: {0}'.format(kPluginCmdFlipPose))
        raise Exception('Failed to register command: {0}'.format(kPluginCmdFlipPose))

    try:
        mplugin.registerCommand(kPluginCmdMirrorSelect, mirrorSelectCmdCreator, mirrorSelectSyntaxCreator)
    except OSError:
        sys.stderr.write('Failed to register command: {0}'.format(kPluginCmdMirrorSelect))
        raise Exception('Failed to register command: {0}'.format(kPluginCmdMirrorSelect))

    try:
        mplugin.registerCommand(kPluginCmdReset, resetCmdCreator, resetSyntaxCreator)
    except OSError:
        sys.stderr.write('Failed to register command: {0}'.format(kPluginCmdReset))
        raise Exception('Failed to register command: {0}'.format(kPluginCmdReset))


def uninitializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)

    try:
        mplugin.deregisterCommand(kPluginCmdBlendBuild)  
    except OSError:
        sys.stderr.write('Failed to un-register command: {0}'.format(kPluginCmdBlendBuild))
        raise Exception('Failed to un-register command: {0}'.format(kPluginCmdBlendBuild))

    try:
        mplugin.deregisterCommand(kPluginCmdBlend)
    except OSError:
        sys.stderr.write('Failed to un-register command: {0}'.format(kPluginCmdBlend))
        raise Exception('Failed to un-register command: {0}'.format(kPluginCmdBlend))

    try:
        mplugin.deregisterCommand(kPluginCmdSelectByXml)
    except OSError:
        sys.stderr.write('Failed to un-register command: {0}'.format(kPluginCmdSelectByXml))
        raise Exception('Failed to un-register command: {0}'.format(kPluginCmdSelectByXml))

    try:
        mplugin.deregisterCommand(kPluginCmdCopyPose)
    except OSError:
        sys.stderr.write('Failed to un-register command: {0}'.format(kPluginCmdCopyPose))
        raise Exception('Failed to un-register command: {0}'.format(kPluginCmdCopyPose))

    try:
        mplugin.deregisterCommand(kPluginCmdPastePose)
    except OSError:
        sys.stderr.write('Failed to un-register command: {0}'.format(kPluginCmdPastePose))
        raise Exception('Failed to un-register command: {0}'.format(kPluginCmdPastePose))

    try:
        mplugin.deregisterCommand(kPluginCmdMirrorPose)
    except OSError:
        sys.stderr.write('Failed to un-register command: {0}'.format(kPluginCmdMirrorPose))
        raise Exception('Failed to un-register command: {0}'.format(kPluginCmdMirrorPose))

    try:
        mplugin.deregisterCommand(kPluginCmdFlipPose)
    except OSError:
        sys.stderr.write('Failed to un-register command: {0}'.format(kPluginCmdFlipPose))
        raise Exception('Failed to un-register command: {0}'.format(kPluginCmdFlipPose))

    try:
        mplugin.deregisterCommand(kPluginCmdMirrorSelect)
    except OSError:
        sys.stderr.write('Failed to un-register command: {0}'.format(kPluginCmdMirrorSelect))
        raise Exception('Failed to un-register command: {0}'.format(kPluginCmdMirrorSelect))

    try:
        mplugin.deregisterCommand(kPluginCmdReset)
    except OSError:
        sys.stderr.write('Failed to un-register command: {0}'.format(kPluginCmdReset))
        raise Exception('Failed to un-register command: {0}'.format(kPluginCmdReset))
