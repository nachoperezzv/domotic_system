#include <LiquidCrystal.h>
#include <SoftwareSerial.h>
#include "items.h"
#include <math.h>
#include <RTClib.h>

// Software Serial
// SoftwareSerial SerialEsp(2,3); // RX / TX

// Counter for shifter iterations
int count_shifter_iterations = 0;
int blinds_counter = 3000;
int blinds_threshold = 3000;

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

bool air_active = false;

// Current Data
CurrentData currentData = CurrentData();

String sentence = currentData.get_random_tv_sentence();

// Real Time Clock
RTC_DS3231 rtc;

// Global variables
const int light_threshold = 600; // Barrier that makes the led light or not

// Items declarations
Lights led = Lights(light_threshold, led_pin, photorresistor);
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);
Shifter shifter = Shifter(latchPin, dataPin, clockPin);

//----------SETUP--------------

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

//-------------LOOP-------------

void loop(){
  if (Serial.available()){
    decodeData();
  } 

  DateTime right_now = rtc.now(); 

  int current_time = currentData.get_time(right_now);

  // ---------- AIR ------------
  
  int air_number = 0, air_state = currentData.get_air_mode(); 
  int temperature = round(currentData.get_temperature());

  shifter.set_shifter_on(currentData.get_air_state(),currentData.get_blinds_state(),1,count_shifter_iterations); 
  shifter.set_shifter_on(currentData.get_air_state(),currentData.get_blinds_state(),0,count_shifter_iterations); 

  int presence = currentData.get_presence();
  
  if(air_state == 1){ // Manual
    if(currentData.get_desired_temperature() < temperature){
      air_number = 1;
      currentData.set_air_state(1);
    }
    else if(currentData.get_desired_temperature() > temperature){
      air_number = 2;
      currentData.set_air_state(2);
    }
    else{
      air_number = 0;
      currentData.set_air_state(0);
    }
  }
  else if(air_state == 2){

    if(  (current_time <= currentData.get_back_hour() && current_time >= (currentData.get_back_hour()-100)) ||  ((current_time <= currentData.get_not_home() || current_time >= (currentData.get_back_hour()-100)) && currentData.is_inside(presence))){ // Esto quiere decirqueen teoria estas en casa
      
      if(temperature < currentData.get_min_temperature() || temperature > currentData.get_max_temperature() || air_active){
        air_active = true;
      }
      else{
        air_number = 0;
        currentData.set_air_state(0);
      }
  
      if(air_active){
        if(currentData.get_default_temperature() < temperature){
          air_number = 1;
          currentData.set_air_state(1);
        }
        else if(currentData.get_default_temperature() > temperature){
          air_number = 2;
          currentData.set_air_state(2);
        }
        else{
          air_number = 0;
          air_active = false;
          currentData.set_air_state(0);
        }
      }
                
    }
    else{
      air_number = 0;
      air_active = false;
      currentData.set_air_state(0);
    }
  }
  else{ // Shut down or failure
    air_number = 0;
  }

  // ----------------APPLIANCE-----------
  int appliance_number = 0;
  if(currentData.get_appliance() == 1 || (current_time >= currentData.get_laundry_time() && current_time <= currentData.get_laundry_time()+30 )){
    appliance_number = 1;
    currentData.set_appliance(1);
    currentData.set_appliance_state(1);
  }
  else{
    appliance_number = 0;
    currentData.set_appliance(0);
    currentData.set_appliance_state(0);
  }

  

  // ----BLINDS


  
  right_now = rtc.now();
  int blinds_number = 0;
  //Serial.println(blinds_counter);
  
  if( current_time >= currentData.get_wake_hour() && current_time < currentData.get_wake_hour()+5 && blinds_counter < blinds_threshold){
    blinds_number = 1;
    currentData.set_blinds_state(1);
    blinds_counter++;
  }
  else if(current_time >= currentData.get_sleep_hour() && current_time < currentData.get_sleep_hour()+5 && blinds_counter > 0){
    blinds_number = 2;
    currentData.set_blinds_state(2);
    blinds_counter--;
  }
  else if(currentData.get_blinds() == 1 && blinds_counter < blinds_threshold){
    blinds_number = 1;
    currentData.set_blinds_state(1);
    blinds_counter++;
  }
  else if(currentData.get_blinds() == 2 && blinds_counter > 0){
    blinds_number = 2;
    currentData.set_blinds_state(2);
    blinds_counter--;
  }
  else{
    blinds_number = 0;
    currentData.set_blinds_state(0);
  }
 
  
  shifter.set_shifter_on(air_number,blinds_number,1,count_shifter_iterations); 
  shifter.set_shifter_on(air_number,blinds_number,0,count_shifter_iterations); 
  count_shifter_iterations++;
  if(count_shifter_iterations >= 4){
    count_shifter_iterations = 0;
  }

  

  
  // LIGHTS
  
  presence = currentData.get_presence();

  if (presence != 2){  
    if(currentData.is_inside(presence) && currentData.get_light()){
      int led_value = led.set_led_intensity(currentData.get_light());
      led.set_value(led_value);  
      currentData.set_light_state(1);
    }
    else{
      led.set_value(0);
      currentData.set_light_state(0);
    }
  }

  
  // TELEVISION

  if (currentData.is_inside(presence)){
    if (currentData.get_television()){
      lcd.display();
      lcd_manager(right_now);
      currentData.set_television_state(1);
    }
    else{
      lcd.noDisplay();
      currentData.set_television_state(0);
    }
  }
  else{
    lcd.noDisplay();
    currentData.set_television_state(0);
  }
  
  
}


