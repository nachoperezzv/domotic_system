#include <RTClib.h>

#define thermistor_resis 10000

class CurrentData {
  public:

    int light;
    int air_mode;
    int sleep_hour;
    int wake_hour; 
    int not_home;
    int back_hour;

    int default_temperature;
    int desired_temperature;
    int max_temperature;
    int min_temperature;
    //                        "123456789ABCDEFGHIJKLMNÑOPQRSTUV"
    String tv_sentences[6] = {"NACHO CUMPLE LOS 100 ANOS",
                              "BASCU TERMINA SU TFG",
                              "AURE SE CASA CON MISS FORTUNE",
                              "CARLOS SE RAPA",
                              "TEEMO ROMPE RELACIONES CON AMPI",
                              "PC DE LA UA ENCIENDE EN <1 HORA"};

    char lcd;
    bool presence;

    //SETTERS
    void set_light(int value){light = value;};
    void set_air_mode(int value){air_mode = value;};
    void set_sleep_hour(int value){sleep_hour = value;};
    void set_wake_hour(int value){wake_hour = value;};
    void set_not_home(int value){not_home = value;};
    void set_back_hour(int value){back_hour = value;};
    void set_default_temperature(int value){default_temperature = value;};
    void set_desired_temperature(int value){desired_temperature = value;};
    void set_max_temperature(int value){max_temperature = value;};
    void set_min_temperature(int value){min_temperature = value;};

    //GETTERS
    int get_light(int value){return light;};
    int get_air_mode(int value){return air_mode;};
    int get_sleep_hour(int value){return sleep_hour;};
    int get_wake_hour(int value){return wake_hour;};
    int get_not_home(int value){return not_home;};
    int get_back_hour(int value){return back_hour;};
    int get_default_temperature(int value){return default_temperature;};
    int get_desired_temperature(int value){return desired_temperature;};
    int get_max_temperature(int value){return max_temperature;};
    int get_min_temperature(int value){return min_temperature;};

    
    int get_temperature();
    int get_presence();
    int get_time(DateTime);
    String get_random_tv_sentence();
    CurrentData(){};
  
};

int CurrentData::get_temperature(){
  
  float temperature;
  int resistance;
  const int temperature_pin = A2;
  
 
  resistance = (thermistor_resis * ((1023.0 / analogRead(temperature_pin)) - 1));
 
  temperature = log(resistance);
 
  // resolvemos la ecuacion de STEINHART-HART
  temperature = 1 / (0.001129148 + (0.000234125 * temperature) + (0.0000000876741 * temperature * temperature * temperature));
 
  // convertir el resultado de kelvin a centigrados y retornar
  return temperature - 273.15;
  
}

int CurrentData::get_presence(){
  const int echoPin = 2;

  // devuelve una medida bien y un 0 en la siguiente todo el rato
  long duration = pulseIn(echoPin, HIGH, 10000);
  long distanceCm = duration * 10 / 292 / 2;

  if(distanceCm == 0){
    return 2;
  }
  else{
    return distanceCm < 15 ? 1 : 0;
  }
  
  
}

int CurrentData::get_time(DateTime right_now){
  char hour_mins[4];
  sprintf(hour_mins, "%02d%02d", right_now.hour(), right_now.minute());
  return String(hour_mins).toInt();
}

String CurrentData::get_random_tv_sentence(){
  int len = sizeof(tv_sentences) / sizeof(String);
  return tv_sentences[(int)random(0,len)];  
}


class Lights {  
  public: 
    int lights_threshold; 
    int led_pin;
    int sensor_pin;
  
    Lights(int, int, int);
    int get_sensor_measure();
    int set_led_intensity(bool);
    void set_value(int);
  
};

class Air{
  public:
    int hot_pin;
    int cold_pin;
    int default_temp;
    int temp_range;

    Air(int, int, int, int);
    int set_temperature(int);
    void power_air_on(int);
};

class Shifter{
  public:
  
    uint8_t air_cold_blinds_off;
    uint8_t air_hot_blinds_off;
    uint8_t air_off_blinds_off;
    
    uint8_t air_cold_blinds_up[4];
    uint8_t air_hot_blinds_up[4];
    uint8_t air_off_blinds_up[4];

    uint8_t air_cold_blinds_down[4];
    uint8_t air_hot_blinds_down[4];
    uint8_t air_off_blinds_down[4];

    uint8_t air_cold_blinds_off_send_pulse;
    uint8_t air_hot_blinds_off_send_pulse;
    uint8_t air_off_blinds_off_send_pulse;
    
