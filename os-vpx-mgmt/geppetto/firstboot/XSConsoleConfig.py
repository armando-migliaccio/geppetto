# Copyright (c) 2007-2009 Citrix Systems Inc.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 2 only.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import os
import sys


class Config:
    instance = None

    def __init__(self):
        self.colours = {
            'fg_dark': (400, 400, 360),
            'fg_normal': (600, 600, 550),
            'fg_bright': (999, 999, 800),
            'bg_dark': (0, 0, 0),
            'bg_normal': (0, 168, 325),
            'bg_bright': (0, 200, 400),
        }

        self.ftpname = 'XenServer Support'
        self.ftpserver = 'ftp://support.xensource.com/bugreports'

    @classmethod
    def Inst(cls):
        if cls.instance is None:
            cls.instance = Config()
        return cls.instance

    @classmethod
    def Mutate(cls, inConfig):
        cls.instance = inConfig

    def Colour(self, inName):
        return self.colours[inName]

    def FTPName(self):
        return self.ftpname

    def FTPServer(self):
        return self.ftpserver

    def BrandingMap(self):
        return {}

    def AllShellsTimeout(self):
        return True

    def DisplaySerialNumber(self):
        return True

    def DisplayAssetTag(self):
        return True

    def BMCName(self):
        return 'BMC'

    def FirstBootEULAs(self):
        return ['/EULA']


if os.path.isfile(sys.path[0] + '/XSConsoleConfigOEM.py'):
    import XSConsoleConfigOEM
