import os

# Constants and variables
DIR_PATH            =   os.path.dirname(os.path.abspath(__file__))
ICON_PATH           =   DIR_PATH + "/config/icons/"
WEATHER_ICON_PATH   =   DIR_PATH + "/config/weather_icons/"
WINDOW_ICON_PATH    =   DIR_PATH + "/config/window_icons/"

WINDOW_SIZE         =   [314,472]   # 8cm (width) x 12 cm(height) x 100 ppp = 13 inches
WINDOW_CAP          =   "Domotic System"
WINDOW_ICON         =   ICON_PATH + "house_icon.png"

INFO_ICON           =   WINDOW_ICON_PATH + "info.png"

WEATHER_WINDOW_WIDTH    =   WINDOW_SIZE[0] - 4
WEATHER_WINDOW_HEIGHT   =   150

CLOUD_ICON          =   WEATHER_ICON_PATH + "clouds.png"   
CLOUDY_NIGHT_ICON   =   WEATHER_ICON_PATH + "cloudy_night.png"
SUN_ICON            =   WEATHER_ICON_PATH + "sun.png"
NIGHT_ICON          =   WEATHER_ICON_PATH + "night.png"

AIR_WINDOW_BG       =   WINDOW_ICON_PATH + "air.png"
TV_WINDOW_BG        =   WINDOW_ICON_PATH + "tv.png"
LIGHTS_WINDOW_BG    =   WINDOW_ICON_PATH + "lights.png"
BLIND_WINDOW_BG     =   WINDOW_ICON_PATH + "blind.png"
APPLIANCE_WIN_BG    =   WINDOW_ICON_PATH + "appliance.png"


# Defining colors 
BLACK               =   [0,0,0,155]
WHITE               =   [255,255,255]
BLUE_SKY            =   [64,207,255]
LIGHT_BLUE          =   [120,120,255]
SUPER_LIGHT_BLUE    =   [150,150,255]
HIPER_LIGHT_BLUE    =   [175,175,255]

BLUE_RAIN           =   [165,180,220]#[255,0,0]
LIGHT_BLUE_RAIN     =   [165,180,200]#[0,255,0]
VERY_LIGHT_BLUE_RAIN=   [165,180,180]#[0,0,255]
RAIN_COLORS         =   [BLUE_RAIN, LIGHT_BLUE_RAIN, VERY_LIGHT_BLUE_RAIN]

# Rain Variables
DROP_NUMBER         =   20

DROP_THICK          =   2
DROP_THIN           =   1
DROP_THICKNESS      =   [DROP_THICK, DROP_THIN]

DROP_LEN_LONG       =   20#5
DROP_LEN_SHORT      =   10#3
DROP_LEN_VERY_SHORT =   5
DROP_LEN            =   [DROP_LEN_LONG, DROP_LEN_SHORT, DROP_LEN_VERY_SHORT]

DROP_FAST           =   2
DROP_SLOW           =   1.5 
DROP_VERY_SLOW      =   1
DROP_VELOCITY       =   [DROP_FAST, DROP_SLOW, DROP_VERY_SLOW]


# Time Variables
TIMESTAMP           =   90 #secs

# API Variables 
API_url             = "https://api.openweathermap.org/data/2.5/weather?"
API_key             = "&appid=7e529a7df215e65c222ec1f24c8fe80c"
API_city            = "&q=Alicante,ES"
API_units           = "&units=metric" 

API                 = API_url + API_city + API_units + API_key

VALID_CLOUD_RATE    = 30 #%
VALID_RAIN_RATE     = 1


# Buttons configuration
BTN_ELEVATION       =   3

BTN_WEATHER_WIDTH   =   WEATHER_WINDOW_WIDTH
BTN_WEATHER_HEIGHT  =   WEATHER_WINDOW_HEIGHT - 4
BTN_WEATHER_POS     =   [2,2]

BTN_LIGHTS_WIDTH    =   WINDOW_SIZE[0]/2 - 2
BTN_LIGHTS_HEIGHT   =   (WINDOW_SIZE[1] - WEATHER_WINDOW_HEIGHT)/4 - 2 
BTN_LIGHTS_POS      =   [2,0*(WINDOW_SIZE[1]-WEATHER_WINDOW_HEIGHT)/4 + WEATHER_WINDOW_HEIGHT + 2]
BTN_TV_WIDTH        =   WINDOW_SIZE[0]/2 - 4
BTN_TV_HEIGHT       =   (WINDOW_SIZE[1] - WEATHER_WINDOW_HEIGHT)/4 - 2
BTN_TV_POS          =   [WINDOW_SIZE[0]/2 + 2,0*(WINDOW_SIZE[1]-WEATHER_WINDOW_HEIGHT)/4 + WEATHER_WINDOW_HEIGHT + 2]
BTN_AIR_WIDTH       =   WINDOW_SIZE[0]/2 - 2
BTN_AIR_HEIGHT      =   (WINDOW_SIZE[1] - WEATHER_WINDOW_HEIGHT)/4 - 2
BTN_AIR_POS         =   [2,1*(WINDOW_SIZE[1]-WEATHER_WINDOW_HEIGHT)/4 + WEATHER_WINDOW_HEIGHT + 2]
BTN_APPLIANCE_WIDTH =   WINDOW_SIZE[0]/2 - 4
BTN_APPLIANCE_HEIGHT=   (WINDOW_SIZE[1] - WEATHER_WINDOW_HEIGHT)/4 - 2
BTN_APPLIANCE_POS   =   [WINDOW_SIZE[0]/2 + 2,1*(WINDOW_SIZE[1]-WEATHER_WINDOW_HEIGHT)/4 + WEATHER_WINDOW_HEIGHT + 2]
BTN_BLINDS_WIDTH    =   WINDOW_SIZE[0] - 4
BTN_BLINDS_HEIGHT   =   (WINDOW_SIZE[1] - WEATHER_WINDOW_HEIGHT)/4 - 4
BTN_BLINDS_POS      =   [2,2*(WINDOW_SIZE[1]-WEATHER_WINDOW_HEIGHT)/4 + WEATHER_WINDOW_HEIGHT +2]
BTN_SETTINGS_WIDTH  =   WINDOW_SIZE[0] - 4
BTN_SETTINGS_HEIGHT =   (WINDOW_SIZE[1] - WEATHER_WINDOW_HEIGHT)/4 - 4
BTN_SETTINGS_POS    =   [2,3*(WINDOW_SIZE[1]-WEATHER_WINDOW_HEIGHT)/4 + WEATHER_WINDOW_HEIGHT + 2]

BTN_GO_BACK_WIDTH   =   30
BTN_GO_BACK_HEIGHT  =   30
BTN_GO_BACK_POS     =   [WINDOW_SIZE[0] - 45, 15]

BTN_SEND_DATA_WIDTH =   WINDOW_SIZE[0] - 40
BTN_SEND_DATA_HEIGHT=   20
BTN_SEND_DATA_POS   =   [20, 448]

# TCP/IP Connection
IP                  = '192.168.100.2'
PORT                = 8888

last_mouse_state    = 0

SLIDER_WIDTH        = 8
SLIDER_HEIGHT       = 16