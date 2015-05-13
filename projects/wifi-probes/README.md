## WiFi Probe packets


### Method 1

This approach uses a packet crafting library for python called [http://bb.secdev.org/scapy/wiki/Home](Scapy). Make sure you have it installed.

    sudo pip install scapy

### Method 2
The script will put your mac in 'monitor' mode and will sniff the waves for 'wifi probe' packets, it will collect a list of devices including the mac address, the rssi (signal strength) and the ssid (if any), as well as the time when it was found and at which loop.

The script will channel-hop, meaning that it will change channel every 8 seconds and scan the waves for devices in that channel. It scans channels from 1 to 14 and then it starts all over again. Every time it starts it increments the loop variable.

The mac is (deliberately) slow to capture wifi packets, so that means that at 8 seconds per channel and 14 channels it can take a while to detect a given device.

What you do with this script is you have to run it in two different computers, then get their IP addresses and then you can fetch the list of devices "seen" by each computer, by accessing the list on the little webserver that runs on the program that I wrote for you.

http://<ip of first  computer>:8080/
http://<ip of second computer>:8080/

The list returned is in JSON format, you should be able to get some help from Dan or a classmate to parse that.

