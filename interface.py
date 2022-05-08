from features import *

import pygame, sys

# Initializing pygame window
pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption(WINDOW_CAP)
pygame.display.set_icon(pygame.image.load(WINDOW_ICON))

# Creating the buttons and panels
btn_settings    =   Button("Settings",BTN_SETTINGS_POS,BTN_SETTINGS_WIDTH, BTN_SETTINGS_HEIGHT, BTN_ELEVATION, pygame.font.Font(None,15),SUPER_LIGHT_BLUE,LIGHT_BLUE)
btn_lights      =   Button("Lights", BTN_LIGHTS_POS, BTN_LIGHTS_WIDTH, BTN_LIGHTS_HEIGHT, BTN_ELEVATION, pygame.font.Font(None,15),SUPER_LIGHT_BLUE,LIGHT_BLUE)
btn_tv          =   Button("TV", BTN_TV_POS, BTN_TV_WIDTH, BTN_TV_HEIGHT, BTN_ELEVATION, pygame.font.Font(None,15),SUPER_LIGHT_BLUE,LIGHT_BLUE)
btn_air         =   Button("Air", BTN_AIR_POS, BTN_AIR_WIDTH, BTN_AIR_HEIGHT, BTN_ELEVATION, pygame.font.Font(None,15),SUPER_LIGHT_BLUE,LIGHT_BLUE)
btn_appliance   =   Button("Appliance", BTN_APPLIANCE_POS, BTN_AIR_WIDTH, BTN_APPLIANCE_HEIGHT, BTN_ELEVATION, pygame.font.Font(None,15),SUPER_LIGHT_BLUE,LIGHT_BLUE)
btn_blinds      =   Button("Blinds", BTN_BLINDS_POS, BTN_BLINDS_WIDTH, BTN_BLINDS_HEIGHT, BTN_ELEVATION, pygame.font.Font(None,15),SUPER_LIGHT_BLUE,LIGHT_BLUE)
btn_weather     =   Button("Weather", BTN_WEATHER_POS, BTN_WEATHER_WIDTH,BTN_WEATHER_HEIGHT,1,pygame.font.Font(None,30), SUPER_LIGHT_BLUE,LIGHT_BLUE)

# Infinite loop that controls the APP
while DoIt:

    # Handling the events - Stop the app
    for event in pygame.event.get():
        if event.type == pygame.QUIT : 
            DoIt = False

    # Buttons 
    screen.fill(HIPER_LIGHT_BLUE)
    btn_weather.draw(screen, btn_print)
    btn_settings.draw(screen, btn_print)
    btn_lights.draw(screen, btn_print)
    btn_tv.draw(screen, btn_print)
    btn_air.draw(screen, btn_print)
    btn_appliance.draw(screen, btn_print)
    btn_blinds.draw(screen, btn_print)

    # What is the weather like ? - Simulation
    print_sunny_day(screen)
    # print_cloudy_day(screen)
    # print_rainy_day(screen)
    # print_dark_night(screen)
    # print_cloudy_night(screen)
    # print_rainy_day(screen)

    # line = pygame.draw.line(screen, WHITE, (50,50), (50,55), 1)
    


    
    pygame.display.flip()

# Closing the app
pygame.quit()
sys.exit()

