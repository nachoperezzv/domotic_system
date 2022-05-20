
import pygame, random, json, time
import urllib.error, urllib.request 


from tramas import *
from lib import *
from datetime import date, datetime

def print_sunny_day(screen, rect):
    # Changing the background of the weather API - Sunny day
    sun = pygame.image.load(SUN_ICON)
    sun_rect = sun.get_rect().clip(rect)
    
    alpha = sun.convert_alpha()
    alpha_rect = alpha.get_rect().clip(rect)
    alpha.fill([50,50,50,50])
    
    screen.blit(sun,sun_rect)
    screen.blit(alpha,alpha_rect)


def print_rainy_day(screen, rect, rain):
    # Changing the background of the weather API - Cloudy day
    cloud = pygame.image.load(CLOUD_ICON)
    cloud_rect = cloud.get_rect().clip(rect)
    
    alpha = cloud.convert_alpha()
    alpha_rect = alpha.get_rect().clip(rect)
    alpha.fill([0,0,0,50])
    
    screen.blit(cloud,cloud_rect)
    screen.blit(alpha,alpha_rect)

    # Let's move each drop of the rain array to simulate the drop is moving
    # In each iteration of the while loop the drop will move one pixel in 
    # y axis
    for drop in rain:
        pygame.draw.line(screen, 
                        drop.colour, 
                        [drop.start_pos.x,drop.start_pos.y], 
                        [drop.end_pos.x,drop.end_pos.y], 
                        drop.thickness)
        
        drop.start_pos.y = drop.start_pos.y + drop.velocity
        drop.end_pos.y = drop.start_pos.y + drop.length

        if drop.start_pos.y > WEATHER_WINDOW_HEIGHT:
            drop.start_pos.x = random.randrange(2, WEATHER_WINDOW_WIDTH - 4)
            drop.end_pos.x = drop.start_pos.x
            drop.start_pos.y = 2
            drop.end_pos.y = drop.start_pos.y + drop.length


def print_cloudy_day(screen, rect):
    # Changing the background of the weather API - Cloudy day
    cloud = pygame.image.load(CLOUD_ICON)
    cloud_rect = cloud.get_rect().clip(rect)
    
    alpha = cloud.convert_alpha()
    alpha_rect = alpha.get_rect().clip(rect)
    alpha.fill([0,0,0,50])
    
    screen.blit(cloud,cloud_rect)
    screen.blit(alpha,alpha_rect)
    

def print_dark_night(screen, rect):
    # Changing the background of the weather API - Night
    night = pygame.image.load(NIGHT_ICON)
    night_rect = night.get_rect().clip(rect)
    
    alpha = night.convert_alpha()
    alpha_rect = alpha.get_rect().clip(rect)
    alpha.fill([0,0,0,50])
    
    screen.blit(night,night_rect)
    screen.blit(alpha,alpha_rect)


def print_cloudy_night(screen, rect):
    # Changing the background of the weather API - Cloudy night
    cloud_night = pygame.image.load(CLOUDY_NIGHT_ICON)
    cloudy_night_rect = cloud_night.get_rect().clip(rect)
    
    alpha = cloud_night.convert_alpha()
    alpha_rect = alpha.get_rect().clip(rect)
    alpha.fill([0,0,0,50])
    
    screen.blit(cloud_night,cloudy_night_rect)
    screen.blit(alpha,alpha_rect)


def print_rainy_night(screen, rect, rain):
    # Changing the background of the weather API - Cloudy night
    cloud_night = pygame.image.load(CLOUDY_NIGHT_ICON)
    cloudy_night_rect = cloud_night.get_rect().clip(rect)
    
    alpha = cloud_night.convert_alpha()
    alpha_rect = alpha.get_rect().clip(rect)
    alpha.fill([0,0,0,50])
    
    screen.blit(cloud_night,cloudy_night_rect)
    screen.blit(alpha,alpha_rect)
    

    # Let's move each drop of the rain array to simulate the drop is moving
    # In each iteration of the while loop the drop will move one pixel in 
    # y axis
    for drop in rain:
        pygame.draw.line(screen, 
                        drop.colour, 
                        [drop.start_pos.x,drop.start_pos.y], 
                        [drop.end_pos.x,drop.end_pos.y], 
                        drop.thickness)
        
        drop.start_pos.y = drop.start_pos.y + drop.velocity
        drop.end_pos.y = drop.start_pos.y + drop.length

        if drop.start_pos.y > WEATHER_WINDOW_HEIGHT:
            drop.start_pos.x = random.randrange(2, WEATHER_WINDOW_WIDTH - 4)
            drop.end_pos.x = drop.start_pos.x
            drop.start_pos.y = 2
            drop.end_pos.y = drop.start_pos.y + drop.length


