# -*- coding: utf-8 -*-

import os


__name__ = 'RollerCoaster'
__version__ = '1.1.2'
__author__ = 'astips'
__package__ = 'rollercoaster'
__build__ = 'Cython 0.29, build on December 13, 2018'

os.environ['PATH'] += os.pathsep + os.path.join(os.path.dirname(__file__), 'bin')
