
import pygame, random, json
import urllib.error, urllib.request 


from tramas import *
from lib import *
from datetime import datetime

def print_sunny_day(screen, rect):
    # Changing the background of the weather API - Sunny day
    sun = pygame.image.load(SUN_ICON)
    sun_rect = sun.get_rect().clip(rect)
    
    screen.blit(sun,sun_rect)


def print_rainy_day(screen, rect, rain):
    # Changing the background of the weather API - Cloudy day
    cloud = pygame.image.load(CLOUD_ICON)
    cloud_rect = cloud.get_rect().clip(rect)
    
    screen.blit(cloud,cloud_rect)

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
    alpha.fill([0,0,0,100])
    
    screen.blit(cloud,cloud_rect)
    screen.blit(alpha,alpha_rect)
    

def print_dark_night(screen, rect):
    # Changing the background of the weather API - Night
    night = pygame.image.load(NIGHT_ICON)
    night_rect = night.get_rect().clip(rect)
    
    screen.blit(night,night_rect)


def print_cloudy_night(screen, rect):
    # Changing the background of the weather API - Cloudy night
    cloud_night = pygame.image.load(CLOUDY_NIGHT_ICON)
    cloudy_night_rect = cloud_night.get_rect().clip(rect)
    
    screen.blit(cloud_night,cloudy_night_rect)


