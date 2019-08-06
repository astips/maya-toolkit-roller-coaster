# -*- coding: utf-8 -*-

import maya.cmds as cmds
import maya.mel as mel


def current():
    return cmds.currentTime(query=True)


def slider():
    return cmds.playbackOptions(q=True, min=True), cmds.playbackOptions(q=True, max=True)


def selected():
    play_slider = mel.eval('$tmpVar=$gPlayBackSlider')
    temp_range = cmds.timeControl(play_slider, q=True, rangeArray=True)
    return temp_range[0], temp_range[1]-1
