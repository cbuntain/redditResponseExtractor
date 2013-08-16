#!/usr/bin/python

import sys
import csv
import pprint
import cPickle

import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import export_graphviz
from sklearn.externals.six import StringIO

def splitData(df, index, testSize=50):

	indexCopy = index[:]
	np.random.shuffle(indexCopy)

	trainingData = df.ix[indexCopy[:-testSize]]
	testingData = df.ix[indexCopy[-testSize:]]

	return (trainingData, testingData)

csvFilePath = sys.argv[1]

print "Reading from: ", csvFilePath

dataList = []
header = []
userIndex = []

with open(csvFilePath, 'r') as csvFile:
	csvObj = csv.reader(csvFile, delimiter=',')

	for headerStr in csvObj.next():
		header.append(headerStr.strip())

	for row in csvObj:

		# strippedRow = [x.strip() for x in row]
		strippedRow = []

		for i in range(len(row)):
			if ( i < 2 ):
				strippedRow.append(row[i].strip())
			else:
				strippedRow.append(float(row[i].strip()))

		dataList.append(strippedRow)
		userIndex.append("%s-%s"%(strippedRow[0], strippedRow[1]))

df = pd.DataFrame(dataList, columns=header, index=userIndex)

shuffledIndex = userIndex[:]
np.random.shuffle(shuffledIndex)

bestClassifier = {'classifier':None, 'score':0}
classifierList = []

featureList = [
	# 'neighbors', 
	'density', 
	'degreedist', 
	'neighborprop', 
	'tieprop', 
	'cluster', 
	'triangle'
]

for _ in range(100):
	(trainDf, testDf) = splitData(df, userIndex)

	trainLabels = trainDf['isanswer'].values
	trainData = trainDf[featureList]

	# classifier = RandomForestClassifier(
	# 	n_estimators=100,
	# 	max_features=None,
	# 	# verbose=2,
	# 	# compute_importances=True,
	# 	n_jobs=4,
	# 	random_state=0,
	# )
	classifier = DecisionTreeClassifier()
	classifier.fit(trainData, trainLabels)

	testLabels = testDf['isanswer'].values
	testData = testDf[featureList]

	score = classifier.score(testData, testLabels)

	if ( score > bestClassifier['score']):
		bestClassifier['score'] = score
		bestClassifier['classifier'] = classifier

	print score

	classifierList.append({'classifier':classifier, 'score':score})

print "Best score: ", bestClassifier['score']

with open("tree.dot", 'w') as f:
	f = export_graphviz(bestClassifier['classifier'], 
		out_file=f, 
		feature_names=featureList)


# save the classifier
with open('my_classifier.pkl', 'wb') as fid:
    cPickle.dump(bestClassifier['classifier'], fid)





