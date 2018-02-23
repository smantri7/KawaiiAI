#Written by Shantanu Mantri on 2/23/2018
import nltk
from nltk.tokenize import word_tokenize
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import subjectivity
from nltk.sentiment import SentimentAnalyzer
from nltk.sentiment.util import *
import pickle

class SentimentLearner:

	def__init__(self):
		self.dict = {}
		self.model = None
		self.classifier = None

	def train_data(self, training_data):
		self.data = training_data
		self.dict = set(word.lower() for sentence in self.data for word in word_tokenize(sentence[0]))
		t = [({value: (value in word_tokenize(x[0])) for value in self.dict}, x[1]) for x in self.data]
		self.classifier = nltk.NaiveBayesClassifier.train(t)
		#save classifier model
		f = open("sentiment_classifier.pickle", 'wb')
		pickle.dump(self.classifier, f)
		f.close()

	def analyze(self, inp):
		#load classifier model
		f = open("sentiment_classifier.pickle", 'wb')
		self.classifier = pickle.load(f)
		ans = self.classifier.classify(inp)
		f.close()
		print(ans)