def print_rainy_night(screen, rect, rain):
    # Changing the background of the weather API - Cloudy night
    cloud_night = pygame.image.load(CLOUDY_NIGHT_ICON)
    cloudy_night_rect = cloud_night.get_rect().clip(rect)
    
    screen.blit(cloud_night,cloudy_night_rect)

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

        self.get_weather_info()        
    
    def __calling_the_API(self):
        try:  
            self.req    = urllib.request.Request(API)
            self.resp   = urllib.request.urlopen(self.req)
            self.info   = json.loads(self.resp.read().decode('utf-8'))

            self.resp.close()

        except urllib.error.HTTPError as e:
            pass

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
    def __init__(self,text,pos,width,height,elevation,font, color_on, color_off):
    #Core attributes 
        self.pressed = False
        self.elevation = elevation
        self.dynamic_elecation = elevation
        self.original_y_pos = pos[1]
        self.color_on = color_on
        self.color_off = color_off

        # top rectangle 
        self.top_rect = pygame.Rect(pos,(width,height))
        self.top_color = self.color_off

        # bottom rectangle 
        self.bottom_rect = pygame.Rect(pos,(width,height))
        self.bottom_color = '#354B5E'
        #text
        self.text_surf = font.render(text,True,'#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)

    def draw(self, screen, function):
    # elevation logic 
        self.top_rect.y = self.original_y_pos - self.dynamic_elecation
        self.text_rect.center = self.top_rect.center 

        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elecation

        pygame.draw.rect(screen,self.bottom_color, self.bottom_rect,border_radius = 6)
        pygame.draw.rect(screen,self.top_color, self.top_rect,border_radius = 6)
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

    # Default temperature
    default_temperature = 21
    blind_top = 15

    def __init__(self):
        self.led        = 0
        self.tv         = 0
        self.air        = [21,0] # First value is to check temperature the air is working at, second if it's on or off
        self.appliance  = 0
        self.blind      = [0,0] # First value is to check the height the blinds are at, second is to known it's 

    def get_trama(self):
        t = str(int(self.led))+str(int(self.tv))+str(int(self.air[1]))+str(int(self.appliance))+str(int(self.blind[1]))
        return t  


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
            if mouse_state[0] == True and last_mouse_state > 25:
                if items.led == 1:
                    items.led = 0
                elif items.led == 0:
                    items.led = 1
                last_mouse_state = 0
                tr = str(1) + items.get_trama()
                return tr
            last_mouse_state += 1
        else:
            tr = str(0)
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

        self.check_tv_status(items)
        self.print_tv_indicator(screen,items)
        self.do_tv_simulation(screen, items)
    
    def check_tv_status(self, items):
        mx, my = pygame.mouse.get_pos()
        if mx >35 and mx < 85 and my > 270 and my < 400:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    items.tv = not items.tv

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

        # Setting Air plan
        self.air_plan_img   = pygame.image.load(AIR_WINDOW_BG)
        self.air_plan_rect  = self.air_plan_img.get_rect(center=(WINDOW_SIZE[0]/2, WINDOW_SIZE[1]/2))

    def print_air_window(self, screen, functions, items): 
        screen.blit(self.air_plan_img, self.air_plan_rect)
        self.go_back_button.draw(screen, functions[0])

        self.check_air_status(items)
        self.print_air_indicator(screen, items)
        self.do_air_simulation(screen, items)

    def check_air_status(self, items):
        mx, my = pygame.mouse.get_pos()
        if mx > 130 and mx < 165 and my > 390 and my < 430:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    items.air[1] = not items.air[1]
    
    def print_air_indicator(self,screen, items):
        if items.air[1] == True:
            air_text = pygame.font.Font(None, 20).render("Air On", True, [50,250,50])
            air_rect = air_text.get_rect(left=130, top=380)
        else:
            air_text = pygame.font.Font(None, 20).render("Air Off", True, [250,50,50])
            air_rect = air_text.get_rect(left=130, top=380)

        screen.blit(air_text, air_rect)

    def do_air_simulation(self,screen, items):
        if items.air[1] == True:                                        # Air on
            if items.air[0] < items.default_temperature:                # Cold air
                pygame.draw.circle(surface=screen, color=[50,50,250], center=(140,400), radius=8)
            elif items.air[0] > items.default_temperature:                # Heat air
                pygame.draw.circle(screen, [250,50,50], (156,400), 8)
            else:                                                       # If the default temperature is equal to the temperature selected
                pygame.draw.circle(screen, [50,50,250], (140,400), 8)
                pygame.draw.circle(screen, [250,50,50], (156,400), 8)
        

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

        self.check_appliance_status(items)
        self.print_appliance_indicator(screen, items)
        self.do_appliance_simulation(screen, items)

    def check_appliance_status(self, items):
        mx, my = pygame.mouse.get_pos()
        if mx > 165 and mx < 275 and my > 350 and my < 420: 
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    items.appliance = not items.appliance

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

    def print_blind_window(self, screen, functions, items):
        screen.blit(self.blind_plan_img, self.blind_plan_rect)
        self.go_back_button.draw(screen, functions[0])

        self.check_blind_status(items)
        self.print_blind_indicator(screen,items)
        self.do_blind_simulation(screen,items)

    def check_blind_status(self,items):
        mx, my = pygame.mouse.get_pos()
        if mx > 25 and mx < 50 and my > 15 and my < 160: 
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    items.blind[1] = not items.blind[1]

    def print_blind_indicator(self,screen,items):
        if items.blind[1] == True:                  # Blinds On
            if items.blind[0] < items.blind_top:
                blind_text = pygame.font.Font(None,20).render("Blind Going up",True, [50,250,50])
                blind_rect = blind_text.get_rect(left=35, top=25)
            elif items.blind[1] > items.blind_top:
                blind_text = pygame.font.Font(None,20).render("Blind Going down",True, [50,250,50])
                blind_rect = blind_text.get_rect(left=35, top=25)
        else:
            blind_text = pygame.font.Font(None,20).render("Blind Going Off",True, [250,50,50])
            blind_rect = blind_text.get_rect(left=35, top=25)

        screen.blit(blind_text,blind_rect)

    def do_blind_simulation(self,screen,items):
        if items.blind[1] == True:
            pass


class SettingsWindow():
    def __init__(self):
        # Button for going back to main window
        self.go_back_button         = Button("<-", BTN_GO_BACK_POS, BTN_GO_BACK_WIDTH, BTN_GO_BACK_HEIGHT, BTN_ELEVATION, pygame.font.Font(None,15),SUPER_LIGHT_BLUE,LIGHT_BLUE)
        self.send_setting_button    = Button("Save", BTN_SEND_DATA_POS, BTN_SEND_DATA_WIDTH, BTN_SEND_DATA_HEIGHT,BTN_ELEVATION, pygame.font.Font(None,20), SUPER_LIGHT_BLUE, LIGHT_BLUE)  

        self.wh_slider_left = 54
        self.wh_slider_top = 72


    def print_settings_window(self, screen, functions, items):
        # Go back button
        self.go_back_button.draw(screen, functions[0])
        self.send_setting_button.draw(screen, functions[1])
        
        # Title text
        self.setting_text = pygame.font.Font(None,40).render("SETTINGS", True, BLACK)
        self.setting_rect = self.setting_text.get_rect(center=(WINDOW_SIZE[0]/2, 25))
        screen.blit(self.setting_text,self.setting_rect)

        # Wake hour slider
        self.wake_text = pygame.font.Font(None,20).render("Waking hour", True, BLACK)
        self.wake_rect = self.wake_text.get_rect(center=(WINDOW_SIZE[0]/2,50))
        screen.blit(self.wake_text,self.wake_rect)
        
        self.info_img_wh    = pygame.image.load(INFO_ICON)
        self.info_rect_wh = self.info_img_wh.get_rect(left=15, top=50)
        screen.blit(self.info_img_wh, self.info_rect_wh)
        
        
        pygame.draw.rect(screen, [200,200,200], (54,80,200,2))
        pygame.draw.rect(screen, [155,155,155], (self.wh_slider_left,self.wh_slider_top,SLIDER_WIDTH,SLIDER_HEIGHT))
        
        self.wh_hour_text = pygame.font.Font(None,15).render(str(int(24/(200/(self.wh_slider_left-53)))), True, BLACK)
        self.wh_hour_rect = self.wh_hour_text.get_rect(left=self.wh_slider_left, top=60)
        screen.blit(self.wh_hour_text, self.wh_hour_rect)

        self.zero_wh_text = pygame.font.Font(None,15).render("0", True, BLACK)
        self.zero_wh_rect = self.zero_wh_text.get_rect(left=40,top=80)
        self.tfour_wh_text= pygame.font.Font(None,15).render("24", True, BLACK)
        self.tfour_wh_rect= self.zero_wh_text.get_rect(left=264, top=80)
        screen.blit(self.zero_wh_text, self.zero_wh_rect)
        screen.blit(self.tfour_wh_text, self.tfour_wh_rect)

        if pygame.mouse.get_pressed()[0]:
            mx,my = pygame.mouse.get_pos()

            if mx > 54 and mx < 254 and my > self.wh_slider_top and my < self.wh_slider_top + SLIDER_HEIGHT:
                self.wh_slider_left = mx 


        # Not home hour slider
        self.not_home_text = pygame.font.Font(None,20).render("Not in home hour", True, BLACK)
        self.not_home_rect = self.not_home_text.get_rect(center=(WINDOW_SIZE[0]/2,100))
        screen.blit(self.not_home_text,self.not_home_rect)
        self.info_img_nh   = pygame.image.load(INFO_ICON)
        self.info_rect_nh  = self.info_img_nh.get_rect(left=15, top=100)
        screen.blit(self.info_img_nh, self.info_rect_nh)

        # Back home hour slider
        self.back_home_text = pygame.font.Font(None,20).render("Back Home hour", True, BLACK)
        self.back_home_rect = self.back_home_text.get_rect(center=(WINDOW_SIZE[0]/2,170))
        screen.blit(self.back_home_text,self.back_home_rect)
        self.info_img_bh    = pygame.image.load(INFO_ICON)
        self.info_rect_bh   = self.info_img_bh.get_rect(left=15, top=160)
        screen.blit(self.info_img_bh, self.info_rect_bh)

        # Sleep time slider
        self.sleep_text = pygame.font.Font(None,20).render("Sleep time", True, BLACK)
        self.sleep_rect = self.sleep_text.get_rect(center=(WINDOW_SIZE[0]/2,230))
        screen.blit(self.sleep_text,self.sleep_rect)
        self.info_img_st    = pygame.image.load(INFO_ICON)
        self.info_rect_st   = self.info_img_st.get_rect(left=15, top=220)
        screen.blit(self.info_img_st, self.info_rect_st)

        # Temperature slider
        self.temp_text = pygame.font.Font(None,20).render("Default Temperature", True, BLACK)
        self.temp_rect = self.temp_text.get_rect(center=(WINDOW_SIZE[0]/2,290))
        screen.blit(self.temp_text,self.temp_rect)
        self.info_img_t  = pygame.image.load(INFO_ICON)
        self.info_rect_t = self.info_img_t.get_rect(left=15, top=280)
        screen.blit(self.info_img_t, self.info_rect_t)

        # Temperature min max slider
        self.tempmm_text = pygame.font.Font(None,20).render("Range Temperature", True, BLACK)
        self.tempmm_rect = self.tempmm_text.get_rect(center=(WINDOW_SIZE[0]/2,350))
        screen.blit(self.tempmm_text,self.tempmm_rect)
        self.info_img_tmm  = pygame.image.load(INFO_ICON)
        self.info_rect_tmm = self.info_img_t.get_rect(left=15, top=340)
        screen.blit(self.info_img_tmm, self.info_rect_tmm)

        # Laundry time
        self.laundry_text = pygame.font.Font(None,20).render("laundry time", True, BLACK)
        self.laundry_rect = self.laundry_text.get_rect(center=(WINDOW_SIZE[0]/2,410))
        screen.blit(self.laundry_text,self.laundry_rect)
        self.info_img_l   = pygame.image.load(INFO_ICON)
        self.info_rect_l  = self.info_img_l.get_rect(left=15, top=400)
        screen.blit(self.info_img_l, self.info_rect_l)

