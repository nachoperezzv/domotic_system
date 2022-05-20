
from ctypes.wintypes import DOUBLE
import sys
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

class ForecastWeather():
    def __init__(self):
        # Initializing the attributes of the class
        
        self.data = []
        self.dt = []
        self.min_temp = []
        self.max_temp = []
        self.icon = []

        self.get_weather_info()  
    
    def __calling_the_API(self):
        
        self.req    = urllib.request.Request(API2)
        self.resp   = urllib.request.urlopen(self.req)
        self.info   = json.loads(self.resp.read().decode('utf-8'))
        self.resp.close()

    def get_weather_info(self):   
        # Calling the API
        self.__calling_the_API()
        
        # Getting info from the JSON response of the API
        
        try: 
            self.data = self.info['daily'][1:6]
        except: pass

        try:
            for d in self.data:
                day = datetime.utcfromtimestamp(d['dt'])
                self.dt.append(day.strftime("%d/%m"))
        except: pass

        try:
            for d in self.data:
                self.min_temp.append(int(d['temp']['min']) - 273)
        except: pass

        try:
            for d in self.data:
                self.max_temp.append(int(d['temp']['max']) - 273)
        except: pass    

        try:
            for d in self.data:
                self.icon.append(d['weather'][0]['icon'])
        except: pass    
    

class REDataAPI():
    def __init__(self):
        self.prices = []

        self.get_data_info()

    def __calling_API(self):
        self.req    = urllib.request.Request(API3_url)
        self.resp   = urllib.request.urlopen(self.req)
        self.info   = json.loads(self.resp.read().decode('utf-8'))
        self.resp.close()

        self.prices.clear()
        for k in self.info.keys():
            self.prices.append(self.info[k]['price'])

    
    def get_data_info(self):
        self.__calling_API()

    
    def get_cheapest_in_range(self,range_min, range_max):
        cheapest    = sys.float_info.max
        hour        = 0

        for i in range(range_min,range_max):
            if self.prices[i] < cheapest:
                cheapest,hour = self.prices[i],i
        
        return cheapest, hour



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

            time_text = pygame.font.Font(None,30).render(str(cw.time), True, WHITE)
            time_rect = time_text.get_rect(center=(WEATHER_WINDOW_WIDTH/2, 4*WEATHER_WINDOW_HEIGHT/5 + 5))
            screen.blit(time_text, time_rect)
        
        # Let's just update the surface we are changing in order to save CPU time
        pygame.display.update(self.btn_weather.get_Rect())


class WeatherWindow():
    def __init__(self):
        # Button for going back to main window
        self.go_back_button =   Button("<-", BTN_GO_BACK_POS, BTN_GO_BACK_WIDTH, BTN_GO_BACK_HEIGHT, BTN_ELEVATION, pygame.font.Font(None,15),SUPER_LIGHT_BLUE,LIGHT_BLUE)

    def print_weather_window(self, screen, functions, cw, fw, rain):
        
        self.do_weather_simulations(screen, cw, fw, rain)
        self.go_back_button.draw(screen, functions[0])



    def do_weather_simulations(self, screen, cw, fw, rain):
       
        rect = pygame.draw.rect(screen,HIPER_LIGHT_BLUE, (BTN_WEATHER_POS[0], BTN_WEATHER_POS[1], BTN_WEATHER_WIDTH,BTN_WEATHER_HEIGHT))

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

        forecast_text = pygame.font.Font(None,30).render("Day           Forecast", True, WHITE)
        forecast_rect = forecast_text.get_rect(left=60, top=160)
        screen.blit(forecast_text,forecast_rect)

        pygame.draw.line(screen,GREY,[30,185],[284,185],3)

        begin = 170
        day_size = 60
        for i in range(len(fw.data)):
            date_text = pygame.font.Font(None,30).render(str(fw.dt[i]), True, WHITE)
            date_rect = date_text.get_rect(left=20, top=(begin + i*day_size + 30))
            screen.blit(date_text, date_rect)

            icon_img = pygame.image.load(WEATHER_ICON_PATH + fw.icon[i] + ".png")
            icon_rect = icon_img.get_rect(left=date_rect.right+30, top=(begin + i*day_size +18))
            screen.blit(icon_img, icon_rect)

            temp_min_text = pygame.font.Font(None,20).render(str("Min: ") + str(fw.min_temp[i]) + str("ºC"), True, WHITE)
            temp_min_rect = temp_min_text.get_rect(left=160, top=(begin + i*day_size + 30))

            temp_max_text = pygame.font.Font(None,20).render(str("Max: ") + str(fw.max_temp[i]) + str("ºC"), True, WHITE)
            temp_max_rect = temp_max_text.get_rect(left=235, top=(begin + i*day_size + 30)) 

            screen.blit(temp_min_text,temp_min_rect)
            screen.blit(temp_max_text,temp_max_rect)


        


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

