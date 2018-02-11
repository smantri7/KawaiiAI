#Created on 2/10/2018
#Author: Shantanu Mantri
#Class: Frame - A frame holds data, forms connections (using relavance indicators), stores key information about an object
class Frame: 

	#title - the name of the object. e.g. frame relating to apples would have title apple
	#attributes - a dictionary that stores a string : data mapping. e.g. "red" : [pixel value]
	#connections - a dictionary that stores relevance indicator (0.0 - 1.0) : [list of relevant objects (string)]
	def __init__(self, title, attributes, connections):
		self.title = title
		self.attributes = attributes
		self.connections = connections

	#returns the name of the frame
	def getTitle(self):
		return self.title

	#returns a list of all the attributes of the frame
	def getAttributes(self): 
		return self.attributes

	#returns a specific attribute of the frame
	def getAttributeByName(self, name):
		return self.attributes[name]

	#returns a list of all the connections in the frame
	def getConnections(self):
		return self.connections

	#returns a specific connection in the frame
	def getConnectionByName(self, name):
		return self.connections[name]

	#adds a connection to the frame
	def addConnection(self, name, value):
		if name not in list(self.connections.keys()):
			self.connections[name] = value

	#adds an attribute to the frame
	def addAttribute(self, name, value):
		if name not in list(self.attributes.keys()):
			self.attributes[name] = value


