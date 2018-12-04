# -*- coding: utf-8 -*-

import maya.cmds as cmds


def set_hotkey(key, name=None, command='', release_name=None, release_command='', ctrl=False, alt=False):
    if cmds.runTimeCommand("{0}_runtime_cmd".format(name), query=True, exists=True):
        cmds.runTimeCommand("{0}_runtime_cmd".format(name), edit=True, delete=True)

    if cmds.runTimeCommand("{0}_runtime_cmd".format(release_name), query=True, exists=True):
        cmds.runTimeCommand("{0}_runtime_cmd".format(release_name), edit=True, delete=True)

    if name:
        press_runtime_cmd = cmds.runTimeCommand("{0}_runtime_cmd".format(name),
                                                annotation="{0}_runtime_cmd".format(name),
                                                command=command,
                                                commandLanguage="python")

        name_cmd = cmds.nameCommand("{0}_name_cmd".format(name),
                                    annotation="{0}_name_cmd".format(name),
                                    command=press_runtime_cmd)

        cmds.hotkey(keyShortcut=key, ctrlModifier=ctrl, altModifier=alt, name=name_cmd)

    if release_name:
        release_runtime_cmd = cmds.runTimeCommand("{0}_runtime_cmd".format(release_name),
                                                  annotation="{0}_runtime_cmd".format(release_name),
                                                  command=release_command,
                                                  commandLanguage="python")

        release_name_cmd = cmds.nameCommand("{0}_name_cmd".format(release_name),
                                            annotation="{0}_name_cmd".format(release_name),
                                            command=release_runtime_cmd)

        cmds.hotkey(keyShortcut=key, ctrlModifier=ctrl, altModifier=alt, releaseName=release_name_cmd)

    cmds.hotkey(autoSave=True)


def current_set(name):
    if not cmds.hotkeySet(name, q=True, exists=True):
        cmds.hotkeySet(name, current=True)
    cmds.hotkeySet(name, e=True, current=True)


def delete_set(name):
    if cmds.hotkeySet(name, q=True, exists=True):
        cmds.hotkeySet(name, e=True, delete=True)
    cmds.hotkeySet('Maya_Default', e=True, current=True)


"""
class SmartHotKey(object):
    
    def current_set(self, name):
        if not cmds.hotkeySet(name, q=True, exists=True):
            cmds.hotkeySet(name, current=True)
        cmds.hotkeySet(name, e=True, current=True)

    def delete_set(self, name):
        if cmds.hotkeySet(name, q=True, exists=True):
            cmds.hotkeySet(name, e=True, delete=True)
        cmds.hotkeySet('Maya_Default', e=True, current=True)

    def set_hotkey(self, key, name=None, command='', release_name=None, release_command='', ctrl=False, alt=False):
        if cmds.runTimeCommand("{0}_runtime_cmd".format(name), query=True, exists=True):
            cmds.runTimeCommand("{0}_runtime_cmd".format(name), edit=True, delete=True)

        if cmds.runTimeCommand("{0}_runtime_cmd".format(release_name), query=True, exists=True):
            cmds.runTimeCommand("{0}_runtime_cmd".format(release_name), edit=True, delete=True)

        if name:
            press_runtime_cmd = cmds.runTimeCommand("{0}_runtime_cmd".format(name),
                                                    annotation="{0}_runtime_cmd".format(name),
                                                    command=command,
                                                    commandLanguage="python")

            name_cmd = cmds.nameCommand("{0}_name_cmd".format(name),
                                        annotation="{0}_name_cmd".format(name),
                                        command=press_runtime_cmd)

            cmds.hotkey(keyShortcut=key, ctrlModifier=ctrl, altModifier=alt, name=name_cmd)

        if release_name:
            release_runtime_cmd = cmds.runTimeCommand("{0}_runtime_cmd".format(release_name),
                                                      annotation="{0}_runtime_cmd".format(release_name),
                                                      command=release_command,
                                                      commandLanguage="python")

            release_name_cmd = cmds.nameCommand("{0}_name_cmd".format(release_name),
                                                annotation="{0}_name_cmd".format(release_name),
                                                command=release_runtime_cmd)

            cmds.hotkey(keyShortcut=key, ctrlModifier=ctrl, altModifier=alt, releaseName=release_name_cmd)

        cmds.hotkey(autoSave=True)
"""