class CurrentWeather():
    def __init__(self):
        # Initializing the attributes of the class
        self.name           = ""
        self.country        = ""
        self.description    = ""
        self.temp           = 0
        self.feels_like     = 0
        self.humidity       = 0
        self.temp_min       = 0
        self.temp_max       = 0
        self.wind_speed     = 0
        self.cloud_percent  = 0
        self.rain_volume    = 0
        self.snow_volume    = 0
        self.sunrise_hour   = ""
        self.sunset_hour    = ""
        self.timezone       = ""
        self.its_day        = ""
        self.time       = ""

        self.get_weather_info()  
        self.get_time()      
    
    def __calling_the_API(self):
        try:  
            self.req    = urllib.request.Request(API)
            self.resp   = urllib.request.urlopen(self.req)
            self.info   = json.loads(self.resp.read().decode('utf-8'))

            self.resp.close()

        except urllib.error.HTTPError as e:
            pass

    def get_time(self):
        self.time = str(datetime.now().strftime('%H:%M'))

    def get_weather_info(self):   
        # Calling the API
        self.__calling_the_API()
        
        # Getting the city and country
        try: 
            self.name = str(self.info['name'])
            self.country = str(self.info['sys']['country'])
        except: pass

        # Getting info from the JSON response of the API
        try: self.timezone = int(self.info['timezone'])
        except: pass

        # Getting the sunrise and sunset hour info
        if self.timezone:
            try:
                ts = int(self.info['sys']['sunrise'] + self.timezone)
                self.sunrise_hour = datetime.utcfromtimestamp(ts)
            except: pass
            try:
                ts = int(self.info['sys']['sunset'] + self.timezone)
                self.sunset_hour = datetime.utcfromtimestamp(ts)  
            except: pass

        # Getting weather description
        try:
            l = self.info['weather']
            d = dict(l[0]) 
            self.description = str(d['description'])
        except: pass

        # Getting the cloud percentage
        try: self.cloud_percent = int(self.info['clouds']['all'])
        except: pass

        # Getting the rain volume
        try: self.rain_volume = int(self.info['rain']['1h'])
        except: pass

        # Getting the snow volume
        try: self.snow_volume = int(self.info['snow']['1h'])
        except: pass

        # Getting the temperature & humidity
        try: 
            self.temp = int(self.info['main']['temp'])
            self.temp_max = int(self.info['main']['temp_max'])
            self.temp_min = int(self.info['main']['temp_min'])
            self.feels_like = int(self.info['main']['feels_like'])
            self.humidity = int(self.info['main']['humidity'])
        except: pass

        # Getting the wind speed
        try: self.wind_speed = int(self.info['wind']['speed'])
        except: pass

        # Now we change the global variables so we can read them from the interface file
        # and select the simulation to use in the Weather App Button
        now = datetime.now()
        if self.sunrise_hour < now and self.sunset_hour > now:
            self.its_day = True
        else:
            self.its_day = False
        

class Button:
    def __init__(self,text,pos,width,height,elevation,font, color_on, color_off, flip=None, text_color='#FFFFFF', border_radius=6):
    #Core attributes 
        self.pressed = False
        self.elevation = elevation
        self.dynamic_elecation = elevation
        self.original_y_pos = pos[1]
        self.color_on = color_on
        self.color_off = color_off
        self.border_radius = border_radius

        # top rectangle 
        self.top_rect = pygame.Rect(pos,(width,height))
        self.top_color = self.color_off

        # bottom rectangle 
        self.bottom_rect = pygame.Rect(pos,(width,height))
        self.bottom_color = '#354B5E'
        #text
        self.text_surf = font.render(text,True,text_color)
        self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)
        
        if not flip == None:
            if flip == True:
                self.text_surf = pygame.transform.flip(self.text_surf, flip_x = False, flip_y=True)
                #self.text_rect = pygame.transform.flip(self.text_rect, flip_x = False, flip_y=True)

    def draw(self, screen, function):
    # elevation logic 
        self.top_rect.y = self.original_y_pos - self.dynamic_elecation
        self.text_rect.center = self.top_rect.center 

        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elecation

        pygame.draw.rect(screen,self.bottom_color, self.bottom_rect,border_radius = self.border_radius)
        pygame.draw.rect(screen,self.top_color, self.top_rect,border_radius = self.border_radius)
        screen.blit(self.text_surf, self.text_rect)
        self.check_click(function)

    def check_click(self, function):
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = self.color_on
            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elecation = 0
                self.pressed = True
            else:
                self.dynamic_elecation = self.elevation
                if self.pressed == True:
                    function()
                    self.pressed = False
        else:
            self.dynamic_elecation = self.elevation
            self.top_color = self.color_off
        
    def get_Rect(self):
        return self.top_rect
        
# Water drop class - Rain simulation

class Point():
    def __init__(self,x,y):
        self.x = x
        self.y = y
    
class WaterDrop():
    def __init__(self, start_pos, end_pos, length, thickness, colour, velocity = 1):
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.length = length
        self.thickness = thickness
        self.colour = colour
        self.velocity = velocity

    def drop_move():
        pass


# This is the class that will save the state of each item connected in the house
class Items():

    def __init__(self):

        # Home lights and appliances
        self.led        = 0
        self.tv         = 0
        self.air        = [0,21] 
                            # Recive:
                            # [0]           [1]
                            # 0 - Off       Temp
                            # 1 - Cold
                            # 2 - Hot
        self.appliance  = 0
        self.blind      = 0 
                            # 0 Off
                            # 1 Up
                            # 2 Down 

        self.air_onoff      = 0

        self.air_mode_ma    = 0
                            # 0 means MANUAL
                            # 1 means AUTOMATIC
        self.air_mode_ch    = 0
                            # 0 means COLD
                            # 1 means HOT

        # Home settings
        self.wake_hour      = "0000"
        self.no_home_time   = "0000"
        self.back_home_hour = "0000"
        self.sleep_time     = "0000"
        self.temperature    = "00"
        self.temperature_m  = "15"
        self.temperature_M  = "30"
        self.laundry_time_m = "0000"
        self.laundry_time_M = "2400"
        #self.laundry_time   = 

    def get_trama(self):
        t = (
            str(int(1)) + 
            str(int(self.led)) + 
            str(int(self.tv)) + 
            str(int(self.air_mode_ma + 1)) + str(int(self.air[1])) +
            str(int(self.appliance)) + 
            str(int(self.blind))
        )
        return t  
    
    def get_trama_settings(self):
        ts = (
            str(int(2)) + 
            str(self.wake_hour) + str("00") + 
            str(self.no_home_time) + str("00") +
            str(self.back_home_hour) + str("00") + 
            str(self.sleep_time) + str("00") +
            str(self.temperature) + str(self.temperature_m) + str(self.temperature_M) +
            str(self.laundry_time_m) + str("00") + str(self.laundry_time_M) + str("00")         
        )
        return ts


