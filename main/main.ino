#include <stdio.h>
#include <string.h>
#include "lib.h"

// Doc: https://www.arduino.cc/reference/en/libraries/wifi/

// Global variables
WiFiServer server(port);
String msg;
String trama;

// Variables for the connections
String led = "1";
String tv = "1";
String air = "1";
String temp1 = "2";
String temp2 = "3";
String appliance = "1";
String blind = "1";

String get_trama()
{
  String str = led + tv + air + temp1 + temp2 + appliance + blind;
  Serial.println(str);
  return str;
}

void setup() {
  Serial_SetUp();  
  ESP8266_SetUp();
  server.begin();

  trama = get_trama();
}

void loop() {
  // Gets a client that is connected to the server and has data avaliable for reading. 
  // The connections persists when the returned client object goes out of scope.
  // server.available() returns a client object. If no client has data available for
  // reading, this object will evaluate to false in an IF statement
  WiFiClient client = server.available(); 

  // client.connected() returns true if the connection succeeds, false if not.
  if(client)
  {
    while(client.connected())
    {
      // client.available() returns the number of bytes available for reading
      int c;
      c = client.available();
      if(c>0)
      {
        for(int i=0;i<c;i++)
        {
//          Serial.print(i);
          char r = client.read();
//          Serial.print(" ");
//          Serial.print(r);
//          Serial.print(" ");
          // client.read() reads the next byte received from the server the client is 
          // connected to. Returns -1 if none is available
          if(r!=-1)
          {
            msg.concat(r);
//            Serial.println(msg);
          }
        }

        // Initial message Connecting
        if(msg=="connecting")
        {
          client.write("connected");  
          Serial.println("Connected to the interface");
        }

        // If the interfaces it's only asking for info and don't want to make changes
        if(msg == "0")
        {
          //do nothing 
          trama = get_trama();
        }
        else 
        {
          if(msg.substring(1,2).toInt() == 1)
          {
            led = "1";
          }
          if(msg.substring(1,2).toInt() == 0)
          {
            led = "0";
          }
          if(msg.substring(2,3).toInt() == 0)
          {
            tv = "0";
          }
          if(msg.substring(2,3).toInt() == 1)
          {
            tv = "1";
          }
          if(msg.substring(3,4).toInt() == 0)
          {
            air = "0";
          }
          if(msg.substring(3,4).toInt() == 1)
          {
            air = "1";
          }
          if(msg.substring(6,7).toInt() == 0)
          {
            appliance = "0";
          }
          if(msg.substring(6,7).toInt() == 1)
          {
            appliance = "1";
          }
          if(msg.substring(7,8).toInt() == 0)
          {
            blind = "0";
          }
          if(msg.substring(7,8).toInt() == 1)
          {
            blind = "1";
          }
        }
        Serial.print(led);
        Serial.print(tv);
        Serial.print(air);
        Serial.print(temp1);
        Serial.print(temp2);
        Serial.print(appliance);
        Serial.println(blind);
        
        trama = get_trama();
        
        char buf[8];
        trama.toCharArray(buf,8);
        client.write(buf);

        Serial.println(trama);
        
        msg.clear();
      }
         
    }
    client.flush();
    client.stop();  
  }  
}
