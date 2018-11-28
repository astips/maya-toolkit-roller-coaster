# -*- coding: utf-8 -*-

import pymel.core as pm


class SmartHud(object):
    """
    recorder & reback model panel's hud setting
    """
    def __init__(self):
        self.defaults = pm.windows.headsUpDisplay(listHeadsUpDisplays=True) or []
        self.defaults_v = []
        self.users = []

    def record(self):
        """
        record default hud 's vis status
        """
        self.defaults_v = []
        for each in self.defaults:
            try:
                self.defaults_v.append(pm.windows.headsUpDisplay(each, q=True, vis=True))
            except:
                self.defaults_v.append(False)

    def clean(self):
        """
        hide defaults' hud
        hide view cube
        """
        pm.windows.viewManip(v=False)
        for item in self.defaults:
            try:
                pm.windows.headsUpDisplay(item, e=True, vis=False)
            except:
                pass

    def create(self, n='', s=0, **kwargs):
        """
        create a new user hud    
        """
        pm.windows.headsUpDisplay(n, s=s, b=pm.windows.headsUpDisplay(nfb=s), **kwargs)
        self.users.append(n)
        
    def hide(self):
        """
        hide user 's hud
        """
        for hud in self.users:
            pm.windows.headsUpDisplay(hud, e=True, vis=False)
            
    def smart_hide(self):
        """
        hide user 's hud by smart way
        """
        huds = pm.windows.headsUpDisplay(listHeadsUpDisplays=True)
        for hud in huds:
            if hud not in self.defaults:
                pm.windows.headsUpDisplay(hud, e=True, vis=False)
            
    def show(self):
        """
        show user 's hud
        """
        for hud in self.users:
            pm.windows.headsUpDisplay(hud, e=True, vis=True)
            
    def smart_show(self):
        """
        show user 's hud by smart way
        """
        huds = pm.windows.headsUpDisplay(listHeadsUpDisplays=True)
        for hud in huds:
            if hud not in self.defaults:
                pm.windows.headsUpDisplay(hud, e=True, vis=True)
                    
    def remove(self):
        """
        remove user 's hud
        """
        for hud in self.users:
            try:
                pm.windows.headsUpDisplay(hud, remove=True)
            except:
                pass
        self.users = []

    def smart_remove(self):
        """
        remove other user 's hud (which created by other tool)
        """
        pm.windows.viewManip(v=False)
        huds = pm.windows.headsUpDisplay(listHeadsUpDisplays=True)

        for hud in huds:
            if hud not in self.defaults:
                try:
                    pm.windows.headsUpDisplay(hud, remove=True)
                except:
                    pass

    def recovery(self):
        """
        remove all user 's hud
        set default 's hud to record status
        """
        self.remove()
        for i in range(len(self.defaults)):
            try:
                pm.windows.headsUpDisplay(self.defaults[i], e=True, vis=self.defaults_v[i])
            except:
                pass

    def color(self, colors=None):
        """
        color the hud 's label & value
        parameter :
            colors=[int, int] # default is [16, 17]
        """
        if not colors:
            colors = [16, 17]
        try:
            pm.general.displayColor('headsUpDisplayLabels', colors[0], dormant=True)
            pm.general.displayColor('headsUpDisplayValues', colors[1], dormant=True)
        except:
            pass
            
    def ruin(self):
        """
        remove all (both default & user)'s hud
        hide the view cube 
        """
        pm.windows.viewManip(v=False)
        huds = pm.windows.headsUpDisplay(listHeadsUpDisplays=True)
        for hud in huds:
            pm.windows.headsUpDisplay(hud, remove=True)
        self.defaults = []
        self.defaults_v = []
        self.users = []
