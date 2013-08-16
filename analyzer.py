#!/usr/bin/python

from operator import itemgetter
import matplotlib.pyplot as plt
import networkx as nx
import math
import sys

def neighborDegreeDist(ego):

	cutoff = 4

	degreeList = ego.degree()
	lowDegreeList = filter(lambda key: degreeList[key] < cutoff, degreeList.keys())

	s = len(lowDegreeList)
	b = len(degreeList) - s - 1

	return math.log(float(s+1)/float(b+1))

def lowDegreeNeighborProp(ego, center):

	successors = ego.successors(center)

	if ( len(successors) == 0 ):
		return 0

	cutoff = 2

	lowDegreeList = filter(lambda key: len(ego.successors(key)) < cutoff, successors)

	proportion = float(len(lowDegreeList)) / float(len(successors))

	# print "\t\t Low degree: ", len(lowDegreeList)
	# print "\t\t High degree: ", len(successors)

	return proportion

def intenseTieProp(ego, center):

	successors = ego.successors(center)

	if ( len(successors) == 0 ):
		return 0

	intenseCounter = 0
	for suc in successors:

		edge = ego[center][suc]

		if ( edge['weight'] > 1 ):

			intenseCounter += 1

	return float(intenseCounter) / float(len(successors))

def triangleRatio(g, center):

	triangleCoef = nx.triangles(g, nodes=[center])[center]

	deg = len(g.neighbors(center))

	maxTriangles = float(deg*(deg-1))/2.0

	return float(triangleCoef)/maxTriangles

graphPathes = [
# 'AskScienceDiscussion',
# 'askmen',
# 'askscience',
# 'askwomen',
# 'compsci',
# 'desmoines',
# 'iama',
# 'machinelearning',
# 'movies',
# 'mylittlepony',
# 'personalfinance',
# 'washingtondc',
'explainlikeimfive'
]

# outFile = open('data.csv', 'w')

# outFile.write("user, subreddit, neighbors, density, degreedist, neighborprop, tieprop, cluster, triangle, isanswer\n")

for graphPath in graphPathes:
	# graphPath = sys.argv[1]

	print "Reading Graph: ", graphPath

	graphObj = nx.read_gexf("%s.gexf" % graphPath)

	doubleFiltered = filter(lambda key: len(graphObj.successors(key)) >= 20, graphObj.nodes())

	print "Interesting Node Count: ", len(doubleFiltered)

	for key in doubleFiltered:
		
		egoGraph = nx.ego_graph(graphObj, key, undirected=True, distance=None)
		egoGraphUni = egoGraph.to_undirected()

		clusteringCoef = nx.clustering(egoGraphUni, nodes=[key])[key]

		# print key, len(graphObj.successors(key))
		# print "\t Density: ", nx.density(egoGraph)
		# print "\t Neighbor Degree Distribution: ", neighborDegreeDist(egoGraph)
		# print "\t Low Degree Neighbor Distribution: ", lowDegreeNeighborProp(egoGraph, key)
		# print "\t Intense Tie Prop: ", intenseTieProp(egoGraph, key)
		# print "\t Clustering Coefficient: ", clusteringCoef
		# print "\t Triangles: ", triangleRatio(egoGraphUni, key)

		dataLine = "%s, %s, %d, %f, %f, %f, %f, %f, %f, %d\n" % (key, 
			graphPath,
			len(graphObj.successors(key)),
			nx.density(egoGraph),
			neighborDegreeDist(egoGraph),
			lowDegreeNeighborProp(egoGraph, key),
			intenseTieProp(egoGraph, key),
			clusteringCoef,
			triangleRatio(egoGraphUni, key),
			0
			)

		# outFile.write(dataLine)
		print dataLine

	# # Draw graph
	# pos=nx.spring_layout(egoGraph)
	# nx.draw(egoGraph,pos,node_color='b',node_size=50,with_labels=False)

	# # Draw ego as large and red
	# nx.draw_networkx_nodes(egoGraph,pos,nodelist=[curiousityNodeLabel],node_size=300,node_color='r')
	# plt.savefig('ego_graph.png')
	# plt.show()