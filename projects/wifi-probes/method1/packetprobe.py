#!/usr/bin/env python
import argparse
from multiprocessing import Process
import subprocess
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *
import signal
import threading
import os, platform

WLAN_PROBE_REQUEST_TYPE=0
WLAN_PROBE_REQUEST_SUBTYPE=4

channel_hop_proc = None
stop_sniff = False

# set platform flags
IS_WIN = True if platform.system() == "Windows" else False
IS_OSX = True if platform.system() == "Darwin" else False
IS_LNX = True if platform.system() == "Linux" else False

def monitor_mode(interface):
    """ set the capture interface in monitor mode """
    if IS_OSX:
        subprocess.call( "networksetup -setairportpower {0} on".format(interface).split() )
        subprocess.call( "sudo airport --disassociate".split() )
    elif IS_LNX:
        pass

def change_channel(interface, chan):
    """ change wifi channel for interface (supports linux and osx) """
    print("Hopping to channel {0}".format(chan))
    if IS_LNX:
        os.system("iwconfig {0} channel {1}".format(interface, chan) )
    elif IS_OSX:
        subprocess.call( "sudo airport --channel={0}".format(chan).split() )

# Channel hopper - This code is very similar to that found in airoscapy.py (http://www.thesprawl.org/projects/airoscapy/)
def channel_hopper(interface):
    """ implement channel hopping """
    while True:
        try:
            channel = random.randrange(1,14)
            change_channel(interface, channel)
            time.sleep(1)
        except KeyboardInterrupt:
            break
 
def stop_channel_hop(signal, frame):
    # set the stop_sniff variable to True to stop the sniffer
    global stop_sniff, channel_hop_proc
    stop_sniff = True
    time.sleep(.5)
    channel_hop_proc.terminate()
    channel_hop_proc.join()

def keep_sniffing(pckt):
    global stop_sniff
    return stop_sniff

def handle_packet(pkt):
    if pkt.haslayer(Dot11):
        print(pkt)
        if pkt.type in (WLAN_PROBE_REQUEST_TYPE, WLAN_PROBE_REQUEST_SUBTYPE):
            print_packet(pkt)

def print_packet(pkt):
    print "Probe Request Captured:"
    try:
        extra = pkt.notdecoded
    except:
        extra = None
    if extra!=None:
        signal_strength = -(256-ord(extra[-4:-3]))
    else:
        signal_strength = -100
        print "No signal strength found"    
    print "Target: %s Source: %s SSID: %s RSSi: %d"%(pkt.addr3,pkt.addr2,pkt.getlayer(Dot11ProbeReq).info,signal_strength)

def main():
    # @hack first wifi interface is most of the time en0, so we can hardcode it
    default_interface = 'en0' if IS_OSX else 'wlan0'

    # make sure we are running as root, we will need it
    if os.geteuid() != 0:
        exit("You need to have root privileges to run this script.\nPlease try again, this time using 'sudo'. Exiting.")

    # command line parsing
    parser = argparse.ArgumentParser(description='phoneprobe - sniff for probe requests from mobile phones')
    parser.add_argument('-i', '--interface', dest='interface', type=str, required=False, help='Interface to use for sniffing and packet injection', default=default_interface)
    args = parser.parse_args()

    # prepare the interface for capture
    #monitor_mode(args.interface)

    # feed back to user
    from datetime import datetime
    print("[{0}] Starting scan".format(datetime.now()) )
    print("Scanning on interface {0}".format(args.interface) )
    print('Press CTRL+c to stop sniffing...')

    # run channel hopping process
    # global channel_hop_proc
    # channel_hop_proc = Process(target=channel_hopper, args=(args.interface,))
    # channel_hop_proc.start()
    # signal.signal(signal.SIGINT, stop_channel_hop)

    # start sniffer
    sniff(iface=args.interface, prn=handle_packet) # stop_filter=keep_sniffing, 
    
if __name__=="__main__":
    main()