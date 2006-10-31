#! /usr/bin/env python
# -*- coding: UTF8 -*-

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


import os,gtk,gobject
import cPickle as pickle
from lib_christine.libs_christine import *
from lib_christine.gtk_misc import *

(PATH,
NAME,
TYPE,
PIX,
ALBUM,
ARTIST,
TN,
SEARCH,
PLAY_COUNT,
TIME)=range(10)

(VPATH,
VNAME,
VPIX) = range(3)

class library(gtk_misc):
	def __init__(self,main):
		self.iters = {}
		gtk_misc.__init__(self)
		#self.player = player(self)
		self.player = play10(self)
		self.xml = glade_xml("treeview.glade","ltv")
		self.xml.signal_autoconnect(self)
		self.gconf = christine_gconf()
		self.main = main
		self.play = self.main.player
		self.tv = self.xml["ltv"]
		self.library_lib = lib_library("music")
		self.gen_model()
		filter = self.model.filter_new()
		sort = gtk.TreeModelSort(filter)
		self.tv.set_model(sort)
		self.add_columns()
		self.set_drag_n_drop()
		gobject.timeout_add(500,self.stream_length)
		
	
	def gen_model(self,refresh=False):
		print "lib_library.gen_model"
		self.tv.freeze_child_notify()
		if not refresh:
			s = gobject.TYPE_STRING
			self.model = gtk.ListStore(s,s,s,gtk.gdk.Pixbuf,
					s,s,s,s,int,s)
		else:
			self.model.clear()
		sounds = self.library_lib.get_sounds()
		soundpix = self.gen_pixbuf("sound.png")
		soundpix = soundpix.scale_simple(20,20,gtk.gdk.INTERP_BILINEAR)
		videopix = self.gen_pixbuf("video.png")
		videopix = videopix.scale_simple(20,20,gtk.gdk.INTERP_BILINEAR)
		keys = sounds.keys()
		keys.sort()
		limit = 20
		for i in keys:
			pix = self.gen_pixbuf("blank.png")
			pix = pix.scale_simple(20,20,gtk.gdk.INTERP_BILINEAR)
			#if len (sounds[i]["name"]) > limit:
			#	name = sounds[i]["name"][:limit-3]+"..."
			#	name = sounds[i]["name"]
			#else:
			name = sounds[i]["name"]
			#if len(sounds[i]["artist"]) > limit:
			#	artist = sounds[i]["artist"][:limit-3]+"..."
			#	artist = sounds[i]["artist"]
			#else:
			artist = sounds[i]["artist"]
			#	
			#if len(sounds[i]["album"]) > limit:
			#	album = sounds[i]["album"][:limit-3]+"..."
			album = sounds[i]["album"]
			#else:
			#	album = sounds[i]["album"]
			
			if not sounds[i].has_key("play_count"):
				sounds[i]["play_count"] = 0

			if not sounds[i].has_key("duration"):
				sounds[i]["duration"] = "00:00"

			self.model.set(self.model.append(),
					NAME,name,
					PATH,i,
					TYPE,sounds[i]["type"],
					PIX, pix,
					ALBUM,album,
					ARTIST,artist,
					TN,str(sounds[i]["track_number"]),
					SEARCH,",".join([name,album,artist]),
					PLAY_COUNT,sounds[i]["play_count"],
					TIME,sounds[i]["duration"])
		self.tv.freeze_child_notify()

	def add_columns(self):
		render = gtk.CellRendererText()
		tv = self.tv
		tvc = gtk.TreeViewColumn
		
		tn = tvc("Track",render,text=TN)
		tn.set_sort_column_id(TN)
		tn.set_visible(self.gconf.get_bool("ui/show_tn"))
		tv.append_column(tn)
	
		pix = gtk.CellRendererPixbuf()
		name = tvc("Title")
		name.set_sort_column_id(NAME)
		name.set_resizable(True)
		name.set_fixed_width(250)
		name.set_property("sizing",gtk.TREE_VIEW_COLUMN_FIXED)
		name.pack_start(pix,False)
		rtext = gtk.CellRendererText()
		name.pack_start(rtext,True)
		name.add_attribute(pix,"pixbuf",PIX)
		name.add_attribute(rtext,"text",NAME)
		tv.append_column(name)
		

		artist = tvc("Artist",render,text=ARTIST)
		artist.set_sort_column_id(ARTIST)
		artist.set_resizable(True)
		artist.set_fixed_width(150)
		artist.set_property("sizing",gtk.TREE_VIEW_COLUMN_FIXED)
		artist.set_visible(self.gconf.get_bool("ui/show_artist"))
		tv.append_column(artist)
		
		album = tvc("Album",render,text=ALBUM)
		album.set_sort_column_id(ALBUM)
		album.set_resizable(True)
		album.set_fixed_width(150)
		album.set_property("sizing",gtk.TREE_VIEW_COLUMN_FIXED)
		album.set_visible(self.gconf.get_bool("ui/show_album"))
		tv.append_column(album)
		
		type = tvc("Type",render,text=TYPE)
		type.set_sort_column_id(TYPE)
		type.set_resizable(True)
		type.set_visible(self.gconf.get_bool("ui/show_type"))
		tv.append_column(type)

		play = tvc("Count",render,text=PLAY_COUNT)
		play.set_sort_column_id(PLAY_COUNT)
		play.set_resizable(True)
		play.set_visible(self.gconf.get_bool("ui/show_play_count"))
		tv.append_column(play)

		length = tvc("Duration",render,text=TIME)
		length.set_sort_column_id(TIME)
		length.set_resizable(True)
		length.set_visible(self.gconf.get_bool("ui/duration"))
		tv.append_column(length)

		self.gconf.notify_add("/apps/christine/ui/show_artist",self.gconf.toggle_visible,artist)
		self.gconf.notify_add("/apps/christine/ui/show_album",self.gconf.toggle_visible,album)
		self.gconf.notify_add("/apps/christine/ui/show_type",self.gconf.toggle_visible,type)
		self.gconf.notify_add("/apps/christine/ui/show_tn",self.gconf.toggle_visible,tn)
		self.gconf.notify_add("/apps/christine/ui/show_play_count",self.gconf.toggle_visible,play)
		self.gconf.notify_add("/apps/christine/ui/duration",self.gconf.toggle_visible,length)
		self.discoverer = discoverer()
		self.discoverer.bus.add_watch(self.message_handler)

	def add(self,file,prepend=False):
		self.discoverer.set_location(file)
		gobject.timeout_add(100,self.stream_length)
		model = self.model
		if prepend:
			iter = model.prepend()
		else:
			iter = model.append()
		self.iters[file] = iter

	def message_handler(self,a,b):
		d = self.discoverer
		t = b.type
		if t == gst.MESSAGE_TAG:
			#print a,b,d.get_location(),self.model.get_path(self.iters[d.get_location()])
			self.discoverer.found_tags_cb(b.parse_tag())
			name	= d.get_tag("title")
			album	= d.get_tag("album")
			artist	= d.get_tag("artist")
			tn		= d.get_tag("track-number")
			#if name != "":
			#	del self.discoverer
			pix = self.gen_pixbuf("blank.png")
			pix = pix.scale_simple(20,20,gtk.gdk.INTERP_BILINEAR)
			if name == "":
				n = os.path.split(d.get_location())[1].split(".")
				name = ".".join([k for k in n[:-1]])
			model = self.model
			if d.get_tag("video-codec") != "" or \
					os.path.splitext(d.get_location())[1] in CHRISTINE_VIDEO_EXT:
				t = "video"
			else:
				t = "audio"
					
			model.set(self.iters[d.get_location()],
						NAME,name,
						PATH,d.get_location(),
						TYPE,t,
						PIX, pix,
						ALBUM,album,
						ARTIST,artist,
						TN,str(tn),
						SEARCH,",".join([name,album,artist]),
						PLAY_COUNT,0)
		return True

	def stream_length(self,widget=None):
		d = self.discoverer
		try: 
			if d.get_location().split(":")[0] == "http":
				return True
			total = d.query_duration(gst.FORMAT_TIME)[0]
			ts = self.total/gst.SECOND
			text = "%02d:%02d"%divmod(ts,60)
			self.model.set(self.iters[d.get_location()],
					TIME,text)
			return False
		except:
			return True

	def add1(self,file,prepend=False):
		name   = ""
		artist = ""
		album  = ""
		track_number = 0

		pix = self.gen_pixbuf("blank.png")
		pix = pix.scale_simple(20,20,gtk.gdk.INTERP_BILINEAR)

		if name == "":
			n = os.path.split(file)[1].split(".")
			name = ".".join([k for k in n[:-1]])
		model = self.model
		if prepend:
			iter = model.prepend()
		else:
			iter = model.append()
		model.set(iter,
					NAME,name,
					PATH,file,
					TYPE,"sound",
					PIX, pix,
					ALBUM,album,
					ARTIST,artist,
					TN,str(track_number),
					SEARCH,",".join([name,album,artist]))
		model.foreach(self.get_last_iter)
		self.iters.append([self.last_iter,file])

	def get_last_iter(self,model,path,iter):
		self.last_iter = iter
		
	def set_tags(self):
		if len(self.iters) > 0:
			iter,path = self.iters.pop()
			self.iter = iter
			self.discoverer.set_location(path)
			self.save()
		return True
			

	def remove(self,iter):
		key = self.model.get_value(iter,PATH)
		self.library_lib.remove(key)
		self.model.remove(iter)
	
	def save(self):
		'''
		Save the current library
		'''
		#self.library_lib.clear()
		self.model.foreach(self.prepare_for_disk)
		self.library_lib.save()
		
		
	def prepare_for_disk(self,model,path,iter):
		name,artist,album,track_number,path,type,pc,duration = model.get(iter,NAME,ARTIST,ALBUM,TN,PATH,TYPE,PLAY_COUNT,TIME)
		self.library_lib.append(path,{"name":name,
				"type":type,"artist":artist,
				"album":album,"track_number":track_number,
				"play_count":pc,
				"duration":duration})
		
	def item_activated(self,widget,path,iter):
		model = widget.get_model()
		iter = model.get_iter(path)
		filename = model.get_value(iter,PATH)
		self.main.set_location(filename)
		#self.main.player.playit()
		#self.main.STATE_PLAYING = True
		self.main.play_button.set_active(False)
		self.main.play_button.set_active(True)
		self.main.filename = filename

	def key_press_handler(self,treeview,event):
		if event.keyval == 65535:
			selection = treeview.get_selection()
			model,iter = selection.get_selected()
			name = model.get_value(iter,NAME)
			model.remove(iter)
			self.library_lib.remove(name)
			self.save()
			
	def set_drag_n_drop(self):
		 self.tv.connect("drag_motion",self.check_contexts)
		 self.tv.connect("drag_drop",self.dnd_handler)
		 self.tv.connect("drag_data_received",self.add_it)
		 self.tv.enable_model_drag_source(gtk.gdk.BUTTON1_MASK,
				 [('STRING',0,0)],gtk.gdk.ACTION_COPY)
		 self.tv.connect("drag-data-get",self.drag_data_get)
	
	def drag_data_get(self,treeview,context,selection,info,timestamp):
		tsel = treeview.get_selection()
		model,iter = tsel.get_selected()
		text = model.get_value(iter,PATH)
		selection.set("STRING",8,text)
		return
		
		 

	def check_contexts(self,treeview,context,selection,info,timestamp):
		context.drag_status(gtk.gdk.ACTION_COPY,timestamp)
		return True
	def dnd_handler(self,treeview,context,selection,info,timestamp,b=None,c=None):
		'''
		'''
		tgt = treeview.drag_dest_find_target(context,[("STRING",0,0)])
		data = treeview.drag_get_data(context,tgt)
		return True
	def add_it(self,treeview,context,x,y,selection,target,timestamp):
		treeview.emit_stop_by_name("drag_data_received")
		target = treeview.drag_dest_find_target(context,[("STRING",0,0)])
		if timestamp !=0:
			#print treeview,context,x,y,selection,target,timestamp
			text = self.parse_received_data(selection.get_text())
			#print text
			if len(text)>0:
				install_gui(text,self)
		return True

