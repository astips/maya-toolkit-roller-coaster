# -*- coding: utf-8 -*-

import pymel.core as pm


class SmartPanel(object):
    """
    usage :
        panel1 = pm.windows.getPanel(type='modelPanel')
        panel2 = pm.windows.getPanel(visiblePanels=True)
        panels = list(set(panel1).intersection(set(panel2)))

        sp = SmartPanel(panels)
        sp.record()
        sp.p_dict
        sp.player()
        sp.reback()
        sp.clean()
    """

    def __init__(self, panels):

        self.v_types = ['nc', 'ns', 'pm', 'sds', 'pl', 'lt', 'ca', 'j', 'ikh', 'df', 
                        'dy', 'fl', 'hs', 'fo', 'ncl', 'npa', 'nr', 'dc', 'lc', 'dim', 
                        'pv', 'ha', 'tx', 'str', 'motionTrails', 'm', 'clipGhosts', 
                        'cv', 'hu', 'gr', 'hud', 'imp', 'sel', 'ps']

        self.p_dict = {}
        self.panels = panels
        
    def record(self):
        self.p_dict = {}
        for panel in self.panels:
            v_dict = {}
            for v_type in self.v_types:
                cmd_str = "pm.windows.modelEditor(panel, q=True, {0}=True)".format(v_type)
                v_dict[v_type] = (eval(cmd_str))
            self.p_dict[panel] = v_dict

    def player(self):
        pm.windows.viewManip(v=False)
        for panel in self.panels:
            pm.windows.modelEditor(panel, e=True, alo=False, gr=False)
            pm.windows.modelEditor(panel, e=True, displayAppearance='smoothShaded', wos=False) 
            pm.windows.modelEditor(panel, e=True, ns=True, pm=True, sds=True, hud=True, imp=True)

    def clean(self):
        for panel in self.panels:
            pm.windows.modelEditor(panel, e=True, alo=False)

    def reback(self):
        for panel in self.panels:
            for v_type in self.v_types:
                cmd_str = "pm.windows.modelEditor(panel, e=True, {0}={1})".format(
                    v_type, str(self.p_dict[panel][v_type])
                )
                eval(cmd_str)
