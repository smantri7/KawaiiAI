#Image Learner for the chatbot. Maps images to concepts
import numpy as np
import re
from sklearn import svm, metrics
from skimage import io, feature, filters, exposure, color
from sklearn.externals import joblib

class ImageLearner:

	def __init__(self, label, images):
		self.model = self.getModel()
		self.labels = np.array([label for i in range(100)])
		self.images = images

		#TODO Implement a variety of classifiers and pick the images for the best one. This changes based on image
		#self.classifiers = []

		#self.classifier = KnowledgeBase.getOptimalClassifier(image)


	def preprocess(self):
		processed = []

		for image in self.images:
			img = filters.gaussian(image, sigma=0.4)
			f = feature.hog(img, orientations=10, pixels_per_cell=(48, 48), cells_per_block=(4 ,4), feature_vector=True, block_norm="L2-Hys")
			processed.append(f)

		return processed

	def train(self, object):
		train_data = self.preprocess()
		#train a variety of classifiers
		self.classifier = svm.LinearSVC()
		self.classifer.fit(train_data, self.labels)

    def predict_labels(self, data):
        predicted_labels = self.classifer.predict(data)
        return predicted_labels

	def updateModel(self):
		joblib.dump(self.classifier, self.label + '.pkl') 

	def getModel(self):
		try:
			self.classifier = joblib.load('classifier.pkl')
		except:
			self.classifier = None
