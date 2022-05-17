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

    uint8_t appliance_on_us[4];
    uint8_t appliance_off_us[2];
    
    int pin_latch;
    int pin_data;
    int pin_clock;

    Shifter(int, int, int);
    void update_shifter_register(uint8_t);
    uint8_t get_air_blinds_data(int, int, int);
    uint8_t get_appliance_data(int, int);
    void set_shifter_on(int, int, int, int);

  
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


  // B 0 sh1 sh2 sh3 sh4 0 0 0
  appliance_off_us[0] = B00000001;
  appliance_off_us[1] = B00000001;

  appliance_on_us[0] = B01100001;
  appliance_on_us[1] = B00110000;
  appliance_on_us[2] = B00011001;
  appliance_on_us[3] = B01001000;
  Serial.println(air_off_blinds_up[0]);
  
}

void Shifter::update_shifter_register(uint8_t data){
  digitalWrite(pin_latch, LOW);
  shiftOut(pin_data, pin_clock, LSBFIRST, data);
  digitalWrite(pin_latch, HIGH);
}

uint8_t Shifter::get_air_blinds_data(int air, int blinds, int iteration){

  if(air == 1){ // air cold
    if(blinds == 1){ // blinds up
      if(iteration < 4){
        return air_cold_blinds_up[iteration];
      }
      else{ // blinds off
        return air_off_blinds_off;      
      }
    }
    else if(blinds == 2){ // blinds down
      if(iteration < 4){
        return air_cold_blinds_down[iteration];
      }
      else{ // blinds off
        return air_off_blinds_off;      
      }
    }
    else{ // blinds off
      return air_cold_blinds_off;      
    }
  }
  
  else if(air == 2){ // air hot
    if(blinds == 1){ // blinds up
      if(iteration < 4){
        return air_hot_blinds_up[iteration];
      }
      else{ // blinds off
        return air_off_blinds_off;      
      }
    }
    else if(blinds == 2){ // blinds down
      if(iteration < 4){
        return air_hot_blinds_down[iteration];
      }
      else{ // blinds off
        return air_off_blinds_off;      
      }
    }
    else{ // blinds off
      return air_hot_blinds_off;      
    }
  }
  
  else{ // air off
    if(blinds == 1){ // blinds up
      if(iteration < 4){
        return air_off_blinds_up[iteration];
      }
      else{ // blinds off
        return air_off_blinds_off;      
      }
    }
    else if(blinds == 2){ // blinds down
      if(iteration < 4){
        return air_off_blinds_down[iteration];
      }
      else{ // blinds off
        return air_off_blinds_off;      
      }
    }
    else{ // blinds off
      return air_off_blinds_off;      
    }
  }  
}

uint8_t Shifter::get_appliance_data(int appliance, int iteration){

  if(appliance == 1){
    if(iteration < 4){
      return appliance_on_us[iteration];
    }
    else{
      if(iteration < 4){
        if(iteration < 2){
          return appliance_on_us[iteration];
        }
        else{
          return appliance_on_us[iteration-2];
        }
        
      }
    }
  }
  else{
    if(iteration < 4){
      if(iteration < 2){
        return appliance_on_us[iteration];
      }
      else{
        return appliance_on_us[iteration-2];
      }
    }
  }  
}

void Shifter::set_shifter_on(int air, int blinds, int appliance, int iteration){
  byte data1 = get_air_blinds_data(air, blinds, iteration);
  uint8_t data2 = get_appliance_data(appliance, iteration);

  update_shifter_register(data2);
  update_shifter_register(data1);
    
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
