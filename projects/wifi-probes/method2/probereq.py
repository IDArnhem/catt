#!/usr/bin/env python
##
## (cc) Luis Rodil-Fernandez <root@derfunke.net>
## DISCLAIMER: Tested on OSX Yosemite only, likely to blow up your computer if using anything else.
## 
## Simplest wifi probe sniffer I could come up with.
## 
## It keeps a list of found devices and serve's that list 
## in JSON format to any incoming requests.
##
## It's slow to react to drops because it has to run a 
## full channel-hopping (at 8 secs per channel) before
## it drops a mac address that has gone out of scope.
##
import re
import pickle
from threading import Timer, Thread
import subprocess
from subprocess import call
from itertools import *
import os.path
import time
import sys, random
import pprint

channels = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
hopTime = 8

airportcmd = '/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport'

exitNow = False
hopper = None
chnr = 0
currentLoop = 0

devices = {}


def prepare_device(device='en0'):
	""" prepares wifi device before going into monitor mode """
	call(['networksetup', '-setairportpower', device, 'on'])
	call(['sudo', airportcmd, '--disassociate'])

def release_device(device='en0'):
	""" """
	call(['networksetup','-setairportpower', device, 'off'])

def channel_hopper():
	global exitNow, chnr, currentLoop
	while not exitNow:
		print('hopping to channel ' + str(channels[chnr]))
		call(['sudo', airportcmd, '--channel=' + str(channels[chnr])])
		chnr = chnr + 1
		if chnr == len(channels):
			chnr = 0
			currentLoop += 1
		time.sleep(hopTime)

def is_mac_address(chunk):
	if 'SA:' in chunk:
		return True
	else:
		return False

def sniff(device='en0'):
	""" start tcpdump to sniff network packets """
	return subprocess.Popen(('sudo', 'tcpdump', '-i', device, '-l', '-e', '-I', 'type mgt subtype probe-req'), stdout=subprocess.PIPE)


## #################################################################################
## webserver stuff
## #################################################################################
import json
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn
import threading

PORT_NUMBER = 8080
server = None


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""
    pass

class SuperSimpleHandler(BaseHTTPRequestHandler):
	""" serve the list of devices captured as a json string """
	def do_GET(self):
		global devices
		self.send_response(200)
		self.send_header('Content-type','text/json')
		self.send_header('Access-Control-Allow-Origin', '*')
		self.end_headers()
		content = json.dumps(devices)
		self.wfile.write(content)
		return
	def log_message(self, format, *args):
		""" silence logging """
		return

def main():
	global exitNow, hopper, currentLoop, devices

	# start http server
	server = ThreadedHTTPServer(('0.0.0.0', PORT_NUMBER), SuperSimpleHandler)
	print "Started httpserver on port " , PORT_NUMBER
	threading.Thread(target=server.serve_forever).start()

	print "Preparing wifi device for capture"

	prepare_device()

	# start the channel hopper
	hopper = Thread(target=channel_hopper)
	hopper.start()

	# run tcpdump to capture probe requests from nearby devices
	p = sniff()
	try:
		# parse command output
		for row in p.stdout:
			result = row.decode('utf-8')
			if 'Probe Request' in result:
				chunks = result.split()
				try:
					sidx = chunks.index('signal')
					rssi   = chunks[sidx-1]
					mac    = [x for x in chunks if is_mac_address(x)][0]
					ssid   = chunks[chunks.index('Request')+1]
					mac 	= mac[3:] # get rif of the 'SA:' prefix
					#print "mac:", mac, "ssid:", ssid, "rssi:", rssi
					
					if mac not in devices:
						devices[mac] = {} # create subdict
					
					devices[mac]['detected'] = time.time()  # seconds since epoch
					devices[mac]['ssid'] = ssid
					devices[mac]['rssi'] = rssi
					devices[mac]['loop'] = currentLoop
					pprint.pprint(devices)
				except (ValueError, IndexError) as e:
					print "oh baby's got the hiccups!"
					continue
	except KeyboardInterrupt:
		global exitNow
		print '^C received, shutting down the web server'
		exitNow = True
		server.socket.close()
		time.sleep(1)
		p.terminate()
		release_device()

if __name__=="__main__":
    main()

