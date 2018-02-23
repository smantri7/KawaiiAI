#Written by Shantanu Mantri 2/23/2018
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sklearn.metrics import accuracy_score
from learners import SentimentLearner

class SentimentAnalyzer:

	def __init__(self, use_learner, data):
		self.model = None
		self.learn = use_learner
		if use_learner:
			self.model = SentimentLeaner()
		else:
			self.model = SentimentIntensityAnalyzer()

	def analyze(self):
		return self.model.classify(data) if self.learn else self.model.polarity_scores(data)






