
import pygame, os, random

# Constants and variables
DIR_PATH        =   os.path.dirname(os.path.abspath(__file__))
ICON_PATH       =   DIR_PATH + "/config/icons/"
W_ICON_PATH     =   DIR_PATH + "/config/weather_icons/"

WINDOW_SIZE     =   [314,472]   # 8cm (width) x 12 cm(height) x 100 ppp = 13 inches
WINDOW_CAP      =   "Domotic System"
WINDOW_ICON     =   ICON_PATH + "house_icon.png"

WEATHER_WINDOW_WIDTH    =   WINDOW_SIZE[0]
WEATHER_WINDOW_HEIGHT   =   150

CLOUD_ICON      =   W_ICON_PATH + "clouds_2.png"   


# Defining colors 
BLACK           =   [0,0,0]
WHITE           =   [255,255,255]
BLUE_SKY        =   [64,207,255]
LIGHT_BLUE      =   [120,120,255]
SUPER_LIGHT_BLUE=   [150,150,255]
HIPER_LIGHT_BLUE=   [175,175,255]


# Buttons configuration
BTN_ELEVATION       =   3
BTN_SETTINGS_WIDTH  =   WINDOW_SIZE[0] - 4
BTN_SETTINGS_HEIGHT =   (WINDOW_SIZE[1] - WEATHER_WINDOW_HEIGHT)/4 - 4
BTN_SETTINGS_POS    =   [2,0*(WINDOW_SIZE[1]-WEATHER_WINDOW_HEIGHT)/4 + WEATHER_WINDOW_HEIGHT + 2]
BTN_LIGHTS_WIDTH    =   WINDOW_SIZE[0]/2 - 2
BTN_LIGHTS_HEIGHT   =   (WINDOW_SIZE[1] - WEATHER_WINDOW_HEIGHT)/4 - 2 
BTN_LIGHTS_POS      =   [2,1*(WINDOW_SIZE[1]-WEATHER_WINDOW_HEIGHT)/4 + WEATHER_WINDOW_HEIGHT]
BTN_TV_WIDTH        =   WINDOW_SIZE[0]/2 - 4
BTN_TV_HEIGHT       =   (WINDOW_SIZE[1] - WEATHER_WINDOW_HEIGHT)/4 - 2
BTN_TV_POS          =   [WINDOW_SIZE[0]/2 + 2,1*(WINDOW_SIZE[1]-WEATHER_WINDOW_HEIGHT)/4 + WEATHER_WINDOW_HEIGHT]
BTN_AIR_WIDTH       =   WINDOW_SIZE[0]/2 - 2
BTN_AIR_HEIGHT      =   (WINDOW_SIZE[1] - WEATHER_WINDOW_HEIGHT)/4 - 2
BTN_AIR_POS         =   [2,2*(WINDOW_SIZE[1]-WEATHER_WINDOW_HEIGHT)/4 + WEATHER_WINDOW_HEIGHT]
BTN_APPLIANCE_WIDTH =   WINDOW_SIZE[0]/2 - 4
BTN_APPLIANCE_HEIGHT=   (WINDOW_SIZE[1] - WEATHER_WINDOW_HEIGHT)/4 - 2
BTN_APPLIANCE_POS   =   [WINDOW_SIZE[0]/2 + 2,2*(WINDOW_SIZE[1]-WEATHER_WINDOW_HEIGHT)/4 + WEATHER_WINDOW_HEIGHT]
BTN_BLINDS_WIDTH    =   WINDOW_SIZE[0] - 4
BTN_BLINDS_HEIGHT   =   (WINDOW_SIZE[1] - WEATHER_WINDOW_HEIGHT)/4 - 4
BTN_BLINDS_POS      =   [2,3*(WINDOW_SIZE[1]-WEATHER_WINDOW_HEIGHT)/4 + WEATHER_WINDOW_HEIGHT]


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

        pygame.draw.rect(screen,self.bottom_color, self.bottom_rect,border_radius = 12)
        pygame.draw.rect(screen,self.top_color, self.top_rect,border_radius = 12)
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

# Buttons Functions
def btn_print():
    print("Boton pulsado")


class WaterDrop():
    def __init__(self):
        pass
    def water_drop_fall_off():
        pass

def print_sunny_day(screen):
    x,y = pygame.mouse.get_pos()
    if x>=0 and x<=WEATHER_WINDOW_WIDTH and y>=0 and y<= WEATHER_WINDOW_HEIGHT:
        # Changing the background color of the weather
        bg = pygame.Rect(0,0,WEATHER_WINDOW_WIDTH,WEATHER_WINDOW_HEIGHT)       
        pygame.draw.rect(screen,BLUE_SKY,bg,0)
    
    


def print_rainy_day(screen):
    pass

def print_cloudy_day(screen):
    x,y = pygame.mouse.get_pos()
    if x>=0 and x<=WEATHER_WINDOW_WIDTH and y>=0 and y<= WEATHER_WINDOW_HEIGHT:
        # Changing the background color of the weather
        bg = pygame.Rect(0,0,WEATHER_WINDOW_WIDTH,WEATHER_WINDOW_HEIGHT)
        
        cloud_bg        = pygame.image.load(CLOUD_ICON)
        cloud_bg_rect   = cloud_bg.get_rect()
        
        pygame.draw.rect(screen,LIGHT_BLUE,bg,0)
        screen.blit(cloud_bg,cloud_bg_rect)
    
    

def print_dark_night(screen):
    pass

def print_cloudy_night(screen):
    pass

def print_rainy_night(screen):
    pass