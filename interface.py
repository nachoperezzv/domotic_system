from pip import main
from features import *

import pygame, sys, time

# ----------------------------
# Initializing pygame window |
# ----------------------------
pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption(WINDOW_CAP)
pygame.display.set_icon(pygame.image.load(WINDOW_ICON))


# ----------------------
# Initializing the API |
# ----------------------
cw = CurrentWeather()   # This is the call for Current weather API


# ---------------------------------
# Creating the different windows  |
# ---------------------------------
# This variable is used to know which window we should print
# 0 = main window       # 1 = weather window    # 2 = lights window
# 3 = Tv window         # 4 = air window        # 5 = apliance window
# 6 = blinds window
# Default window is main = 0
current_screen = 0

# Declaration of the object main_buttons from main_window class
main_window = MainWindow()

# Declaration of the object light_buttons from lights_window class
light_window = LightsWindow()

# Declaration of the object air_buttons from air_window class
air_window = AirWindow()

# Declaration of the object tv_buttons from tv_window class
tv_window = TVWindow()

# Declaration of the object blind_buttons from blind_window class
blind_window = BlindWindow()


# -------------------------------
# Creating the button functions |
# -------------------------------
# These functions will change the variable 'current_screen'. This one indicates which window we should print 

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

# Let's just create a vector that contains all the functions just so it will be easier to call the function print of the main buttons
functions = [moving_to_weather_window, moving_to_light_window, moving_to_tv_window, moving_to_air_window, moving_to_appliance_window ,moving_to_blind_window, moving_to_setting_window]

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
        main_window.print_main_window(screen, functions, cw, rain)
    elif current_screen == 1:pass
        # Draw Weather Window
    elif current_screen == 2:pass
        # Draw Light Window
    elif current_screen == 3:pass
        # Draw TV Window
    elif current_screen == 4:pass
        # Draw Air Window
    elif current_screen == 5:pass
        # Draw Appliance Window
    elif current_screen == 6:pass
        # Draw Blind Window
    elif current_screen == 7:pass
        # Draw Setting Window

    pygame.display.flip()

    

# Closing the app
pygame.quit()
sys.exit()