# This is the class for the main window. It contais the buttons that fill the window and the functions that will print them. The simulation of the weather is also defined here. 
class MainWindow():

    def __init__(self):
        self.btn_settings    =   Button("Settings",BTN_SETTINGS_POS,BTN_SETTINGS_WIDTH, BTN_SETTINGS_HEIGHT, BTN_ELEVATION, pygame.font.Font(None,15),SUPER_LIGHT_BLUE,LIGHT_BLUE)
        self.btn_lights      =   Button("Lights", BTN_LIGHTS_POS, BTN_LIGHTS_WIDTH, BTN_LIGHTS_HEIGHT, BTN_ELEVATION, pygame.font.Font(None,15),SUPER_LIGHT_BLUE,LIGHT_BLUE)
        self.btn_tv          =   Button("TV", BTN_TV_POS, BTN_TV_WIDTH, BTN_TV_HEIGHT, BTN_ELEVATION, pygame.font.Font(None,15),SUPER_LIGHT_BLUE,LIGHT_BLUE)
        self.btn_air         =   Button("Air", BTN_AIR_POS, BTN_AIR_WIDTH, BTN_AIR_HEIGHT, BTN_ELEVATION, pygame.font.Font(None,15),SUPER_LIGHT_BLUE,LIGHT_BLUE)
        self.btn_appliance   =   Button("Appliance", BTN_APPLIANCE_POS, BTN_AIR_WIDTH, BTN_APPLIANCE_HEIGHT, BTN_ELEVATION, pygame.font.Font(None,15),SUPER_LIGHT_BLUE,LIGHT_BLUE)
        self.btn_blinds      =   Button("Blinds", BTN_BLINDS_POS, BTN_BLINDS_WIDTH, BTN_BLINDS_HEIGHT, BTN_ELEVATION, pygame.font.Font(None,15),SUPER_LIGHT_BLUE,LIGHT_BLUE)
        self.btn_weather     =   Button("Weather", BTN_WEATHER_POS, BTN_WEATHER_WIDTH,BTN_WEATHER_HEIGHT,1,pygame.font.Font(None,30), SUPER_LIGHT_BLUE,LIGHT_BLUE)

    def print_main_window(self, screen, functions, cw, rain):
        self.btn_weather.draw(screen, functions[0])
        self.btn_lights.draw(screen, functions[1])
        self.btn_tv.draw(screen, functions[2])
        self.btn_air.draw(screen, functions[3])
        self.btn_appliance.draw(screen, functions[4])
        self.btn_blinds.draw(screen, functions[5])
        self.btn_settings.draw(screen, functions[6])

        self.do_weather_simulations(screen, cw, rain)


    def do_weather_simulations(self, screen, cw, rain):
        mx,my = pygame.mouse.get_pos()
        if (mx>2 and mx<WEATHER_WINDOW_WIDTH and my>2 and my<WEATHER_WINDOW_HEIGHT - 2) :
            if cw.its_day:
                if cw.rain_volume > VALID_RAIN_RATE:
                    print_rainy_day(screen, self.btn_weather.get_Rect(), rain)
                elif cw.cloud_percent > VALID_CLOUD_RATE: 
                    print_cloudy_day(screen, self.btn_weather.get_Rect())
                else:
                    print_sunny_day(screen, self.btn_weather.get_Rect())            
            else: 
                if cw.rain_volume > VALID_RAIN_RATE:
                    print_rainy_day(screen, self.btn_weather.get_Rect(), rain)
                elif cw.cloud_percent > VALID_CLOUD_RATE: 
                    print_cloudy_day(screen, self.btn_weather.get_Rect())
                else:
                    print_dark_night(screen, self.btn_weather.get_Rect())

            offset = 15

            location_text = pygame.font.Font(None,30).render(str(cw.name) + ", " + str(cw.country), True, WHITE)
            location_rect = location_text.get_rect(center=(WEATHER_WINDOW_WIDTH/2, 0*WEATHER_WINDOW_HEIGHT/5 + offset))
            screen.blit(location_text,location_rect)

            temp_text = pygame.font.Font(None,50).render(str(cw.temp) + "ºC", True, WHITE)
            temp_rect = temp_text.get_rect(center=(WEATHER_WINDOW_WIDTH/2,1*WEATHER_WINDOW_HEIGHT/5 + offset))
            screen.blit(temp_text,temp_rect)
            
            description_text = pygame.font.Font(None,30).render(str(cw.description), True, WHITE)
            description_rect = description_text.get_rect(center=(WEATHER_WINDOW_WIDTH/2,2*WEATHER_WINDOW_HEIGHT/5 + offset))
            screen.blit(description_text,description_rect)

            text = str("max: ")  + str(cw.temp_max) + "º  " + "min: " + str(cw.temp_min) + "º"
            temp_minmax_text = pygame.font.Font(None,20).render(text, True, WHITE)
            temp_minmax_rect = temp_minmax_text.get_rect(center=(WEATHER_WINDOW_WIDTH/2,3*WEATHER_WINDOW_HEIGHT/5 + 5))
            screen.blit(temp_minmax_text,temp_minmax_rect)

            time_text = pygame.font.Font(None,30).render(str(cw.time), True, WHITE)
            time_rect = time_text.get_rect(center=(WEATHER_WINDOW_WIDTH/2, 4*WEATHER_WINDOW_HEIGHT/5 + 5))
            screen.blit(time_text, time_rect)
        
        # Let's just update the surface we are changing in order to save CPU time
        pygame.display.update(self.btn_weather.get_Rect())