    uint8_t air_cold_blinds_up_send_pulse[4];
    uint8_t air_hot_blinds_up_send_pulse[4];
    uint8_t air_off_blinds_up_send_pulse[4];

    uint8_t air_cold_blinds_down_send_pulse[4];
    uint8_t air_hot_blinds_down_send_pulse[4];
    uint8_t air_off_blinds_down_send_pulse[4];

    
    int pin_latch;
    int pin_data;
    int pin_clock;

    Shifter(int, int, int);
    void update_shifter_register(uint8_t);
    uint8_t get_air_blinds_data(int, int, int, int);
    void set_shifter_on(int, int, int, int);
    void send_pulse();

  
};

// ------------------ SHIFTER ------------------ //

Shifter::Shifter(int l, int d, int c){
  pin_latch = l;
  pin_data = d;
  pin_clock = c;
  
  // B 0 hot cold sh1 sh2 sh3 sh4 0
  air_cold_blinds_off = B00100000;
  
  air_hot_blinds_off = B01000000;
  
  air_off_blinds_off = B00000000;

  air_cold_blinds_down[0] = B00111000;
  air_cold_blinds_down[1] = B00101100;
  air_cold_blinds_down[2] = B00100110;
  air_cold_blinds_down[3] = B00110010;

  air_hot_blinds_down[0] = B01011000;
  air_hot_blinds_down[1] = B01001100;
  air_hot_blinds_down[2] = B01000110;
  air_hot_blinds_down[3] = B01010010;

  air_cold_blinds_up[0] = B00100110;
  air_cold_blinds_up[1] = B00101100;
  air_cold_blinds_up[2] = B00111000;
  air_cold_blinds_up[3] = B00110010;

  air_hot_blinds_up[0] = B01000110;
  air_hot_blinds_up[1] = B01001100;
  air_hot_blinds_up[2] = B01011000;
  air_hot_blinds_up[3] = B01010010;

  air_off_blinds_down[0] = B00011000;
  air_off_blinds_down[1] = B00001100;
  air_off_blinds_down[2] = B00000110;
  air_off_blinds_down[3] = B00010010;

  air_off_blinds_up[0] = B00000110;
  air_off_blinds_up[1] = B00001100;
  air_off_blinds_up[2] = B00011000;
  air_off_blinds_up[3] = B00010010;

  //----------------------//

  air_cold_blinds_off_send_pulse = B10100000;
  
  air_hot_blinds_off_send_pulse = B11000000;
  
  air_off_blinds_off_send_pulse = B10000000;

  air_cold_blinds_down_send_pulse[0] = B10111000;
  air_cold_blinds_down_send_pulse[1] = B10101100;
  air_cold_blinds_down_send_pulse[2] = B10100110;
  air_cold_blinds_down_send_pulse[3] = B10110010;

  air_hot_blinds_down_send_pulse[0] = B11011000;
  air_hot_blinds_down_send_pulse[1] = B11001100;
  air_hot_blinds_down_send_pulse[2] = B11000110;
  air_hot_blinds_down_send_pulse[3] = B11010010;

  air_cold_blinds_up_send_pulse[0] = B10100110;
  air_cold_blinds_up_send_pulse[1] = B10101100;
  air_cold_blinds_up_send_pulse[2] = B10111000;
  air_cold_blinds_up_send_pulse[3] = B10110010;

  air_hot_blinds_up_send_pulse[0] = B11000110;
  air_hot_blinds_up_send_pulse[1] = B11001100;
  air_hot_blinds_up_send_pulse[2] = B11011000;
  air_hot_blinds_up_send_pulse[3] = B11010010;

  air_off_blinds_down_send_pulse[0] = B10011000;
  air_off_blinds_down_send_pulse[1] = B10001100;
  air_off_blinds_down_send_pulse[2] = B10000110;
  air_off_blinds_down_send_pulse[3] = B10010010;

  air_off_blinds_up_send_pulse[0] = B10000110;
  air_off_blinds_up_send_pulse[1] = B10001100;
  air_off_blinds_up_send_pulse[2] = B10011000;
  air_off_blinds_up_send_pulse[3] = B10010010;

  
}

void Shifter::update_shifter_register(uint8_t data){
  digitalWrite(pin_latch, LOW);
  shiftOut(pin_data, pin_clock, LSBFIRST, data);
  digitalWrite(pin_latch, HIGH);
}

void Shifter::send_pulse(){
  update_shifter_register(air_cold_blinds_off_send_pulse);
}