class queue(gtk_misc):
	def __init__(self,main):
		gtk_misc.__init__(self)
		self.main = main
		self.iters = {}
		self.discoverer = discoverer()
		self.discoverer.bus.add_watch(self.message_handler)
		self.library = lib_library("queue")
		self.xml = glade_xml("treeview_reorderable.glade","ltv")
		self.xml.signal_autoconnect(self)
		self.treeview = self.xml["ltv"]
		#self.treeview.set_reorderable(True)
		self.gen_model()
		self.treeview.set_model(self.model)
		self.add_columns()
		self.set_drag_n_drop()
	
		
	def gen_model(self,refresh=False):
		if refresh:
			self.model.clear()
		else:
			s = gobject.TYPE_STRING
			p = gtk.gdk.Pixbuf
			self.model = gtk.ListStore(s,s,s)
		keys = self.library.keys()
		print self.library.files
		keys.sort()
		for i in keys:
			print i, self.library[i]["name"]
			iter = self.model.append()
			self.model.set(iter,
					PATH,self.library[i]["path"],
					NAME,self.library[i]["name"],
					TYPE,self.library[i]["type"])
			
	def message_handler(self,a,b):
		d = self.discoverer
		t = b.type
		if t == gst.MESSAGE_TAG:
			#print a,b,d.get_location(),self.model.get_path(self.iters[d.get_location()])
			self.discoverer.found_tags_cb(b.parse_tag())
			name	= self.strip_xml_entities(d.get_tag("title"))
			album	= self.strip_xml_entities(d.get_tag("album"))
			artist	= self.strip_xml_entities(d.get_tag("artist"))
			tn		= d.get_tag("track-number")
			if name == "":
				n = os.path.split(self.file)[1].split(".")
				name = ".".join([k for k in n[:-1]])
			name = "<b><i>%s</i></b>"%name
			name = self.strip_xml_entities(name)
			if album !="":
				name += "\n from <i>%s</i>"%album
			if artist != "":
				name += "\n by <i>%s</i>"%artist

			model = self.model
			model.set(self.iters[d.get_location()],
			#model.set(self.iters,
						PATH,d.get_location(),
						NAME,name,
						TYPE,"sound")
			self.save()
		return True
	
	def add(self,file,prepend=False):
		print "queue.add(%s)"%file
		self.file = file
		self.discoverer.tags = {}
		if not os.path.isfile(file):
			return False
		self.discoverer.set_location(file)
		model = self.model
		if prepend:
			iter = model.prepend()
		else:
			iter = model.append()
		model.set(iter,
					PATH,file,
					NAME,"<b>%s</b>"%self.strip_xml_entities(os.path.split(file)[1]),
					TYPE,"sound")
		self.iters[file] = iter

	def add_columns(self):
		render = gtk.CellRendererText()
		tv = self.treeview
		pix = gtk.CellRendererPixbuf()
		icon = gtk.TreeViewColumn("",pix,pixbuf=PIX)
		icon.set_sort_column_id(TYPE)
		#tv.append_column(icon)
		name = gtk.TreeViewColumn("Queue",render,markup=NAME)
		name.set_sort_column_id(NAME)
		tv.append_column(name)

	def remove(self,iter):
		path = self.model.get_value(iter,PATH)
		self.model.remove(iter)
		self.library.files = {}
		self.save()
	
	def save(self):
		'''
		Save the current library
		'''
		print "save"
		self.pos = 0
		self.model.foreach(self.prepare_for_disk)
		self.library.save()
		
		
	def prepare_for_disk(self,model,path,iter):
		name = self.model.get_value(iter,NAME)
		path = self.model.get_value(iter,PATH)
		self.library.append(self.pos,{"path":path,"name":name,"type":"sound","extra":[]})
		self.pos += 1
		
	def item_activated(self,widget,path,iter):
		model = widget.get_model()
		iter = model.get_iter(path)
		filename = model.get_value(iter,PATH)
		self.main.set_location(filename)
		self.main.player.set_location(filename)
		self.main.play_button.set_active(False)
		self.main.play_button.set_active(True)
		self.main.filename = filename
	
	def key_press_handler(self,widget,event,key):
		print widget,event,key
	
	def set_drag_n_drop(self):
		return True
	### FIXME For some reason this thing doesn't work!!! ###
		self.treeview.drag_dest_set(gtk.DEST_DEFAULT_DROP,[("STRING",0,0),('GTK_TREE_MODEL_ROW',2,0)],0)
		self.treeview.connect("drag-motion",self.check_contexts)
		self.treeview.connect("drag-drop",self.dnd_handler)
		self.treeview.connect("drag-data-received",self.add_it)

	def check_contexts(self,treeview,context,selection,info,timestamp):
		context.drag_status(gtk.gdk.ACTION_COPY,timestamp)
		#print selection.get_text()
		return True

	def dnd_handler(self,treeview,context,selection,info,timestamp,b=None,c=None):
		'''
		'''
		tgt = treeview.drag_dest_find_target(context,[('STRING',0,0),('GTK_TREE_MODEL_ROW',2,0)])
		print treeview.drag_dest_get_target_list()
		data = treeview.drag_get_data(context,tgt)
		print locals(),context.get_data(tgt)
		return True
	
	def add_it(self,treeview,context,x,y,selection,target,timestamp):
		#print locals()
		treeview.emit_stop_by_name("drag_data_received")
		target = treeview.drag_dest_find_target(context,[("STRING",0,0)])
		if timestamp !=0:
			text = self.parse_received_data(selection.get_text())
			if len(text)>0:
				for i in text:
					print i
					#self.add(i)
		return True

	def parse_received_data(self,text):
		'''
		Parse the text and return a tuple with the text.
		'''
		result = []
		text = str(text)
		te = text.split("\n")
		for i in te:
			i = i.replace("\r"," ").strip()
			ext = i.split(".").pop()
			if ext in sound or \
					ext in video:
				result.append(i)
		return result
		