class Slider():
    def __init__(self, screen, text, tam_text, text_color, text_pos, 
                bar_color, bar_pos, bar_width, bar_height, left_bar_text, left_bar_text_pos, right_bar_text, right_bar_text_pos,
                slider_color, slider_pos, slider_width, slider_height,
                division = 100, info=False, info_pos=None, offset=0):

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
        if info_pos != None:
            self.info_pos = info_pos    

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
        
        mx,my = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:       
            if mx > self.bar_pos[0] and mx < (self.bar_pos[0]+self.bar_width) and my > self.slider_pos[1] and my < self.slider_pos[1] + self.slider_height:
                self.mark = mx 
                

    def print_info(self, text_info, text_info2=None, text_info3=None, downside=False):
        mx,my = pygame.mouse.get_pos()
        y_pos_mul = 0
        x_val = 5
        y_val = 10
        if downside:
            y_val = -25
            text = pygame.font.Font(None,15).render(text_info, True, BLACK)
            text_rect = text.get_rect(left=self.info_pos[0] + x_val ,top=self.info_pos[1] - y_val + y_pos_mul*10)

            if text_info2 != None:
                y_pos_mul = y_pos_mul +  1
                text2 = pygame.font.Font(None,15).render(text_info2, True, BLACK)
                text_rect2 = text2.get_rect(left=self.info_pos[0] + x_val,top=self.info_pos[1] - y_val + y_pos_mul*10)
                

            if text_info3 != None:
                y_pos_mul = y_pos_mul +  1
                text3 = pygame.font.Font(None,15).render(text_info3, True, BLACK)
                text_rect3 = text3.get_rect(left=self.info_pos[0] + x_val,top=self.info_pos[1] - y_val + y_pos_mul*10)
                

            

        else:
            if text_info3 != None:
                text3 = pygame.font.Font(None,15).render(text_info3, True, BLACK)
                text_rect3 = text3.get_rect(left=self.info_pos[0] + x_val,bottom=self.info_pos[1] - y_val - y_pos_mul*10)
                y_pos_mul = y_pos_mul +  1

            if text_info2 != None:
                text2 = pygame.font.Font(None,15).render(text_info2, True, BLACK)
                text_rect2 = text2.get_rect(left=self.info_pos[0] + x_val,bottom=self.info_pos[1] - y_val - y_pos_mul*10)
                y_pos_mul = y_pos_mul +  1


            text = pygame.font.Font(None,15).render(text_info, True, BLACK)
            text_rect = text.get_rect(left=self.info_pos[0] + x_val ,bottom=self.info_pos[1] - y_val - y_pos_mul*10)


        info_rect = text_rect.copy()
        info_rect.top = info_rect.top - 5
        info_rect.height = info_rect.height + 10
        info_rect.left = info_rect.left - 5
        info_rect.width = info_rect.width + 10

        if text_info2 != None:
            info_rect.height = info_rect.height + text_rect2.copy().height

        if text_info3 != None:
            info_rect.height = info_rect.height + text_rect3.copy().height


        if mx > self.info_pos[0] and mx < self.info_pos[0] + 15 and my > self.info_pos[1] and my < self.info_pos[1] + 15:
            
            pygame.draw.rect(self.screen, WHITE, info_rect)
            if not downside:
                pygame.draw.polygon(self.screen, WHITE, [(self.info_pos[0]+x_val,self.info_pos[1]-y_val),(self.info_pos[0]+x_val,self.info_pos[1]),(self.info_pos[0]+15,self.info_pos[1]-y_val) ])
            else:
                pygame.draw.polygon(self.screen, WHITE, [(self.info_pos[0]+x_val,self.info_pos[1]-y_val),(self.info_pos[0]+x_val,self.info_pos[1]+15),(self.info_pos[0]+15,self.info_pos[1]-y_val) ])


            self.screen.blit(text,text_rect)
            if text_info2!= None:
                self.screen.blit(text2,text_rect2)
            if text_info3 != None:
                self.screen.blit(text3,text_rect3)
        

            


