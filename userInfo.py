#!/usr/bin/python

import praw
from pprint import pprint
import networkx as nx

# try:
#     import matplotlib.pyplot as plt
# except:
#     raise


def extractPosts(graph, redditObj, user, l=10):

	author = redditObj.get_redditor(user)

	print author

	print "Subreddits: "

	authorSubmissions = author.get_submitted(limit=500)
	subList = {}
	counter = 0

	for submission in authorSubmissions:
		counter+=1
		thisSubreddit = submission.subreddit.display_name

		if ( not thisSubreddit in subList.keys() ):
			subList[thisSubreddit] = 1
		else:
			subList[thisSubreddit] += 1

	sorted_subList = sorted(subList, key=subList.get)

	for subreddit in sorted_subList:
		print "\t", subreddit, subList[subreddit]

	print "Total Submissions: ", counter

	authorComments = author.get_comments(sort="top",limit=1000)
	subList = {}

	print "Subreddit Comments:"

	commentCount = 0
	for comment in authorComments:
		commentCount+=1
		thisSubreddit = comment.subreddit.display_name

		if ( not thisSubreddit in subList.keys() ):
			subList[thisSubreddit] = 1
		else:
			subList[thisSubreddit] += 1

	sorted_subList = sorted(subList, key=subList.get)

	for subreddit in sorted_subList:
		print "\t", subreddit, subList[subreddit]

	print "Total Comments: ", commentCount

	print "Replies: "

	commentCount = 0
	for comment in authorComments:
		if ( comment.is_root ):
			submission = comment.submission
			print "\t", submission.author
		else:
			parent = redditObj.get_info(thing_id=comment.parent_id)
			print "\t", parent.author
		commentCount+=1

	print "\tComment count:", commentCount

replyGraph = nx.DiGraph()

password = raw_input('Password:')

r = praw.Reddit(user_agent='edu.umd.cs.inst633o.cbuntain')
r.login('proteius',password)

userList = [
'MCMXCII'
]

try:
	for user in userList:
		print "Checking on user: /u/", user

		extractPosts(replyGraph, r, user, 25)

except Exception, e:
	print "Failed during execution: ", e

#finally:
	# nx.write_gexf(replyGraph, 'cs_users.gexf')







