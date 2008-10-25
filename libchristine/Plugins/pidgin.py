#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of the Christine project
#
# Copyright (c) 2006-2007 Marco Antonio Islas Cruz
#
# Christine is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Christine is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301 USA
#
# @category  Multimedia
# @package   Christine
# @author    Maximiliano Valdez Gonzalez <garaged@gmail.com>
# @author    Marco Antonio Islas Cruz <markuz@islascruz.org>
# @copyright 2006-2008 Christine Development Group
# @license   http://www.gnu.org/licenses/gpl.txt

import dbus, gobject
from dbus.mainloop.glib import DBusGMainLoop
from libchristine.ui import interface
from libchristine.Plugins.plugin_base import plugin_base
from libchristine.Tagger import Tagger

class pidgin(plugin_base):
	"""
	Class to set pidgin's message, tests if pidgin and its dbus is accesible,
	and puts the current song played on the message
	"""
	def __init__(self):
		plugin_base.__init__(self)
		self.name = 'Pidgin'
		self.description = 'This plugin set the song you are playing on pidgin'
		self.obj = None
		self.interface = interface()
		self.christineConf.notifyAdd('backend/last_played', self.set_message)
		self.SessionStart()
		self.tagger = Tagger()

	def SetMessage(self,):
		file = self.christineConf.getString('backend/last_played')
		tags =  self.tagger.readTags(file)
		message = self.christineConf.getString('pidgin/message')
		if (not message):
			message = "Escuchando: %s - %s - en Christine"
			self.christineConf.setValue('pidgin/message', message)
		message = message % (tags['title'], tags['artist'])
		if ( self.obj is not None ):
			try:
				current = self.purple.PurpleSavedstatusGetType(
									self.purple.PurpleSavedstatusGetCurrent())
				status = self.purple.PurpleSavedstatusNew("", current)
				self.purple.PurpleSavedstatusSetMessage(status, message)
				self.purple.PurpleSavedstatusActivate(status)
			except:
				self.obj = None

	def SessionStart(self):
		dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
		session_bus = dbus.SessionBus()
		try:
			self.obj = session_bus.get_object("im.pidgin.purple.PurpleService",
											"/im/pidgin/purple/PurpleObject")
			self.purple = dbus.Interface(self.obj,
										"im.pidgin.purple.PurpleInterface")
		except:
			self.obj = None

	def set_message(self, *args):
		"""
		Convenient helper function to try the DBus connection if it's not
		already opened
		Could be done inside the self.SetMessage() but I don't
		like the idea, this is more flexible
		"""
		if ( self.obj is None and self.active):
			self.SessionStart()
		self.SetMessage()

	def get_active(self):
		return self.christineConf.getBool('pidgin/enabled')

	def set_active(self, value):
		return self.christineConf.setValue('pidgin/enabled', value)

	active = property(get_active, set_active, None,
					'Determine if the plugin is active or inactive')