class mini_lists:
	def __init__(self,header,first_element):
		self.xml = glade_xml("treeview.glade","ltv")
		self.treeview = self.xml["ltv"]
		self.header = header
		self.first_element = first_element
		self.list = []
		self.text_to_search = ""
		self.gen_model()
		self.add_column()
		filter = self.model.filter_new()
		filter.set_visible_func(self.filter)
		self.treeview.set_model(filter)
		
	def gen_model(self,refresh=False):
		if refresh:
			self.model.clear()
		else:
			self.model = gtk.ListStore(gobject.TYPE_STRING,
					gobject.TYPE_STRING)
		self.add(self.first_element,"")
			
	def add(self,artist,parent=""):
		iter = self.model.append()
		self.model.set(iter,
				0,artist,
				1,parent)
		if not artist in self.list:
			self.list.append(artist)
		
	def add_column(self):
		artist = gtk.TreeViewColumn(self.header,
				gtk.CellRendererText(),
				text=0)
		self.treeview.append_column(artist)
		
	def filter(self,model,iter):
		value = model.get_value(iter,1)
		album = model.get_value(iter,0)
		if value == self.text_to_search \
				or self.text_to_search == "All Artists" \
				or album == "All Albums":
			return True
		else:
			return False
	
class sources(gtk_misc):
	def __init__(self):
		gtk_misc.__init__(self)
		self.xml = glade_xml("treeview.glade","ltv")
		self.treeview = self.xml["ltv"]
	
	def gen_model(self):
		self.model = gtk.ListStore(gtk.gdk.Pixbuf,str)
		
