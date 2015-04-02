#!/usr/bin/env python
import tweepy
#from our keys module (keys.py), import the keys dictionary
from keys import keys
from pprint import pprint
import time
import re
import urllib, time, sys, json
import os
import magic

CONSUMER_KEY = keys['consumer_key']
CONSUMER_SECRET = keys['consumer_secret']
ACCESS_TOKEN = keys['access_token']
ACCESS_TOKEN_SECRET = keys['access_token_secret']

api = None

def find_mentions(txt):
	""" find all the people mentioned in a tweet """
	mention_re = re.compile(r'@([A-Za-z0-9_]+)')
	return mention_re.findall(txt)

def grab_images_from_tweet(tweet):
	count = 0
	for media in tweet.extended_entities['media']:
		count += 1
		if media['type'] == 'photo':
			image_uri = media['media_url'] + ':large'
			print image_uri
			#filename = date + '-twitter.com_' + screen_name + '-' + status_id + '-' + str(count)
			#filepath = directory + '/' + filename
			filepath = "mybotsimages.jpg"
			# download image
			urllib.urlretrieve(image_uri, filepath)
			# identify mime type and attach extension
			# if os.path.exists(filepath):
			# 	mime = magic.from_file(filepath, mime=True)
			# 	if mime == "image/gif":
			# 		newfilepath = filepath + ".gif"
			# 	elif mime == "image/jpeg":
			# 		newfilepath = filepath + ".jpg"
			# 	elif mime == "image/png":
			# 		newfilepath = filepath + ".png"
			# 	else:
			# 		err = filepath + ": unrecgonized image type"
			# 		print_error(err)
			# 		continue
			# 	os.rename(filepath, newfilepath)
		else:
			# donwload failed for whatever reason
			err = filename + ": failed to download " + image_uri
			print_error(err)
			continue

def connect():
	global api
	print "Connecting to the twitter API"
	auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
	api = tweepy.API(auth)

def search():
	global api
	twts = api.search(q="Hello World!")
	#pprint(twts[0])
	print "*"*80
	#print twts[0].text
	for t in twts:
		pprint( t.text )
		print "- -" * 20

def mentions():
	mentions = api.mentions_timeline(count=1)
	if mentions:
		for m in mentions:
			print(m) # now print the mention
	else:
		print "No mentions yet"

def tweetforever():
	filename=open('lines.txt','r')
	f=filename.readlines()
	filename.close()

	for line in f:
		 api.update_status(status=line)
		 print line
		 time.sleep(3600) # Sleep for 1 hour

def main():
	connect()
	#tweetforever()
	#while 1:
	#search()
	#mentions()
	mentions = api.mentions_timeline()
	if mentions:
		#print "We have some mentions"
		for m in mentions:
			if m.extended_entities:
				grab_images_from_tweet(m)
	else:
		print "no mentions"

if __name__ == "__main__":
	main()
