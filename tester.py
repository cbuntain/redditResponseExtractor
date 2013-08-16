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

classifierPath = sys.argv[1]
csvFilePath = sys.argv[2]

print "Using classifer: ", classifierPath
print "Will classify data in: ", csvFilePath

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

classifier = None

with open(classifierPath, 'rb') as fid:
    classifier = cPickle.load(fid)

featureList = [
	# 'neighbors', 
	'density', 
	'degreedist', 
	'neighborprop', 
	'tieprop', 
	'cluster', 
	'triangle'
]

testData = df[featureList]

predictedLabels = classifier.predict(testData)

print testData
print predictedLabels

print "------"

testData['isanswer'] = predictedLabels
print testData