class SettingsWindow():
    def __init__(self, screen):
        # Button for going back to main windowNo documentati
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
                                15,info=True,info_pos = T_INFO_POS)

        self.trm_slider= Slider(screen,TR_TEXT,TR_TEXT_TAM,TR_TEXT_COLOR,TR_TEXT_POS,
                                TR_BAR_COLOR,TR_BAR_POS,TR_BAR_WIDTH,TR_BAR_HEIGHT,TR_LEFT_BAR_TEXT,TR_LEFT_BAR_TEXT_POS,TR_RIGHT_BAR_TEXT,TR_RIGHT_BAR_TEXT_POS,
                                TR_SLIDER_COLOR,TR_SLIDER_POS,TR_SLIDER_WIDTH,TR_SLIDER_HEIGHT,
                                15,info=True,info_pos = TR_INFO_POS,offset=15)
        
        self.trM_slider= Slider(screen,TRM_TEXT,TRM_TEXT_TAM,TRM_TEXT_COLOR,TRM_TEXT_POS,
                                TRM_BAR_COLOR,TRM_BAR_POS,TRM_BAR_WIDTH,TRM_BAR_HEIGHT,TRM_LEFT_BAR_TEXT,TRM_LEFT_BAR_TEXT_POS,TRM_RIGHT_BAR_TEXT,TRM_RIGHT_BAR_TEXT_POS,
                                TRM_SLIDER_COLOR,TRM_SLIDER_POS,TRM_SLIDER_WIDTH,TRM_SLIDER_HEIGHT,
                                15,info=True,info_pos = TRM_INFO_POS,offset=15)

        self.lt_slider = Slider(screen,LT_TEXT,LT_TEXT_TAM,LT_TEXT_COLOR,LT_TEXT_POS,
                                LT_BAR_COLOR,LT_BAR_POS,LT_BAR_WIDTH,LT_BAR_HEIGHT,LT_LEFT_BAR_TEXT,LT_LEFT_BAR_TEXT_POS,LT_RIGHT_BAR_TEXT,LT_RIGHT_BAR_TEXT_POS,
                                LT_SLIDER_COLOR,LT_SLIDER_POS,LT_SLIDER_WIDTH,LT_SLIDER_HEIGHT,
                                DIV,info=True,info_pos = LT_INFO_POS)

    def print_settings_window(self, screen, functions, items):
        # Go back button
        self.go_back_button.draw(screen, functions[0])
        self.send_setting_button.draw(screen, functions[1])
        
        # Title text
        self.setting_text = pygame.font.Font(None,40).render("SETTINGS", True, BLACK)
        self.setting_rect = self.setting_text.get_rect(center=(WINDOW_SIZE[0]/2, 15))
        screen.blit(self.setting_text,self.setting_rect)

        # Wake hour slider
        self.wh_slider.draw()
        self.nh_slider.draw()
        self.bh_slider.draw()
        self.st_slider.draw()
        self.t_slider.draw()
        self.trm_slider.draw()
        self.trM_slider.draw()
        self.lt_slider.draw()

        self.wh_slider.print_info("Select the hour when you usually get up",downside=True)
        self.nh_slider.print_info("Select the hour when you usually leave home")
        self.bh_slider.print_info("Select the hour when you usually get back home")
        self.st_slider.print_info("Select the hour when you usually go to bed")
        self.t_slider.print_info("Select the home desired temperature by default")
        self.trm_slider.print_info("Select the minimum limit temperature which", text_info2="should not be passed", downside=True)
        self.trM_slider.print_info("Select the maximum limit temperature which", text_info2="should not be passed")
        self.lt_slider.print_info("Select the hour ranges when you usually would", text_info2="set the laundry on")



