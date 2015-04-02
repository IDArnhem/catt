#!/usr/bin/env python
import tweepy
#from our keys module (keys.py), import the keys to interact with Twitter
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

def get_my_followers():
	""" get screen names of all followers of this bot """
	followers = []
	for follower in tweepy.Cursor(api.followers).items():
		follower.follow()
		followers.append(follower.screen_name)

def grab_images_from_tweet(tweet):
	count = 0
	for media in tweet.extended_entities['media']:
		count += 1
		if media['type'] == 'photo':
			image_uri = media['media_url'] + ':large'
			print image_uri
			#filename = date + '-twitter.com_' + screen_name + '-' + status_id + '-' + str(count)
			#filepath = directory + '/' + filename
			filepath = "mybotsimages-{0}".format(tweet.id)
			# download image
			urllib.urlretrieve(image_uri, filepath)
			# identify mime type and attach extension
			if os.path.exists(filepath):
				mime = magic.from_file(filepath, mime=True)
				if mime == "image/gif":
					newfilepath = filepath + ".gif"
				elif mime == "image/jpeg":
					newfilepath = filepath + ".jpg"
				elif mime == "image/png":
					newfilepath = filepath + ".png"
				else:
					err = filepath + ": unrecognized image type"
					print_error(err)
					continue
				# rename with file extension
				os.rename(filepath, newfilepath)
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

def load_my_answers():
	global ANSWERS
	f=open('eightball.txt','r')
	ANSWERS=f.readlines()
	f.close()

def get_answer():
	return random.choice(ANSWERS)

## ###########################################################################
## main loops of the different bots
## ###########################################################################
def loop_icelandic_tweets():
	""" routine for Wido's bot """
	filename=open('icelandic.txt','r')
	f=filename.readlines()
	filename.close()

	#print "number of lines: ", len(f)
	#print f[:2]
	#print f[9]

	mn = 0
	mx = len(f)-1
	idx = randint(mn, mx)
	mytweet = f[idx]
	print mytweet

	mypic = "images/{0}.jpg".format( randint(0,696) ) # 696 is the number of images in the images directory
	print "posting image: ", mypic

	# tweet with image and geolocation coordinates
	api.update_with_media(filename=mypic, status=mytweet, lat=63.631050 , long=-19.607225)

def loop_image_grabber():
	""" main routine for Gabrielles bot """
	mentions = api.mentions_timeline()
	if mentions:
		#print "We have some mentions"
		for m in mentions:
			if m.extended_entities:
				grab_images_from_tweet(m)
	else:
		print "no mentions"

def loop_8ball_responder():
	""" main routine for Channin's bot """
	load_my_answers()

	while 1:
		try:
			mentions = api.mentions_timeline()
			if mentions:
				#print "We have been mentioned! "
				for m in mentions:
					# print "*"*80
					# print m.text
					# print "^"*80
					# print m.author.name
					# print "%"*80
					# print m.author.screen_name
					# print "@"*80
					# print "answer: ", get_answer()
					# print "@"*80

					# compose the tweet responding to the person that tweeted to us
					answer = "@{0} {1}".format(m.author.screen_name, get_answer())
					api.update_status(status=(answer)) #, m.id)
			else:
				print "we haven't been mentioned  :("
		except Exception, e:
			continue

		time.sleep(1)

def main():
	connect()
	#loop_icelandic_tweets() # wido
	#loop_image_grabber() # gabrielle
	loop_8ball_responder() # channin

if __name__ == "__main__":
	print("Press Ctrl+C to stop the bot...")
	try:
		main()
	except KeyboardInterrupt, e:
		pass