class WeatherWindow():
    def __init__(self):
        # Button for going back to main window
        self.go_back_button =   Button("<-", BTN_GO_BACK_POS, BTN_GO_BACK_WIDTH, BTN_GO_BACK_HEIGHT, BTN_ELEVATION, pygame.font.Font(None,15),SUPER_LIGHT_BLUE,LIGHT_BLUE)

    def print_weather_window(self, screen, functions):
        self.go_back_button.draw(screen, functions[0])


class LightsWindow():

    def __init__(self):
        # Button for going back to main window
        self.go_back_button =   Button("<-", BTN_GO_BACK_POS, BTN_GO_BACK_WIDTH, BTN_GO_BACK_HEIGHT, BTN_ELEVATION, pygame.font.Font(None,15),SUPER_LIGHT_BLUE,LIGHT_BLUE)      
    
        # Setting light plan
        self.light_plan_img =   pygame.image.load(LIGHTS_WINDOW_BG)
        self.light_plan_rect=   self.light_plan_img.get_rect(center=(WINDOW_SIZE[0]/2, WINDOW_SIZE[1]/2))

    def print_lights_window(self, screen, functions, items):
        screen.blit(self.light_plan_img, self.light_plan_rect)
        self.go_back_button.draw(screen, functions[0])

        tr = self.check_light_status(items)
        self.print_indicator(screen, items)
        self.do_lights_simulation(screen, items)

        return tr

    def check_light_status(self, items):
        global last_mouse_state
        mx, my = pygame.mouse.get_pos()
        if mx > 240 and mx < 260 and my > 225 and my < 245: 
            mouse_state = pygame.mouse.get_pressed()
            last_mouse_state += 1
            if mouse_state[0] == True and last_mouse_state > 25:
                if items.led == 1:
                    items.led = 0
                elif items.led == 0:
                    items.led = 1
                last_mouse_state = 0
                tr = items.get_trama()
                return tr
            else:
                tr = str(int(0))
                return tr
            
        else:
            tr = str(int(0))
            return tr
    
    def print_indicator(self,screen, items):
        if items.led == 1:
            tv_text = pygame.font.Font(None,20).render("LED On", True, [50,250, 50])
            tv_rect = tv_text.get_rect(left=230, top=210)
        else:
            tv_text = pygame.font.Font(None,20).render("LED Off", True, [250, 50, 50])
            tv_rect = tv_text.get_rect(left=230, top=210)
        
        screen.blit(tv_text, tv_rect)
        

    def do_lights_simulation(self,screen,items):
        if items.led == 1:
            pygame.draw.circle(surface=screen, color = pygame.Color(255,255,0), center=(250, 235), radius = 8)
            

class TVWindow():
    def __init__(self):
        # Button for going back to main window
        self.go_back_button =   Button("<-", BTN_GO_BACK_POS, BTN_GO_BACK_WIDTH, BTN_GO_BACK_HEIGHT, BTN_ELEVATION, pygame.font.Font(None,15),SUPER_LIGHT_BLUE,LIGHT_BLUE)

        # Setting TV plan
        self.tv_plan_img    =   pygame.image.load(TV_WINDOW_BG)
        self.tv_plan_rect   =   self.tv_plan_img.get_rect(center=(WINDOW_SIZE[0]/2, WINDOW_SIZE[1]/2))

    def print_tv_window(self, screen, functions, items):
        screen.blit(self.tv_plan_img, self.tv_plan_rect)
        self.go_back_button.draw(screen, functions[0])

        tr = self.check_tv_status(items)
        self.print_tv_indicator(screen,items)
        self.do_tv_simulation(screen, items)

        return tr

    def check_tv_status(self, items):
        global last_mouse_state
        mx, my = pygame.mouse.get_pos()
        if mx > 35 and mx < 85 and my > 270 and my < 400: 
            mouse_state = pygame.mouse.get_pressed()
            last_mouse_state += 1
            if mouse_state[0] == True and last_mouse_state > 25:
                if items.tv == 1:
                    items.tv = 0
                elif items.tv == 0:
                    items.tv = 1
                last_mouse_state = 0
                tr = items.get_trama()
                return tr
            else:
                tr = str(int(0))
                return tr
            
        else:
            tr = str(int(0))
            return tr

    def print_tv_indicator(self, screen, items):
        if items.tv == True:
            tv_text = pygame.font.Font(None,20).render("TV On", True, [50,255,50])
            tv_rect = tv_text.get_rect(left=35,top=260)
        else:
            tv_text = pygame.font.Font(None,20).render("TV Off", True, [250,50,50])
            tv_rect = tv_text.get_rect(left=35,top=260)
            
        screen.blit(tv_text, tv_rect)
    
    def do_tv_simulation(self,screen, items):
        if items.tv == True:
            pygame.draw.rect(surface=screen, color=LIGHT_BLUE, rect=(45,285,25,110),width=0)


