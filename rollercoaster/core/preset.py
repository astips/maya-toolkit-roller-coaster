# -*- coding: utf-8 -*-

import os
import json
from .dirs import ConfigDir
from rollercoaster import __toolset__, __name__


class PresetManager(object):

    PRESET_FILE_NAME = 'presets.json'

    def __init__(self):
        user_preset_path = ConfigDir(__toolset__, __name__, 'presets').path()
        self.user_preset_file = os.path.join(user_preset_path, self.PRESET_FILE_NAME)
        self.tool_preset_file = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), self.PRESET_FILE_NAME
        )
        self.user = None
        self.tool = None

    def load_tool_preset(self):
        with open(self.tool_preset_file, 'rb') as f:
            self.tool = json.load(f) or {}

    def load_user_preset(self):
        try:
            with open(self.user_preset_file, 'rb') as f:
                self.user = json.load(f) or {}
        except:
            self.user = {}

    def load(self):
        self.load_tool_preset()
        self.load_user_preset()

    def dump(self):
        with open(self.user_preset_file, 'wb') as f:
            f.write(json.dumps(self.user, ensure_ascii=True, indent=4))

    def reset(self):
        if not os.path.exists(self.user_preset_file):
            return
        try:
            os.remove(self.user_preset_file)
        except Exception as e:
            print e
