#Created on 2/10/2018
#Author: Shantanu Mantri
#Class: Image Miner - Mines for Images, and returns a list of relevant images
#Code Credit goes to: https://github.com/hardikvasa/google-images-download/blob/master/google-images-download.py
#The follwoing code was inspired by and edited from the above repository/script
import urllib2
import simplejson
import cStringIO
import numpy
class ImageMiner:

	def __init__(self):
		self.keyword = ""
		self.images = []

	def reset(self):
		self.images = []
		self.keyword = ""

	def setKeyWord(self, word):
		self.keyword = word

	def getImageList(self):
		fetcher = urllib2.build_opener()
		startIndex = 0

		while(startIndex < 25):
			searchUrl = "http://ajax.googleapis.com/ajax/services/search/images?v=1.0&q=" + self.keyword + "&start=" + startIndex
			f = fetcher.open(searchUrl)
			deserialized_output = simplejson.load(f)

			#add images to image list
			for i in range(4):
				imageUrl = deserialized_output['responseData']['results'][i]['unescapedUrl']
				file = cStringIO.StringIO(urllib.urlopen(imageUrl).read())
				img = Image.open(file)
				images.append(img)

			#we want 100 images
			startIndex += 1
		return self.images