class AirWindow():
    def __init__(self):
        # Button for going back to main window
        self.go_back_button =   Button("<-", BTN_GO_BACK_POS, BTN_GO_BACK_WIDTH, BTN_GO_BACK_HEIGHT, BTN_ELEVATION, pygame.font.Font(None,15),SUPER_LIGHT_BLUE,LIGHT_BLUE)

        # Air Mode and up down temperature
        self.on_mode        = Button("ON", BTN_AIR_ON_POS, BTN_AIR_ON_WIDTH, BTN_AIR_ON_HEIGHT, 0,pygame.font.Font(None,20), GREY, GREY, border_radius=0)
        self.off_mode       = Button("OFF", BTN_AIR_OFF_POS, BTN_AIR_OFF_WIDTH, BTN_AIR_OFF_HEIGHT, 0, pygame.font.Font(None,20), GREY, GREY, border_radius=0)
        self.manual_mode    = Button("MAN", BTN_AIR_MAN_POS, BTN_AIR_MAN_WIDTH, BTN_AIR_MAN_HEIGHT, 0, pygame.font.Font(None,20), GREY, GREY, border_radius=0)
        self.automatic_mode = Button("AUTO", BTN_AIR_AUTO_POS, BTN_AIR_AUTO_WIDTH, BTN_AIR_AUTO_HEIGHT, 0, pygame.font.Font(None,20), GREY, GREY, border_radius=0)

        # Up and down temp
        self.air_up         = Button("^", BTN_AIR_UP_POS, BTN_AIR_UP_WIDTH, BTN_AIR_UP_HEIGHT, 0, pygame.font.Font(None,30), GREY, GREY, border_radius=0)
        self.air_down       = Button("^", BTN_AIR_DOWN_POS, BTN_AIR_DOWN_WIDTH, BTN_AIR_DOWN_HEIGHT, 0, pygame.font.Font(None,30), GREY, GREY, flip=True, border_radius=0)

        # Setting Air plan
        self.air_plan_img   = pygame.image.load(AIR_WINDOW_BG)
        self.air_plan_rect  = self.air_plan_img.get_rect(center=(WINDOW_SIZE[0]/2, WINDOW_SIZE[1]/2))

    def print_air_window(self, screen, functions, items): 
        # Printing Go back button
        screen.blit(self.air_plan_img, self.air_plan_rect)
        self.go_back_button.draw(screen, functions[0])

        # Checking the air button
        #tr = self.check_air_status(items)

        # Checking if we print ON or OFF button
        if items.air[0] == 0:   
            self.on_mode.draw(screen,functions[1])
        elif not items.air[0] == 0:
            self.off_mode.draw(screen,functions[1])
        
        # Checking if we print MAN or AUTO button
        if items.air_mode_ma == 0:
            self.automatic_mode.draw(screen,functions[2])
        elif items.air_mode_ma == 1:
            self.manual_mode.draw(screen,functions[2])

        # Printing up down temperature
        self.air_up.draw(screen,functions[3])
        self.air_down.draw(screen,functions[4])
        
        # Printing temperature text
        pygame.draw.rect(screen, GREY, (194,312,40,60), border_radius=0)
        temp_text = pygame.font.Font(None,25).render(str(items.air[1]), True, WHITE)
        temp_rect = temp_text.get_rect(left=207,top=332)
        screen.blit(temp_text,temp_rect)

        # Printing separation
        pygame.draw.line(screen,DARK_GREY,(125,341),(170,341),2)

        self.print_air_indicator(screen, items)
        self.do_air_simulation(screen, items)

        #return tr

    def check_air_status(self, items):
        global last_mouse_state
        mx, my = pygame.mouse.get_pos()
        if (
            (mx > 130 and mx < 165 and my > 390 and my < 430) or 
            (items.air_onoff == 1)
            ): 
            mouse_state = pygame.mouse.get_pressed()
            last_mouse_state += 1
            if mouse_state[0] == True and last_mouse_state > 25:
                if items.air[0] == 1:
                    items.air[0] = 0
                elif items.air[0] == 0:
                    items.air[0] = 1
                last_mouse_state = 0
                tr = items.get_trama()
                return tr
            else:
                tr = str(int(0))
                return tr
            
        else:
            tr = str(int(0))
            return tr
    
    def print_air_indicator(self,screen, items):
        if items.air[0] == 0:
            air_text = pygame.font.Font(None, 20).render("Air Off", True, RED)
            air_rect = air_text.get_rect(left=130, top=380)
        elif items.air[0] == 1:
            air_text = pygame.font.Font(None, 20).render("Air On - COLD", True, GREEN)
            air_rect = air_text.get_rect(left=130, top=380)
        elif items.air[0] == 2:    
            air_text = pygame.font.Font(None, 20).render("Air On - HOT", True, GREEN)
            air_rect = air_text.get_rect(left=130, top=380)

        screen.blit(air_text, air_rect)

    def do_air_simulation(self,screen, items):
        if items.air[0] == 1:       # Cold air
            pygame.draw.circle(screen, BLUE, center=(140,400), radius=8)
        
        elif items.air[0] == 2:     # Heat air
            pygame.draw.circle(screen, RED, center=(156,400), radius=8)
        

