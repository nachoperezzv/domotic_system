#include <LiquidCrystal.h>
#include <SoftwareSerial.h>
#include "items.h"
#include <math.h>
#include <RTClib.h>


#define thermistor_resis 10000

// SOftware Serial
SoftwareSerial SerialEsp(2,3); // RX / TX

// Counter for shifter iterations
int count = 0;

// Lights pin numbers
const int led_button = 3;
const int led_pin = 5; // Digital --> PWM


// Shifter pins
const int latchPin = 7; //7 1
const int clockPin = 6; //6 2 
const int dataPin = 4; // 4 0

// LCD pin numbers
const int rs = 13, en = 12, d4 = 11, d5 = 10, d6 = 9, d7 = 8;

// Sensors pin numbers
const int photorresistor = A1; // Analogic
const int temp_sensor_pin = A2;
const int echoPin = 2;

// Real Time Clock
RTC_DS3231 rtc;

// Current Data

CurrentData currentData = CurrentData();


// Global variables
const int light_threshold = 600; // Barrier that makes the led light or not
long distanceCm = 0.0;

String tv_display = "MAMAWEBO";

//int movement = tv_display.length();

int default_temp = 22;
int temp_range = 2;


// Light state
bool lights_on = true;

// Items declarations
Lights led = Lights(light_threshold, led_pin, photorresistor);
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);
Shifter shifter = Shifter(latchPin, dataPin, clockPin);

void setup(){
  Serial.begin(9600);
  lcd.begin(16, 2);

  // Pines PWM y Analógicos
  pinMode(led_pin, OUTPUT);
  pinMode(led_button, INPUT_PULLUP);
  pinMode(photorresistor, INPUT);

  // Shifter pins 
  pinMode(latchPin, OUTPUT);
  pinMode(dataPin, OUTPUT);
  pinMode(clockPin, OUTPUT);
  
  // Button interrumption
  attachInterrupt(digitalPinToInterrupt(led_button),led_button_interrupt, RISING);  
  if (! rtc.begin()) {
   Serial.println("No hay un módulo RTC");
   while (1);
   }
  rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));
}

void loop(){
  
  // -------------------------- LED y BOTÓN -------------------------- //
  int led_value = led.set_led_intensity(lights_on);
  led.set_value(led_value);  

  // -------------------------- LCD TV -------------------------- //
  lcd.setCursor(0,0);
  lcd.print(tv_display);
//  lcd.setCursor(0,1);
//  lcd.print(tv_display2);

  // -------------------------- TEMPERATURE  -------------------------- //
   
  float temperatura;
  int resistencia;
 
  resistencia = thermistor_get_resistance(analogRead(thermistor_resis));
  temperatura = thermistor_get_temperature(resistencia);
  
  // -------------------------- SHIFTER  -------------------------- //
  shifter.set_shifter_on(1,1,count); 
  count++;
  if(count >= 4){
    count = 0;
  }

  // -------------------------- ULTRASONIC  -------------------------- // 
  // devuelve una medida bien y un 0 en la siguiente todo el rato
  long duration = pulseIn(echoPin, HIGH, 10000);
  distanceCm = duration * 10 / 292 / 2;


  // -------------------------- CLOCK  -------------------------- // 
  DateTime now = rtc.now();
  char hour_mins[4];
  sprintf(hour_mins, "%02d%02d", now.hour(), now.minute());
}


// --------------------------- FUNCTIONS --------------------------- //

int thermistor_get_resistance(int adcval)
{
  // calculamos la resistencia del NTC a partir del valor del ADC
  return (thermistor_resis * ((1023.0 / adcval) - 1));
}


float thermistor_get_temperature(int resistance)
{
  float temp;
 
  temp = log(resistance);
 
  // resolvemos la ecuacion de STEINHART-HART
  temp = 1 / (0.001129148 + (0.000234125 * temp) + (0.0000000876741 * temp * temp * temp));
 
  // convertir el resultado de kelvin a centigrados y retornar
  return temp - 273.15;
}

// --------------------------- INTERRUMPTIONS --------------------------- //

void led_button_interrupt(){
  lights_on = !lights_on;  
}
