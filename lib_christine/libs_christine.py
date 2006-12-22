#! /usr/bin/env python
# -*- coding: UTF-8 -*-

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


#import pygst; pygst.require("0.10")
import os,gtk,gobject
import cPickle as pickle
#import gst
#import gst.interfaces

from lib_christine.gtk_misc import *
from lib_christine.gst_base import *

class sanity:
	'''
		Make all the sanity checks
	'''
	def __init__(self):
		self.__check_christine_dir()
		self.__check_sources_dir()

	def __check_christine_dir(self):
		if not os.path.exists(wdir):
			os.mkdir(wdir)
		else:
			if os.path.isfile(wdir):
				os.unlink(wdir)
				self.__check_christine_dir()
	def __check_sources_dir(self):
		sdir = os.path.join(wdir,"sources")
		if not os.path.exists(sdir):
			os.mkdir (sdir)
		else:
			if os.path.isfile(sdir):
				os.unlink(sdir)
				self.__check_sources_dir()


class lib_library(object):
	def __init__(self,list):
		sanity()
		if os.path.exists(os.path.join(wdir,list)):
			f =	open(os.path.join(wdir,list),"r")
			self.__files = pickle.load(f)
			f.close()
		else:
			self.__files = {}
		self.list = list

	def __setitem__(self,name,path):
		self.append(name,path)

	def __getitem__(self,key):
		return self.__files[key]
		
	def append(self,name,data):
		if type(data) != type({}):
			raise TypeError, "data must be a dict, got %s"%type(data)
		self.__files[name]=data

	def keys(self):
		return self.__files.keys()
	
	def save(self):
		f = open(wdir+self.list,"w")
		pickle.dump(self.__files,f)
		f.close()

	def clear(self):
		self.__files.clear()
	
	def remove(self,key):
		c = {}
		if key in self.keys():
			for i in self.keys():
				if i != key:
					c[i]= self.__files[i]
			self.__files = c.copy()
			#print "%s removed"%key
		else:
			#print "key %s not found"%key
			pass
	
	def get_type(self,file):
		ext = file.split(".").pop()
		if ext in sound:
			return "sound"
		if ext in video:
			return "video"
	
	def get_sounds(self):
		a = {}
		for i in self.keys():
			if self.__files[i]["type"] == "audio":
				a[i] = self.__files[i]
		return a

	def get_videos(self):
		a = {}
		for i in self.keys():
			if self.__files[i]["type"] == "video":
				a[i] = self.__files[i]
		return a
