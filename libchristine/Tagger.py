import os
import mutagen.mp3, mutagen.oggvorbis

class Track:
	def __init__(self, song):
	
		self.Song = song
		
		self.Title = ""
		self.Artist = ""
		self.Album = ""
		self.Track = "" 
		self.Genre = ""
		self.Length = ""
		self.Bitrate = ""		 
		
	def createDict(self):
		tags = {
				'title'   : self.Title,
				'artist'  : self.Artist,
				'album'   : self.Album,
				'track'   : self.Track,
				'genre'   : self.Genre,
				'length'  : self.Length,
				'bitrate' : self.Bitrate						 
			   }
		return tags
	
	

class MP3Track(Track):
	IDS = { "TIT2": "title",
			"TPE1": "artist",
			"TALB": "album",
			"TRCK": "track",
			"TDRC": "year",
			"TCON": "genre"
			}

	def __init__(self, *args):
		Track.__init__(self, *args)

	def getTag(self, id3, t):
		if not id3.has_key(t): return ""
		text = str(id3[t])

		text = text.replace("\n", " ").replace("\r", " ")
		return text

	def readTags(self):
		info = mutagen.mp3.MP3(self.Song)
		self.Length = info.info.length
		self.Bitrate = info.info.bitrate
		try:
			id3 = mutagen.id3.ID3(self.Song)
			self.Title = self.getTag(id3, "TIT2")
			self.Artist = self.getTag(id3, "TPE1")
			self.Album = self.getTag(id3, "TALB")
			self.Genre = self.getTag(id3, "TCON")

			try:
				# get track/disc id
				track = self.getTag(id3, "TRCK")
				if track.find('/') > -1:
					(self.Track, self.DiscId) = track.split('/')
					self.Track = int(self.Track)
					self.DiscId = int(self.DiscId)
				else:
					self.track = int(track)

			except ValueError:
				self.Track = -1
				self.DiscId = -1

			self.Year = self.getTag(id3, "TDRC")

		except:
			pass
		
		return self.createDict()



class OGGTrack(Track):
	def __init__(self, *args):
		Track.__init__(self, *args)

	def getTag(self, f, tag):
		try:
			return unicode(f[tag][0])
		except:
			return ""

	def readTags(self):
		try:
			f = mutagen.oggvorbis.OggVorbis(self.Song)
		except mutagen.oggvorbis.OggVorbisHeaderError:
			return

		self.Length = int(f.info.length)
		self.Bitrate = int(f.info.bitrate / 1024)

		self.Artist = self.getTag(f, "artist")
		self.Album = self.getTag(f, "album")
		self.Title = self.getTag(f, "title")
		self.Genre = self.getTag(f, "genre")
		self.Track = self.getTag(f, "tracknumber")
		self.DiscId = self.getTag(f, "tracktotal")
		self.Year = self.getTag(f, "date")
		
		return self.createDict()  

class FakeTrack(Track):
	def __init__(self, *args):
		Track.__init__(self, *args)

	def readTags(self):
		return self.createDict()


class Tagger:
	def __init__(self, song):
		self.Song = song
		if self.Song.split('.').pop().lower() == 'mp3':
			self.Rola = MP3Track(self.Song)
		elif self.Song.split('.').pop().lower() == 'ogg':
			self.Rola = OGGTrack(self.Song)
		else:
			self.Rola = FakeTrack(self.Song)

	def readTags(self):
		return self.Rola.readTags()
