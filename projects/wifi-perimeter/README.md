## Simple wifi-perimeter scanner

- Your client must speak OSC. See Processing example "wifimapping" by Willem Kempers.
- **For OSX only**.
- Terrible latency. Every time the airport tool is called a 3 second scan is performed. So if you want higher sampling frequencies you will need a dedicated setup.

You are supposed to have the OSX airport utility in your path, so you will have to open up a terminal and type in some commands.

Create a symbolic link to the airport utility in your path:

`sudo ln -s /System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport /usr/sbin/airport`

Test that it worked by typing:

`airport --scan --xml`

You should now see a dump of wifi networks within range.

The python interface to your OS contains another usefull snippets such as listing all the WiFi networks your mac has ever been connected to.

### Processign sketch
You can use the included processing sketch as your starting point for WiFi signal visualizations.

Thanks to [Willem Kempers](http://willemkempers.nl/) for the sketch.