// --------------------------- INTERRUMPTIONS --------------------------- //

void led_button_interrupt(){
  currentData.set_light(!currentData.get_light());  
}

void lcd_manager(DateTime right_now){

  char hour_mins[4];
  sprintf(hour_mins, "%02d:%02d", right_now.hour(), right_now.minute()); 
  int temperature = round(currentData.get_temperature()); 
  String time_sentence = "";  

  String new_sentence = sentence;
  int new_position_counter = sentence_position_counter;
  
  if (lcd_iterations_counter >= max_lcd_iterations_threshold){
    time_sentence = String(hour_mins) + " " + String(temperature) + "C";
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
  lcd.setCursor(3,1);
  lcd.print(time_sentence);
  lcd_iterations_counter++;
  
}

void encodeData(){
  String message = "1";

  message += String(currentData.get_light_state());
  message += String(currentData.get_television_state());
  message += String(currentData.get_air_state());
  message += String(currentData.get_appliance_state());
  message += String(currentData.get_blinds_state());
  
  Serial.print(message);
}

void decodeData(){

  String instruction = Serial.readString();

  int instruction_type = instruction.substring(0,1).toInt();

  if (instruction_type == 1){
    currentData.set_light(instruction.substring(1,2).toInt());
    currentData.set_television(instruction.substring(2,3).toInt());
    currentData.set_air_mode(instruction.substring(3,4).toInt());
    currentData.set_desired_temperature(instruction.substring(4,6).toInt());
    currentData.set_appliance(instruction.substring(6,7).toInt());
    currentData.set_blinds(instruction.substring(7,8).toInt());
  }
  else if (instruction_type == 2){
    currentData.set_wake_hour(instruction.substring(1,5).toInt());
    currentData.set_not_home(instruction.substring(5,9).toInt());
    currentData.set_back_hour(instruction.substring(9,13).toInt());
    currentData.set_sleep_hour(instruction.substring(13,17).toInt());
    currentData.set_default_temperature(instruction.substring(17,19).toInt());
    currentData.set_min_temperature(instruction.substring(19,21).toInt());
    currentData.set_max_temperature(instruction.substring(21,23).toInt());
    currentData.set_laundry_time(instruction.substring(23,27).toInt());   
  }
  encodeData();
}
