# -*- coding: utf-8 -*-

import maya.cmds as cmds
import maya.mel as mel
from ...core.preset import PresetManager


preset = PresetManager()
preset.load()


def create_menu():
    if cmds.popupMenu('RollerCoasterPopupMenu', q=True, exists=True):
        cmds.deleteUI('RollerCoasterPopupMenu')

    menu = cmds.popupMenu(
        'RollerCoasterPopupMenu', button=1, ctl=False, alt=False, sh=False,
        parent=mel.eval("findPanelPopupParent"), mm=True
    )

    def new_menu_item(parent=None, label='', command='', sub_menu=False,
                      option_box=False, enable_command_repeat=False, **kwargs):

        menu_item = cmds.menuItem(
            parent=parent, label=label, command=command,
            subMenu=sub_menu, tearOff=False, optionBox=option_box, enable=True, data=0,
            enableCommandRepeat=enable_command_repeat, boldFont=False, sourceType='python', **kwargs
        )
        return menu_item

    new_menu_item(
        label='Copy  Pose', radialPosition='N', parent=menu,
        command='from rollercoaster.main import sprc_menu;sprc_menu.copy_pose();'
    )
    new_menu_item(
        label='Paste  Pose', radialPosition='S', parent=menu,
        command='from rollercoaster.main import sprc_menu;sprc_menu.paste_pose();'
    )
    new_menu_item(
        label='Mirror  Pose', radialPosition='NE', parent=menu,
        command='from rollercoaster.main import sprc_menu;sprc_menu.mirror_pose();'
    )
    new_menu_item(
        label='Flip  Pose', radialPosition='SE', parent=menu,
        command='from rollercoaster.main import sprc_menu;sprc_menu.flip_pose();'
    )
    new_menu_item(
        label='Mirror  Select', radialPosition='NW', parent=menu,
        command='from rollercoaster.main import sprc_menu;sprc_menu.mirror_select();'
    )
    new_menu_item(
        label='Flip  Select', radialPosition='SW', parent=menu,
        command='from rollercoaster.main import sprc_menu;sprc_menu.flip_select();'
    )
    new_menu_item(
        label='Reset', parent=menu, command='from rollercoaster.main import sprc_menu;sprc_menu.reset();'
    )
    new_menu_item(divider=True, parent=menu)
    menu_item_copy_clip = new_menu_item(label='Copy  Clip',  parent=menu, sub_menu=True)
    new_menu_item(
        label='Selected',  parent=menu_item_copy_clip,
        command='from rollercoaster.main import sprc_menu;sprc_menu.copy_animation("SELECTED");'
    )
    new_menu_item(divider=True, parent=menu_item_copy_clip)
    new_menu_item(
        label='Recursive',  parent=menu_item_copy_clip,
        command='from rollercoaster.main import sprc_menu;sprc_menu.copy_animation("RECURSIVE");'
    )
    menu_item_paste_clip = new_menu_item(label='Paste  Clip', parent=menu, sub_menu=True)
    new_menu_item(
        label='Selected', parent=menu_item_paste_clip,
        command='from rollercoaster.main import sprc_menu;sprc_menu.paste_animation("SELECTED");'
    )
    new_menu_item(divider=True, parent=menu_item_paste_clip)
    new_menu_item(
        label='Recursive', parent=menu_item_paste_clip,
        command='from rollercoaster.main import sprc_menu;sprc_menu.paste_animation("RECURSIVE");'
    )
    new_menu_item(divider=True, parent=menu)
    new_menu_item(
        label='Save  Pose', parent=menu,
        command='from rollercoaster.main import run_creator;run_creator("pose");'
    )
    new_menu_item(
        label='Save  Motion  Clip', parent=menu,
        command='from rollercoaster.main import run_creator;run_creator("clip");'
    )
    new_menu_item(divider=True, parent=menu)
    menu_item_context = new_menu_item(label='Set  X-RIG  Context',  parent=menu, sub_menu=True)
    for xrig in preset.tool['context']:
        new_menu_item(divider=True, parent=menu_item_context)
        new_menu_item(
            label=xrig.upper(), parent=menu_item_context,
            command='from rollercoaster.main import sprc_menu;sprc_menu.context(\"{0}\");'.format(xrig)
        )
        

def delete_menu():
    if cmds.popupMenu('RollerCoasterPopupMenu', q=True, exists=True):
        items = cmds.popupMenu('RollerCoasterPopupMenu', q=True, itemArray=True)
        for item in items:
            cmds.deleteUI(item)
        cmds.deleteUI('RollerCoasterPopupMenu')
