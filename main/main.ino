#include <stdio.h>
#include <string.h>
#include "lib.h"

// Doc: https://www.arduino.cc/reference/en/libraries/wifi/

// Global variables
WiFiServer server(port);
String msg;
String trama;

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
        else if(msg == "0")
        {
          //do nothing 
          Serial.println(trama); 
        }
        else if(msg.startsWith("11"))
        {
          led = "1";
          Serial.println(trama);
        }
        else if(msg.startsWith("10"))
        {
          led = "0";
          Serial.println(trama);
        }

        trama = get_trama();
        char buf[8];
        trama.toCharArray(buf,8);
        client.write(buf);
                
//        // LED TRAMA
//        else if(msg.startsWith("10")) // Trama for LED_WRITE
//        {
//          // Interface is writing and changing the status of the LED
//          if(msg=="100")        // LED is Off
//            led = '0';
//          else if(msg=="101")   // LED is On
//            led = '1';
//        }
//        else if(msg.startsWith("11")) // Trama for LED_READ
//        {
//          // Interface is asking for the status of the led
//          client.write(led);
//        }
//  
//        // TV TRAMA
//        else if(msg.startsWith("20"))  // Trama for TV_WRITE
//        {
//          // Interface is writing and changing the status of the TV
//          if(msg=="200")      // TV is off
//            tv = '0';          
//          else if(msg=="201") // TV is on
//            tv = '1';
//        }
//        else if(msg.startsWith("21"))   // Trama for TV_READ
//        {
//          // Interface is asking for the status of the TV
//          client.write(tv);
//        }
//  
//        // AIR TRAMA
//        else if(msg.startsWith("300")) // Trama for AIR_WRITE
//        {
//          // Interface is writting and changing the status of the AIR
//          if(msg=="300")      // Air is off
//            air = '0';  
//          else if(msg=="301") // Air is on - HOT
//            air = '1';
//          else if(msg=="302") // Air is on - COLD
//            air = '2';            
//        }
//        else if(msg.startsWith("31"))  // Trama for AIR_READ
//        {
//          // Interface is asking for the status of the air
//          client.write(air);
//        }
//  
//        // APPLIANCE TRAMA
//        else if(msg.startsWith("40"))  // Trama for APPLIANCE_WRITE
//        {
//          // Interface is writting and changing the status of the APPLIANCE
//          if(msg=="400")      // Appliance is off
//            appliance = '0';
//          else if(msg=="401") // Appliance is on
//            appliance = '1';
//        }
//        else if(msg.startsWith("41"))  // Trama for APPLIANCE_READ
//        {
//          // Interface is asking for the status of the AIR
//          client.write(appliance);
//        }
//  
//        // BLIND TRAMA
//        else if(msg.startsWith("50"))  //Trama for the BLINDS_WRITE
//        {
//          // Interface is writting and changing the status of the BLINDS
//          if(msg=="500")      // Blind is off
//            blind = '0';
//          else if(msg=="501") // Blind is up
//            blind = '1';
//          else if(msg=="502") // Blind is down
//            blind = '2';            
//        }
//        else if(msg.startsWith("51"))  // Trama for the BLINDS_READ
//        {
//          // Interface is asling for the status of the BLINDS
//          client.write(blind);
//        }
        
        //Serial.println(msg);
        msg.clear();
      }
         
    }
    client.flush();
    client.stop();  
  }  
}