class ApplianceWindow():
    def __init__(self):
        # Button for going back to main window
        self.go_back_button =   Button("<-", BTN_GO_BACK_POS, BTN_GO_BACK_WIDTH, BTN_GO_BACK_HEIGHT, BTN_ELEVATION, pygame.font.Font(None,15),SUPER_LIGHT_BLUE,LIGHT_BLUE)
    
        # Setting Appliance plan
        self.aplliance_plan_img = pygame.image.load(APPLIANCE_WIN_BG)
        self.aplliance_plan_rect= self.aplliance_plan_img.get_rect(center=(WINDOW_SIZE[0]/2, WINDOW_SIZE[1]/2))

    def print_appliance_window(self, screen, functions, items):
        screen.blit(self.aplliance_plan_img, self.aplliance_plan_rect)
        self.go_back_button.draw(screen, functions[0])

        tr = self.check_appliance_status(items)
        self.print_appliance_indicator(screen, items)
        self.do_appliance_simulation(screen, items)

        return tr

    def check_appliance_status(self, items):
        global last_mouse_state
        mx, my = pygame.mouse.get_pos()
        if mx > 165 and mx < 275 and my > 350 and my < 420: 
            mouse_state = pygame.mouse.get_pressed()
            last_mouse_state += 1
            if mouse_state[0] == True and last_mouse_state > 25:
                if items.appliance == 1:
                    items.appliance = 0
                elif items.appliance == 0:
                    items.appliance = 1
                last_mouse_state = 0
                tr = items.get_trama()
                return tr
            else:
                tr = str(int(0))
                return tr
        else:
            tr = str(int(0))
            return tr

    def print_appliance_indicator(self,screen,items):
        if items.appliance == True:
            appliance_text = pygame.font.Font(None,20).render("Washing Machine On", True, [50,250,50])
            appliance_rect = appliance_text.get_rect(left=160, top=340)
        else:
            appliance_text = pygame.font.Font(None,20).render("Washing Machine Off", True, [250,50,50])
            appliance_rect = appliance_text.get_rect(left=160, top=340)
        screen.blit(appliance_text, appliance_rect)

    def do_appliance_simulation(self,screen, items):
        if items.appliance == True:
            # pygame.draw.rect(screen, [200,200,200], pygame.Rect(190,360,70,50))
            pass


class BlindWindow():
    def __init__(self):
        # Button for going back to main window
        self.go_back_button =   Button("<-", BTN_GO_BACK_POS, BTN_GO_BACK_WIDTH, BTN_GO_BACK_HEIGHT, BTN_ELEVATION, pygame.font.Font(None,15),SUPER_LIGHT_BLUE,LIGHT_BLUE)

        # Setting Blind plan
        self.blind_plan_img =   pygame.image.load(BLIND_WINDOW_BG)
        self.blind_plan_rect=   self.blind_plan_img.get_rect(center=(WINDOW_SIZE[0]/2, WINDOW_SIZE[1]/2))

        # Defining Buttons
        self.blind_up         = Button("^", BTN_BLIND_UP_POS, BTN_BLIND_UP_WIDTH, BTN_BLIND_UP_HEIGHT, 0, pygame.font.Font(None,30), GREY, GREY, border_radius=0)
        self.blind_down       = Button("^", BTN_BLIND_DOWN_POS, BTN_BLIND_DOWN_WIDTH, BTN_BLIND_DOWN_HEIGHT, 0, pygame.font.Font(None,30), GREY, GREY, flip=True, border_radius=0)


    def print_blind_window(self, screen, functions, items):
        screen.blit(self.blind_plan_img, self.blind_plan_rect)
        self.go_back_button.draw(screen, functions[0])

        # Print blind buttons         
        self.blind_up.draw(screen,functions[1])
        self.blind_down.draw(screen,functions[2])

        # Print separation  
        pygame.draw.line(screen,DARK_GREY,(62,94),(98,94),2)

        #tr = self.check_blind_status(items)
        self.print_blind_indicator(screen,items)
        self.do_blind_simulation(screen,items)

        tr = items.get_trama()
        return tr

    def check_blind_status(self,items):
        mx, my = pygame.mouse.get_pos()
        if mx > 25 and mx < 50 and my > 15 and my < 160: 
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    items.blind = not items.blind

    def print_blind_indicator(self,screen,items):
        if items.blind == 0:
            blind_text = pygame.font.Font(None,20).render("Blind Going Off",True, [250,50,50])
            blind_rect = blind_text.get_rect(left=35, top=25)
        elif items.blind == 1:
            blind_text = pygame.font.Font(None,20).render("Blind Going up",True, [50,250,50])
            blind_rect = blind_text.get_rect(left=35, top=25)
        elif items.blind == 2:
            blind_text = pygame.font.Font(None,20).render("Blind Going down",True, [50,250,50])
            blind_rect = blind_text.get_rect(left=35, top=25)            

        screen.blit(blind_text,blind_rect)

    def do_blind_simulation(self,screen,items):
        if items.blind == True:
            pass