uint8_t Shifter::get_air_blinds_data(int air, int blinds, int pulse, int iteration){

  if(air == 1){ // air cold
    if(blinds == 1){ // blinds up
      if(pulse == 1){
        return air_cold_blinds_up_send_pulse[iteration];
      }
      else{
        if(iteration < 4){
          return air_cold_blinds_up[iteration];
        }
        else{ // blinds off
         
          return air_cold_blinds_off;       
        }
      }
    }
    else if(blinds == 2){ // blinds down
      if(pulse == 1){
        return air_cold_blinds_down_send_pulse[iteration];
      }
      else{
        if(iteration < 4){
          return air_cold_blinds_down[iteration];
        }
        else{ // blinds off
          
          return air_cold_blinds_off;       
        }
      }
    }
    else{ // blinds off
      if(pulse == 1){
        return air_cold_blinds_off_send_pulse;
      }
      else{
        return air_cold_blinds_off;   
      }  
    }
  }
  
  else if(air == 2){ // air hot
    if(blinds == 1){ // blinds up
      if(pulse == 1){
        return air_hot_blinds_up_send_pulse[iteration];
      }
      else{
        if(iteration < 4){
          return air_hot_blinds_up[iteration];
        }
        else{ // blinds off
          return air_hot_blinds_off;   
        }
      }
    }
    else if(blinds == 2){ // blinds down
      if(pulse == 1){
        return air_hot_blinds_down_send_pulse[iteration];
      }
      else{
        if(iteration < 4){
          return air_hot_blinds_down[iteration];
        }
        else{ // blinds off
          return air_hot_blinds_off;     
        }
      }
    }
    else{ // blinds off  
      if(pulse == 1){
        return air_hot_blinds_off_send_pulse;
      }
      else{
        return air_hot_blinds_off;
      }   
    }
  }
  
  else{ // air off
    if(blinds == 1){ // blinds up
      if(pulse == 1){
        return air_off_blinds_up_send_pulse[iteration];
      }
      else{
        if(iteration < 4){
          return air_off_blinds_up[iteration];
        }
        else{ // blinds off 
          return air_off_blinds_off;              
        }
      }
    }
    else if(blinds == 2){ // blinds down
      if(pulse == 1){
        return air_off_blinds_down_send_pulse[iteration];
      }
      else{
        if(iteration < 4){
          return air_off_blinds_down[iteration];
        }
        else{ // blinds off
          return air_off_blinds_off;     
        }
      }
    }
    else{ // blinds off
      if(pulse == 1){
        return air_off_blinds_off_send_pulse;
      }
      else{
        return air_off_blinds_off;    
      }
    }
  }  
}

void Shifter::set_shifter_on(int air, int blinds, int pulse, int iteration){

  byte data1 = get_air_blinds_data(air, blinds, pulse, iteration);
  
  if(pulse == 1){
    update_shifter_register(data1);
    
    data1 = get_air_blinds_data(air, blinds, 0, iteration);
    
    update_shifter_register(data1);
  }
  else{    
    update_shifter_register(data1);
  }
  

  
    
}


// ------------------ LIGHTS ------------------ //

Lights::Lights(int threshold, int pin, int sensor){
  lights_threshold = threshold;
  led_pin = pin;
  sensor_pin = sensor;
}
  
int Lights::get_sensor_measure(){
  return analogRead(sensor_pin);
}
  
int Lights::set_led_intensity(bool on){
    
  int measure = get_sensor_measure();
  
  if(on && measure > lights_threshold ){    
    return (((float)measure-(float)lights_threshold)/((float)1000-(float)lights_threshold)) * 255;     
  }  
  else      
    return 0;      
}

void Lights::set_value(int value){
  analogWrite(led_pin, value);
}


// ------------------ AIR ------------------ //

Air::Air(int pin_h, int pin_c, int temp, int range){
  hot_pin = pin_h;
  cold_pin = pin_c;
  default_temp = temp;
  temp_range = range;
}


int Air::set_temperature(int temp){
  return temp * 254 / 27;
}

void Air::power_air_on(int temp){
  if(temp < default_temp - temp_range){
    analogWrite(hot_pin, set_temperature(abs(default_temp - temp)));
  }
  else if(temp > default_temp + temp_range){
    analogWrite(cold_pin, set_temperature(abs(default_temp - temp)));
  }
  else{
    analogWrite(cold_pin, 0);
    analogWrite(hot_pin, 0);
  }
}


// ------------------- CurrentData --------------
