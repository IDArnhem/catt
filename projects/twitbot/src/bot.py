#!/usr/bin/env python
import tweepy
#from our keys module (keys.py), import the keys dictionary
from keys import keys
from pprint import pprint
import time

CONSUMER_KEY = keys['consumer_key']
CONSUMER_SECRET = keys['consumer_secret']
ACCESS_TOKEN = keys['access_token']
ACCESS_TOKEN_SECRET = keys['access_token_secret']

api = None

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
	 	print "---------------------------------"

def mentions():
	mentions = api.mentions_timeline(count=1)
	if mentions:
		for m in mentions:
			print(m)
	else:
		print "No mentions yet"

def tweetforever():
	filename=open('lines.txt','r')
	f=filename.readlines()
	filename.close()

	for line in f:
	     api.update_status(status=line)
	     #api.update_with_media(filename="images/mypic.jpg", status=line)
	     print line
	     time.sleep(3600) # Sleep for 1 hour

def main():
	connect()
	while 1:
		search()
	#mentions()

if __name__ == "__main__":
	main()
