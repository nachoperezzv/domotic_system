from features import *
from tramas import *
from lib import *

from threading import Thread

import pygame, sys, time
import socket

# ----------------------------
# Initializing pygame window |
# ----------------------------
pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption(WINDOW_CAP)
pygame.display.set_icon(pygame.image.load(WINDOW_ICON))

# ---------------------------------------
# Variable for infinite loop of the app |
# ---------------------------------------
DoIt =  True

# ----------------------
# Initializing the API |
# ----------------------
cw = CurrentWeather()   # This is the call for Current weather API

# -------------------------------------
# Initializing the items of the house |
# -------------------------------------
# This class will keep track of the state of each item on the house
items = Items()

# --------------------------------------
# Initializing the tcp/ip of the house |
# --------------------------------------
# Creates the tcp/ip connection object
trama   = str(int(0))
data    = ""
pressed = bool(False)


class TCPIPconnection():
    def __init__(self):
        # TCP/IP socket declaration
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect(IP,PORT)
        self.check_connection()
        
    def connect(self, ip, port):
        # Connecting to server
        self.server_address = (ip, port)
        print('connecting to {} port {}'.format(*self.server_address))
        self.sock.connect(self.server_address)

    def check_connection(self):
        # Sending a message to the ESP8266 and printing the response.
        # This should be a string: 'Connected'
        self.sock.send("connecting".encode('ascii'))
        msg = self.sock.recv(1024)
        print(msg.decode('ascii'))

    def communicate(self):
        global items, trama, data
        self.sock.send(str(trama).encode('ascii'))
        data = self.to_list(self.sock.recv(1024).decode('ascii'))
        
        self.updateItems()
        
        # print("--------")
        # print("trama: ", type(str(trama)), trama)
        # print("data: ", type(data), type(data[0]), data)
        # print("items: ", items.led, items.tv, items.air[1],items.appliance, items.blind[1])
        
        
    def to_list(self,string):
        list1=[]
        list1[:0]=string
        return list1
    
    def updateItems(self):
        global items, data
        items.led = int(data[0])
        items.tv = int(data[1])
        items.air[0] = items.air_onoff = int(data[2])
        items.air[1] = int(data[3])*int(10) + int(data[4])
        items.appliance = int(data[5])
        items.blind = int(data[6])

    def close(self):
        self.sock.close()

 
tcpip = TCPIPconnection()

# ---------------------------------
# Creating the different windows  |
# ---------------------------------
# This variable is used to know which window we should print
# 0 = main window       # 1 = weather window    # 2 = lights window
# 3 = Tv window         # 4 = air window        # 5 = apliance window
# 6 = blinds window
# Default window is main = 0
current_screen = 0

# Declaration of the object main_window from MainWindow class - this will contain the main buttons
main_window = MainWindow()

# Declaration of the object weather_window from WeatherWindw class - this will contain the weather labels
weather_window = WeatherWindow()

# Declaration of the object light_window from LightWindow class - this will contain the light buttons
light_window = LightsWindow()

# Declaration of the object tv_window from TVWindow class - this will contain the tv buttons
tv_window = TVWindow()

# Declaration of the object air_window from AirWindow class - this will contain the air buttons
air_window = AirWindow()

# Declaration of the object appliance_window from ApplianceWindow class - this will contain appliance buttons
appliance_window = ApplianceWindow()

# Declaration of the object blind_window from BlindWindow class - this will contain the blind buttons
blind_window = BlindWindow()

# Declaration of the object settings_window from SettingsWindow class - this will contain the settings buttons
settings_window = SettingsWindow(screen)


# -------------------------------
# Creating the button functions |
# -------------------------------
# These functions will change the variable 'current_screen'. This one indicates which window we should print 

def moving_to_main_window():
    global current_screen
    current_screen = 0

def moving_to_weather_window():
    global current_screen
    current_screen = 1

def moving_to_light_window():
    global current_screen
    current_screen = 2

def moving_to_tv_window():
    global current_screen
    current_screen = 3

def moving_to_air_window():
    global current_screen
    current_screen = 4

def moving_to_appliance_window():
    global current_screen
    current_screen = 5

def moving_to_blind_window():
    global current_screen
    current_screen = 6

def moving_to_setting_window():
    global current_screen
    current_screen = 7

def change_air_onoff():
    global items
    if items.air[0] == 0:
        items.air[0] = 1
    elif items.air[0] == 1:
        items.air[0] == 0

