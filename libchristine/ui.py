#! /usr/bin/env python
## Copyright (c) 2006 Marco Antonio Islas Cruz
## <markuz@islascruz.org>
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.


from libchristine.pattern.Singleton import Singleton
from libchristine.Logger import LoggerManager

class interface(Singleton):
    '''
    This class is a singleton storage for the interface instances.
    '''
    def __init__(self):
        self.empty = ''
        self.LoggerManager = LoggerManager()
        #Some attributes added:
        #coreClass, the main class (libchristine.Christine)
        self.coreClass = None
        #The player
        self.Player = None
        self.db = None
    
