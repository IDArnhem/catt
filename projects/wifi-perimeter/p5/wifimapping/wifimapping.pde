import oscP5.*;
import netP5.*;

boolean sketchFullScreen() {
  return true;
}

OscP5 oscP5 = new OscP5(this,2222);
NetAddress myBroadcastLocation = new NetAddress("127.0.0.1",32000); 

ArrayList<WifiNode> nodes = new ArrayList<WifiNode>();

String name = "";
String macaddress = "";
int value = 0;
boolean newMessage = false;

void setup() {
  size(displayWidth, displayHeight, P2D);
  frameRate(60);
  textAlign(CENTER);
  colorMode(HSB, 360, 100, 100, 100);
  smooth(8);
  background(0);
}

void draw() {
  background(0);
  for (int i = 0; i<nodes.size(); i++) {
    WifiNode n = nodes.get(i);
    n.update(i, nodes.size());
    n.display();
  }
}

class WifiNode {
  int id;
  int total;
  String name;
  String macaddress;
  int value;

  float cx = (width / 2);
  float cy = (height / 2);
  float deg, rad, len, px, py;
  
  WifiNode(String name, String macaddress, int value) {
    this.id = id;
    this.name = name;
    this.macaddress = macaddress;
    this.value = value; 
  }
  
  void update(int i, int total) {
    id = i;
    total = total;

    deg = map(id,0,nodes.size(),0,360);
    rad = radians(deg);
    len = map(value,-90,-30,height/2-50,0);
    px = (cos(rad) * len) + cx;
    py = (sin(rad) * len) + cy;
  }
  
  void display() {
    noFill();
    stroke(0,0,100);
    ellipse(px, py, 10, 10);
    line(width/2,height/2,px,py);
    text(name,px,py + 15);
  }
}


//wifi signals go from -30 (highest) to -90 (lowest)
void oscEvent(OscMessage theOscMessage) {
  name = theOscMessage.get(0).stringValue();  
  macaddress = theOscMessage.get(1).stringValue();
  value = theOscMessage.get(2).intValue();

  boolean found = false;
  for(int i = 0; i < nodes.size(); i++) {
    WifiNode tmp = nodes.get(i);
    found = tmp.macaddress.equals(macaddress);
    if(found) {
      nodes.get(i).value = value;
      break;
    }
  }

  if(!found) {
   nodes.add(new WifiNode(name, macaddress, value));
 }
}

