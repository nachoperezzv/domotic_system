// Importing the library of the ESP8266
#include <ESP8266WiFi.h>

// TCP/IP variables
int         port  = 8888;

const char  *SSID = "Nacho_cabezon";
const char  *PASS = "123456789";

// Variables for the connections
String led = "1";
String tv = "1";
String air = "1";
String appliance = "1";
String blind = "1";
// Setting up the Serial Port
void Serial_SetUp()
{
  Serial.begin(115200);
  // Serial.setTimeout(3200);
}

// Functions: Set up of the ESP8266
void ESP8266_SetUp()
{
  WiFi.mode(WIFI_STA);
  WiFi.begin(SSID, PASS);

  while(WiFi.status() != WL_CONNECTED){ delay(50); /*Waiting for connection*/ }
  Serial.println("Connected to the WiFi");
}

String get_trama()
{
  String str = led + tv + air + appliance + blind;
  return str;
}
