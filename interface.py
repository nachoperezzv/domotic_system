from features import *

import pygame, sys, time

# Initializing pygame window
pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption(WINDOW_CAP)
pygame.display.set_icon(pygame.image.load(WINDOW_ICON))

# Initializing the API
cw = CurrentWeather()   # This is the call for Current weather API

# Creating the buttons and panels
btn_settings    =   Button("Settings",BTN_SETTINGS_POS,BTN_SETTINGS_WIDTH, BTN_SETTINGS_HEIGHT, BTN_ELEVATION, pygame.font.Font(None,15),SUPER_LIGHT_BLUE,LIGHT_BLUE)
btn_lights      =   Button("Lights", BTN_LIGHTS_POS, BTN_LIGHTS_WIDTH, BTN_LIGHTS_HEIGHT, BTN_ELEVATION, pygame.font.Font(None,15),SUPER_LIGHT_BLUE,LIGHT_BLUE)
btn_tv          =   Button("TV", BTN_TV_POS, BTN_TV_WIDTH, BTN_TV_HEIGHT, BTN_ELEVATION, pygame.font.Font(None,15),SUPER_LIGHT_BLUE,LIGHT_BLUE)
btn_air         =   Button("Air", BTN_AIR_POS, BTN_AIR_WIDTH, BTN_AIR_HEIGHT, BTN_ELEVATION, pygame.font.Font(None,15),SUPER_LIGHT_BLUE,LIGHT_BLUE)
btn_appliance   =   Button("Appliance", BTN_APPLIANCE_POS, BTN_AIR_WIDTH, BTN_APPLIANCE_HEIGHT, BTN_ELEVATION, pygame.font.Font(None,15),SUPER_LIGHT_BLUE,LIGHT_BLUE)
btn_blinds      =   Button("Blinds", BTN_BLINDS_POS, BTN_BLINDS_WIDTH, BTN_BLINDS_HEIGHT, BTN_ELEVATION, pygame.font.Font(None,15),SUPER_LIGHT_BLUE,LIGHT_BLUE)
btn_weather     =   Button("Weather", BTN_WEATHER_POS, BTN_WEATHER_WIDTH,BTN_WEATHER_HEIGHT,1,pygame.font.Font(None,30), SUPER_LIGHT_BLUE,LIGHT_BLUE)

# Functions for the buttons 
def btn_print():
    pass

def btn_configure_lights():
    pass

# Creating the rain - This is done just once
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

# Setting inicial variables for time
start   = time.time()
end     = start

# Infinite loop that controls the APP
while DoIt:

    # Handling the events - Stop the app
    for event in pygame.event.get():
        if event.type == pygame.QUIT : 
            DoIt = False

    end = time.time()
    # Handling the API through the time. It must have been X seconds since last call. 
    # X (the time in seconds) is determined by the TIMESTAMP variable
    if (end-start) >= TIMESTAMP:        
        # This calls the OpenWeather API and get the information that is required
        cw.get_weather_info()

        # Let´s restart the timer so it does another call to the API in the selected timestamp
        start   = time.time()
        end     = start
        
        

    # Buttons 
    screen.fill(HIPER_LIGHT_BLUE)
    btn_weather.draw(screen, btn_print)
    btn_settings.draw(screen, btn_print)
    btn_lights.draw(screen, btn_configure_lights)
    btn_tv.draw(screen, btn_print)
    btn_air.draw(screen, btn_print)
    btn_appliance.draw(screen, btn_print)
    btn_blinds.draw(screen, btn_print)

    # What is the weather like ? - Simulation
    mx,my = pygame.mouse.get_pos()
    if (mx>2 and mx<WEATHER_WINDOW_WIDTH and my>2 and my<WEATHER_WINDOW_HEIGHT - 2) :
        
        # Checking if it's day/night, cloudy or rainy
        if cw.its_day:
            if cw.rain_volume > VALID_RAIN_RATE:
                print_rainy_day(screen, btn_weather.get_Rect(), rain)
            elif cw.cloud_percent > VALID_CLOUD_RATE: 
                print_cloudy_day(screen, btn_weather.get_Rect())
            else:
                print_sunny_day(screen, btn_weather.get_Rect())            
        else: 
            if cw.rain_volume > VALID_RAIN_RATE:
                print_rainy_day(screen, btn_weather.get_Rect(), rain)
            elif cw.cloud_percent > VALID_CLOUD_RATE: 
                print_cloudy_day(screen, btn_weather.get_Rect())
            else:
                print_dark_night(screen, btn_weather.get_Rect())
            
        # Adding to the Weather App some widgets
        offset = 15

        location_text = pygame.font.Font(None,30).render(str("Alicante, ES"), True, WHITE)
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
        pygame.display.update(btn_weather.get_Rect())
    
    else:
        # If none of the buttons have been pressed the we update the whole screen
        pygame.display.flip()

    

# Closing the app
pygame.quit()
sys.exit()

