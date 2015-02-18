#!/usr/bin/python
# -*- encoding: utf-8 -*-
import sys, os
import re
import time
import logging
import airport
import optparse
from OSC import *

HOST_ADDRESS = ('127.0.0.1', 23456)  # host, port tuple
verbose = False

def osc_send_ap(ssid, mac, rssi):
    """ Dispatch access point's details over OSC """
    global verbose
    tx = OSCClient()
    tx.connect( HOST_ADDRESS )
    msg = OSCMessage("/accespoint")
    msg.append(ssid)
    msg.append(mac)
    msg.append(rssi)

    if verbose:
        print msg
        #print "sending {0} {1} {2} {3}".format("/entropy", measurement, percentage, poolsize)

    tx.send( msg )
    tx.close()

def main(freq):
    # determine time to sleep from frequency
    wait = 1.0 / float(freq)
    try:
        while True:
            aps = airport.scan()
            # send all found APs
            for ap in aps:
                osc_send_ap(ap['SSID'], ap['MAC'], ap['RSSI'])
            # sleep for some time
            print("sleeping for {0}".format(wait))
            time.sleep(wait)
    except KeyboardInterrupt, e:
        print("Goodbye.")



if __name__ == '__main__':
    logging.getLogger().handlers = []
    logging.basicConfig(level=logging.DEBUG)

    option_parser_class = optparse.OptionParser

    parser = option_parser_class(description='Create a broadcasting node that speaks OSC to communicate with the heart sensor network.')

    parser.add_option('-v','--verbose', 
        action='store_true',
        dest="verbose",
        default=False, 
        help='verbose printing [default:%i]'% False)

    parser.add_option('-d','--desthost', 
        action='store',
        type="string", 
        dest="host",
        default="127.0.0.1", 
        help='the ip address of the application that has to receive the OSC messages [default:%s]'% "127.0.0.1")

    parser.add_option('-t','--hostport', 
        type=int, 
        action='store',
        dest="port",
        default=2222, 
        help='the port on which the application that has to receive the OSC messages will listen [default:%i]'% 2222 )

    parser.add_option('-f','--frequency', 
        type=int, 
        action='store',
        dest="frequency",
        default=4, 
        help='how many times per second shall we check [default:%s]'% 4)

    (options,args) = parser.parse_args()

    verbose = options.verbose
    HOST_ADDRESS = ( options.host, options.port )

    print("Running at frequency {0}".format(options.frequency))
    main(options.frequency)