def change_air_mode():
    global items, trama
    if items.air_mode_ma == 0:
        items.air_mode_ma = 1
    elif items.air_mode_ma == 1:
        items.air_mode_ma = 0
    
def up_temperature():
    global items, trama
    if items.air[1] < 30 and not items.air[0] == 0:    
        items.air[1] = items.air[1] + 1
    
    trama = items.get_trama()
    print(trama)

def down_temperature():
    global items, trama
    if items.air[1] > 15 and not items.air[0] == 0:  
        items.air[1] = items.air[1] - 1

    trama = items.get_trama()
    print(trama)

def up_blind():
    global items, trama
    if items.blind == 0 or items.blind == 2:    
        items.blind = 1 
    else:
        items.blind = 0
    print("up")
    trama = items.get_trama()

def down_blind():
    global items,trama
    if items.blind == 0 or items.blind == 1:   
        items.blind = 2
    else:
        items.blind = 0
    print("down")
    trama = items.get_trama()

def send_settings_data():
    global trama, items
    trama = items.get_trama_settings()

# Let's just create a vector that contains all the functions just so it will be easier to call the function print of the main buttons
main_functions      = [moving_to_weather_window, moving_to_light_window, moving_to_tv_window,
                        moving_to_air_window, moving_to_appliance_window ,
                        moving_to_blind_window, moving_to_setting_window]

weather_functions   = [moving_to_main_window]
lights_functions    = [moving_to_main_window]
tv_functions        = [moving_to_main_window]

air_functions       = [moving_to_main_window, change_air_onoff, change_air_mode, 
                        up_temperature, down_temperature]

appliance_functions = [moving_to_main_window]
blinds_functions    = [moving_to_main_window, up_blind, down_blind]
settings_functions  = [moving_to_main_window, send_settings_data]

# --------------------------
# Creating the rain vector |
# --------------------------
rain = []
for i in range(DROP_NUMBER):
    length = DROP_LEN[random.randrange(0,len(DROP_LEN))]
    thickness = DROP_THICKNESS[random.randrange(0,len(DROP_THICKNESS))]
    velocity = DROP_VELOCITY[random.randrange(0,len(DROP_VELOCITY))]
    colour = RAIN_COLORS[random.randrange(0,len(RAIN_COLORS))]
        
    xo,yo = random.randrange(2,WEATHER_WINDOW_WIDTH - 4), random.randrange(2, WEATHER_WINDOW_HEIGHT-10)
    xf,yf = xo, yo + length
        
    start_pos = Point(xo,yo)
    end_pos = Point(xf,yf)

    drop = WaterDrop(start_pos, end_pos, length, thickness, colour, velocity)

    rain.append(drop)


# ------------------------------------
# Setting inicial variables for time |
# ------------------------------------
start   = time.time()
end     = start


# -------------------------------------
# Infinite loop that controls the APP |
# -------------------------------------
while DoIt:
    t = Thread(target=tcpip.communicate(), )
    t.setDaemon = True
    t.start()

    # Handling the events - Stop the app
    for event in pygame.event.get():
        if event.type == pygame.QUIT : 
            DoIt = False

    
    # Handling the API through the time. It must have been X seconds since last call. 
    # X (the time in seconds) is determined by the TIMESTAMP variable   
    end = time.time()
    if (end-start) >= TIMESTAMP:        
        # This calls the OpenWeather API and get the information that is required
        cw.get_weather_info()

        # Let´s restart the timer so it does another call to the API in the selected timestamp
        start   = time.time()
        end     = start
        
    # Checking which window we have to print, but first we fill the background with a default color
    screen.fill(HIPER_LIGHT_BLUE)

    if current_screen == 0:
        main_window.print_main_window(screen, main_functions, cw, rain)
    elif current_screen == 1:
        weather_window.print_weather_window(screen, weather_functions)
    elif current_screen == 2:
        trama = light_window.print_lights_window(screen, lights_functions, items)
    elif current_screen == 3:
        trama = tv_window.print_tv_window(screen, tv_functions, items)
    elif current_screen == 4:
        air_window.print_air_window(screen, air_functions, items)
    elif current_screen == 5:
        trama = appliance_window.print_appliance_window(screen, appliance_functions, items)
    elif current_screen == 6:
        trama = blind_window.print_blind_window(screen, blinds_functions, items)
    elif current_screen == 7:
        settings_window.print_settings_window(screen, settings_functions, items)
    
    # print(trama)
    pygame.display.flip()

# Closing the socket
tcpip.close()

# Closing the app
pygame.quit()
sys.exit()

