# -*- coding: utf-8 -*-

###########################################################################################
#
# Title: The South Park - Roller Coaster Dir
#
# Author: PLE
#
# Date: 2018.09
#
# Description: The South Park - Roller Coaster Dir Package
#
###########################################################################################
import os
import shutil
import tempfile


__all__ = [
    'ConfigDir',
    'TempDir'
]


MAINTAINER = '.ple'
SUBJECT = 'toolkit'


class ConfigDir(object):
    """
    Configure Dir.
    """
    def __init__(self, *args, **kwargs):
        home_dir = os.path.expanduser('~').replace('\\', '/')
        config_dir = os.path.join(home_dir, MAINTAINER, SUBJECT)
        self._path = os.path.join(config_dir, *args)
        if kwargs.get('clean', False):
            self.clean()
        if kwargs.get('makedirs', True):
            self.makedirs()

    def path(self):
        return self._path

    def clean(self):
        if os.path.exists(self.path()):
            shutil.rmtree(self.path())

    def makedirs(self):
        if not os.path.exists(self.path()):
            os.makedirs(self.path())


class TempDir(object):
    """
    Temp Dir.
    """
    def __init__(self, *args, **kwargs):
        tempdir = tempfile.gettempdir().replace('\\', '/')
        self._path = os.path.join(tempdir, *args).replace('\\', '/')
        if kwargs.get('clean', False):
            self.clean()
        if kwargs.get('makedirs', True):
            self.makedirs()

    def path(self):
        return self._path

    def clean(self):
        if os.path.exists(self.path()):
            shutil.rmtree(self.path())

    def makedirs(self):
        if not os.path.exists(self.path()):
            os.makedirs(self.path())
