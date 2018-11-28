# -*- coding: utf-8 -*-

import pymel.core as pm


class SmartDisplayColor(object):
    """
    recorder & reback display color
    """
    def __init__(self):
        self.default = None

    def record(self):
        """
        record default display color
        """
        self.default = [
            pm.general.displayRGBColor('background', q=True),
            pm.general.displayRGBColor('backgroundTop', q=True),
            pm.general.displayRGBColor('backgroundBottom', q=True)
        ]

    def recovery(self):
        """
        set back to default display color
        """
        try:
            pm.general.displayRGBColor('background', self.default[0][0], self.default[0][1], self.default[0][2])
            pm.general.displayRGBColor('backgroundTop', self.default[1][0], self.default[1][1], self.default[1][2])
            pm.general.displayRGBColor('backgroundBottom', self.default[2][0], self.default[2][1], self.default[2][2])
        except:
            pass

    def color(self, color=None):
        """
        set new display color
        """
        try:
            pm.general.displayRGBColor('background', color[0], color[1], color[2])
            pm.general.displayRGBColor('backgroundTop', color[0], color[1], color[2])
            pm.general.displayRGBColor('backgroundBottom', color[0], color[1], color[2])
        except:
            pass
