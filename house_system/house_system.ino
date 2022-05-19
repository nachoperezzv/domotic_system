#include <LiquidCrystal.h>
#include <SoftwareSerial.h>
#include "items.h"
#include <math.h>
#include <RTClib.h>

// SOftware Serial
// SoftwareSerial SerialEsp(2,3); // RX / TX

// Counter for shifter iterations
int count_shifter_iterations = 0;

//pulse indicator
int pulse = 0;

//LCD Iterations
int lcd_iterations_counter = 0;
int max_lcd_iterations_threshold = 100;
int sentence_position_counter = 16;

// Lights pin numbers
const int led_button = 3;
const int led_pin = 5; // Digital --> PWM


// Shifter pins
const int latchPin = 7; //7 1
const int clockPin = 6; //6 2 
const int dataPin = 4; // 4 0

// LCD pin numbers
const int rs = 13, en = 12, d4 = 11, d5 = 10, d6 = 9, d7 = 8;

const int photorresistor = A1;

// Current Data

CurrentData currentData = CurrentData();


String sentence = currentData.get_random_tv_sentence();


// Real Time Clock
RTC_DS3231 rtc;


// Global variables
const int light_threshold = 600; // Barrier that makes the led light or not

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
  
  
  
  // -------------------------- SHIFTER  -------------------------- //
  shifter.set_shifter_on(2,1,1,count_shifter_iterations); 
  currentData.get_presence();
  
  count_shifter_iterations++;
  if(count_shifter_iterations >= 4){
    count_shifter_iterations = 0;
  }

  // -------------------------- ULTRASONIC  -------------------------- // 
  

  // -------------------------- CLOCK  -------------------------- // 
  DateTime right_now = rtc.now();
  
  lcd_manager(right_now);
}


// --------------------------- INTERRUMPTIONS --------------------------- //

void led_button_interrupt(){
  lights_on = !lights_on;  
}

void lcd_manager(DateTime right_now){

  char hour_mins[4];
  sprintf(hour_mins, "%02d:%02d", right_now.hour(), right_now.minute());
  String time_sentence = String(hour_mins); 

  String new_sentence = sentence;
  int new_position_counter = sentence_position_counter;
  
  if (lcd_iterations_counter >= max_lcd_iterations_threshold){
    lcd_iterations_counter = 0;
    if(sentence_position_counter <= -(int)sentence.length()){
      sentence = currentData.get_random_tv_sentence();
      sentence_position_counter = 16;
      new_position_counter = sentence_position_counter;
      new_sentence = sentence.substring(0,16);
    }
    else if(sentence_position_counter < 0){
      new_sentence = sentence.substring(abs(sentence_position_counter));
      sentence_position_counter--;
      new_position_counter = 0;
      
    }
    else{
      sentence_position_counter--;
      new_position_counter = sentence_position_counter;
      new_sentence = sentence.substring(0,16);
    }
    lcd.clear();
    lcd.setCursor(new_position_counter,0);
    lcd.print(new_sentence);
    
  }
  lcd.setCursor(5,1);
  lcd.print(time_sentence);
  lcd_iterations_counter++;
  
}

void encodeData(char* instruction){
  

}


void decodeData(char* instruction){

  int instruction_type = (int)instruction[0];

  if (instruction_type == 1){
    
    
  }
  else if (instruction_type == 2){

    
  }

}