class Slider():
    def __init__(self, screen, text, tam_text, text_color, text_pos, 
                bar_color, bar_pos, bar_width, bar_height, left_bar_text, left_bar_text_pos, right_bar_text, right_bar_text_pos,
                slider_color, slider_pos, slider_width, slider_height,
                division = 100, info=False, info_pos=None, offset=0, button_control=0):

        self.data = str("00")

        self.mark = slider_pos[0]

        self.screen = screen
        self.bar_color = bar_color
        self.bar_pos = bar_pos
        self.bar_width = bar_width
        self.bar_height = bar_height
        self.slider_color = slider_color
        self.slider_width = slider_width
        self.slider_height = slider_height
        self.slider_pos = slider_pos
        self.division = division
        self.offset = offset
        self.button_control = button_control

        self.text = pygame.font.Font(None,tam_text).render(text, True, text_color)
        self.rect = self.text.get_rect(center=(text_pos[0],text_pos[1]))
    
        
        if info==True and not info_pos==None:
            self.info_img   = pygame.image.load(INFO_ICON)
            self.info_rect  = self.info_img.get_rect(left=info_pos[0], top=info_pos[1])
            
                
               
        self.zero_wh_text = pygame.font.Font(None,15).render(left_bar_text, True, BLACK)
        self.zero_wh_rect = self.zero_wh_text.get_rect(left=left_bar_text_pos[0],top=left_bar_text_pos[1])    
        
        self.tfour_wh_text= pygame.font.Font(None,15).render(right_bar_text, True, BLACK)
        self.tfour_wh_rect= self.zero_wh_text.get_rect(left=right_bar_text_pos[0], top=right_bar_text_pos[1])

    def draw(self):   
        pygame.draw.rect(self.screen, self.bar_color, (self.bar_pos[0],self.bar_pos[1],self.bar_width,self.bar_height))
        pygame.draw.rect(self.screen, self.slider_color, (self.mark,self.slider_pos[1],self.slider_width,self.slider_height))
        
        if self.offset==0:
            self.mark_text = pygame.font.Font(None,15).render(str(int(self.division*((self.mark-self.bar_pos[0]+5)/self.bar_width))), True, BLACK)
        else:
            self.mark_text = pygame.font.Font(None,15).render(str(int(self.division*((self.mark-self.bar_pos[0]+5)/self.bar_width))+self.offset), True, BLACK)
        self.mark_rect = self.mark_text.get_rect(left=self.mark, top=self.bar_pos[1]+12)

        self.screen.blit(self.text,self.rect)                    # Print the slider text
        self.screen.blit(self.info_img, self.info_rect)          # Print the info button
        self.screen.blit(self.mark_text, self.mark_rect)         # Print the mark indicator  - slider pos
        self.screen.blit(self.zero_wh_text, self.zero_wh_rect)   # Print the left indicator  - limit
        self.screen.blit(self.tfour_wh_text, self.tfour_wh_rect) # Print the right indicator - limit

        if pygame.mouse.get_pressed()[self.button_control]:
            mx,my = pygame.mouse.get_pos()

            if mx > self.bar_pos[0] and mx < (self.bar_pos[0]+self.bar_width) and my > self.slider_pos[1] and my < self.slider_pos[1] + self.slider_height:
                self.mark = mx 
                self.data = str(int(self.division*((self.mark-self.bar_pos[0]+5)/self.bar_width)) + int(self.offset))

        return self.data


class SettingsWindow():
    def __init__(self, screen):
        # Button for going back to main window
        self.go_back_button         = Button("<-", BTN_GO_BACK_POS, BTN_GO_BACK_WIDTH, BTN_GO_BACK_HEIGHT, BTN_ELEVATION, pygame.font.Font(None,15),SUPER_LIGHT_BLUE,LIGHT_BLUE)
        self.send_setting_button    = Button("Save", BTN_SEND_DATA_POS, BTN_SEND_DATA_WIDTH, BTN_SEND_DATA_HEIGHT,BTN_ELEVATION, pygame.font.Font(None,20), SUPER_LIGHT_BLUE, LIGHT_BLUE)       

        self.wh_slider = Slider(screen,WH_TEXT,WH_TEXT_TAM,WH_TEXT_COLOR,WH_TEXT_POS,
                                WH_BAR_COLOR,WH_BAR_POS,WH_BAR_WIDTH,WH_BAR_HEIGHT,WH_LEFT_BAR_TEXT,WH_LEFT_BAR_TEXT_POS,WH_RIGHT_BAR_TEXT,WH_RIGHT_BAR_TEXT_POS,
                                WH_SLIDER_COLOR,WH_SLIDER_POS,WH_SLIDER_WIDTH,WH_SLIDER_HEIGHT,
                                DIV,info=True,info_pos = WH_INFO_POS)

        self.nh_slider = Slider(screen,NH_TEXT,NH_TEXT_TAM,NH_TEXT_COLOR,NH_TEXT_POS,
                                NH_BAR_COLOR,NH_BAR_POS,NH_BAR_WIDTH,NH_BAR_HEIGHT,NH_LEFT_BAR_TEXT,NH_LEFT_BAR_TEXT_POS,NH_RIGHT_BAR_TEXT,NH_RIGHT_BAR_TEXT_POS,
                                NH_SLIDER_COLOR,NH_SLIDER_POS,NH_SLIDER_WIDTH,NH_SLIDER_HEIGHT,
                                DIV,info=True,info_pos = NH_INFO_POS)

        self.bh_slider = Slider(screen,BH_TEXT,BH_TEXT_TAM,BH_TEXT_COLOR,BH_TEXT_POS,
                                BH_BAR_COLOR,BH_BAR_POS,BH_BAR_WIDTH,BH_BAR_HEIGHT,BH_LEFT_BAR_TEXT,BH_LEFT_BAR_TEXT_POS,BH_RIGHT_BAR_TEXT,BH_RIGHT_BAR_TEXT_POS,
                                BH_SLIDER_COLOR,BH_SLIDER_POS,BH_SLIDER_WIDTH,BH_SLIDER_HEIGHT,
                                DIV,info=True,info_pos = BH_INFO_POS)

        self.st_slider = Slider(screen,ST_TEXT,ST_TEXT_TAM,ST_TEXT_COLOR,ST_TEXT_POS,
                                ST_BAR_COLOR,ST_BAR_POS,ST_BAR_WIDTH,ST_BAR_HEIGHT,ST_LEFT_BAR_TEXT,ST_LEFT_BAR_TEXT_POS,ST_RIGHT_BAR_TEXT,ST_RIGHT_BAR_TEXT_POS,
                                ST_SLIDER_COLOR,ST_SLIDER_POS,ST_SLIDER_WIDTH,ST_SLIDER_HEIGHT,
                                DIV,info=True,info_pos = ST_INFO_POS)

        self.t_slider  = Slider(screen,T_TEXT,T_TEXT_TAM,T_TEXT_COLOR,T_TEXT_POS,
                                T_BAR_COLOR,T_BAR_POS,T_BAR_WIDTH,T_BAR_HEIGHT,T_LEFT_BAR_TEXT,T_LEFT_BAR_TEXT_POS,T_RIGHT_BAR_TEXT,T_RIGHT_BAR_TEXT_POS,
                                T_SLIDER_COLOR,T_SLIDER_POS,T_SLIDER_WIDTH,T_SLIDER_HEIGHT,
                                15,info=True,info_pos = T_INFO_POS,offset=15)

        self.trm_slider= Slider(screen,TR_TEXT,TR_TEXT_TAM,TR_TEXT_COLOR,TR_TEXT_POS,
                                TR_BAR_COLOR,TR_BAR_POS,TR_BAR_WIDTH,TR_BAR_HEIGHT,TR_LEFT_BAR_TEXT,TR_LEFT_BAR_TEXT_POS,TR_RIGHT_BAR_TEXT,TR_RIGHT_BAR_TEXT_POS,
                                TR_SLIDER_COLOR,TR_SLIDER_POS,TR_SLIDER_WIDTH,TR_SLIDER_HEIGHT,
                                15,info=True,info_pos = TR_INFO_POS,offset=15,button_control=0)
        
        self.trM_slider= Slider(screen,TRM_TEXT,TRM_TEXT_TAM,TRM_TEXT_COLOR,TRM_TEXT_POS,
                                TRM_BAR_COLOR,TRM_BAR_POS,TRM_BAR_WIDTH,TRM_BAR_HEIGHT,TRM_LEFT_BAR_TEXT,TRM_LEFT_BAR_TEXT_POS,TRM_RIGHT_BAR_TEXT,TRM_RIGHT_BAR_TEXT_POS,
                                TRM_SLIDER_COLOR,TRM_SLIDER_POS,TRM_SLIDER_WIDTH,TRM_SLIDER_HEIGHT,
                                15,info=True,info_pos = TRM_INFO_POS,offset=15,button_control=2)

        self.lt_slider = Slider(screen,LT_TEXT,LT_TEXT_TAM,LT_TEXT_COLOR,LT_TEXT_POS,
                                LT_BAR_COLOR,LT_BAR_POS,LT_BAR_WIDTH,LT_BAR_HEIGHT,LT_LEFT_BAR_TEXT,LT_LEFT_BAR_TEXT_POS,LT_RIGHT_BAR_TEXT,LT_RIGHT_BAR_TEXT_POS,
                                LT_SLIDER_COLOR,LT_SLIDER_POS,LT_SLIDER_WIDTH,LT_SLIDER_HEIGHT,
                                DIV,info=True,info_pos = LT_INFO_POS, button_control=0)

        self.ltm_slider = Slider(screen,LTM_TEXT,LTM_TEXT_TAM,LTM_TEXT_COLOR,LTM_TEXT_POS,
                                LTM_BAR_COLOR,LTM_BAR_POS,LTM_BAR_WIDTH,LTM_BAR_HEIGHT,LTM_LEFT_BAR_TEXT,LTM_LEFT_BAR_TEXT_POS,LTM_RIGHT_BAR_TEXT,LTM_RIGHT_BAR_TEXT_POS,
                                LTM_SLIDER_COLOR,LTM_SLIDER_POS,LTM_SLIDER_WIDTH,LTM_SLIDER_HEIGHT,
                                DIV,info=True,info_pos = LTM_INFO_POS, button_control=2)

    def print_settings_window(self, screen, functions, items):
        # Go back button
        self.go_back_button.draw(screen, functions[0])
        self.send_setting_button.draw(screen, functions[1])
       
        # Title text
        self.setting_text = pygame.font.Font(None,40).render("SETTINGS", True, BLACK)
        self.setting_rect = self.setting_text.get_rect(center=(WINDOW_SIZE[0]/2, 15))
        screen.blit(self.setting_text,self.setting_rect)

        # Wake hour slider
        items.wake_hour     = self.wh_slider.draw()
        if len(items.wake_hour) < 2: items.wake_hour = str(int(0)) + items.wake_hour

        items.no_home_time  = self.nh_slider.draw()
        if len(items.no_home_time) < 2: items.no_home_time = str(int(0)) + items.no_home_time

        items.back_home_hour= self.bh_slider.draw()
        if len(items.back_home_hour) < 2: items.back_home_hour = str(int(0)) + items.back_home_hour
        
        items.sleep_time    = self.st_slider.draw()
        if len(items.sleep_time) < 2: items.sleep_time = str(int(0)) + items.sleep_time

        items.temperature   = self.t_slider.draw()
        items.temperature_m = self.trm_slider.draw()
        items.temperature_M = self.trM_slider.draw()
        
        items.laundry_time_m= self.lt_slider.draw()
        if len(items.laundry_time_m) < 2: items.laundry_time_m = str(int(0)) + items.laundry_time_m

        items.laundry_time_M= self.ltm_slider.draw()
        if len(items.laundry_time_M) < 2: items.laundry_time_M = str(int(0)) + items.laundry_time_M

        # if pressed == True:
        #     pressed = False
        #     return items.get_trama_settings(), pressed
        # else:
        #     return str(int(0)), pressed