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
RED                 =   [255,150,100]
BLUE                =   [100,150,255]
BLUE_SKY            =   [64,207,255]
LIGHT_BLUE          =   [120,120,255]
SUPER_LIGHT_BLUE    =   [150,150,255]
HIPER_LIGHT_BLUE    =   [175,175,255]
GREY                =   [155,155,155]
LIGHT_GREY          =   [200,200,200]

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
TIMESTAMP           =   90      #seconds
TIMESTAMP           =   3600    #seconds

# API Variables 
API_url             = "https://api.openweathermap.org/data/2.5/weather?"
API_key             = "&appid=7e529a7df215e65c222ec1f24c8fe80c"
API_city            = "&q=Alicante,ES"
API_units           = "&units=metric" 

API2_url            = "https://api.openweathermap.org/data/2.5/onecall?"
API2exclude         = "&exclude=current,minutely,hourly,alerts"
ALC_lat             = "lat=38.3452"
ALC_lon             = "&lon=-0.481006"

API3_url            = "https://api.preciodelaluz.org/v1/prices/all?zone=PCB"

API                 = API_url + API_city + API_units + API_key
API2                = API2_url + ALC_lat + ALC_lon + API2exclude + API_key

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
BAR_WIDTH           = 200
BAR_HEIGHT          = 2

DIV                 = 24

WH_TEXT             = "Waking Hour"
WH_TEXT_TAM         = 20
WH_TEXT_COLOR       = BLACK
WH_TEXT_POS         = [WINDOW_SIZE[0]/2,40]
WH_BAR_COLOR        = LIGHT_GREY
WH_BAR_POS          = [57,60]
WH_BAR_WIDTH        = 200
WH_BAR_HEIGHT       = 2
WH_LEFT_BAR_TEXT    = "0"
WH_LEFT_BAR_TEXT_POS= [40,60]
WH_RIGHT_BAR_TEXT   = "24"
WH_RIGHT_BAR_TEXT_POS=[269,60]
WH_SLIDER_COLOR     = GREY
WH_SLIDER_POS       = [54,52]
WH_SLIDER_WIDTH     = 8
WH_SLIDER_HEIGHT    = 16
WH_INFO_POS         = [15,52]

NH_TEXT             = "Not in home time"
NH_TEXT_TAM         = 20
NH_TEXT_COLOR       = BLACK
NH_TEXT_POS         = [WINDOW_SIZE[0]/2,90]
NH_BAR_COLOR        = LIGHT_GREY
NH_BAR_POS          = [57,110]
NH_BAR_WIDTH        = 200
NH_BAR_HEIGHT       = 2
NH_LEFT_BAR_TEXT    = "0"
NH_LEFT_BAR_TEXT_POS= [40,110]
NH_RIGHT_BAR_TEXT   = "24"
NH_RIGHT_BAR_TEXT_POS=[269,110]
NH_SLIDER_COLOR     = GREY
NH_SLIDER_POS       = [54,102]
NH_SLIDER_WIDTH     = 8
NH_SLIDER_HEIGHT    = 16
NH_INFO_POS         = [15,102]

BH_TEXT             = "Back Home time"
BH_TEXT_TAM         = 20
BH_TEXT_COLOR       = BLACK
BH_TEXT_POS         = [WINDOW_SIZE[0]/2,150]
BH_BAR_COLOR        = LIGHT_GREY
BH_BAR_POS          = [57,170]
BH_BAR_WIDTH        = 200
BH_BAR_HEIGHT       = 2
BH_LEFT_BAR_TEXT    = "0"
BH_LEFT_BAR_TEXT_POS=[40,170]
BH_RIGHT_BAR_TEXT   = "24"
BH_RIGHT_BAR_TEXT_POS=[269,170]
BH_SLIDER_COLOR     = GREY
BH_SLIDER_POS       = [54,162]
BH_SLIDER_WIDTH     = 8
BH_SLIDER_HEIGHT    = 16
BH_INFO_POS         = [15,162]

ST_TEXT             = "Sleep time"
ST_TEXT_TAM         = 20
ST_TEXT_COLOR       = BLACK
ST_TEXT_POS         = [WINDOW_SIZE[0]/2,210]
ST_BAR_COLOR        = LIGHT_GREY
ST_BAR_POS          = [57,230]
ST_BAR_WIDTH        = 200
ST_BAR_HEIGHT       = 2
ST_LEFT_BAR_TEXT    = "0"
ST_LEFT_BAR_TEXT_POS= [40,230]
ST_RIGHT_BAR_TEXT   = "24"
ST_RIGHT_BAR_TEXT_POS=[269,230]
ST_SLIDER_COLOR     = GREY
ST_SLIDER_POS       = [54,222]
ST_SLIDER_WIDTH     = 8
ST_SLIDER_HEIGHT    = 16
ST_INFO_POS         = [15,222]

T_TEXT             = "Temperature"
T_TEXT_TAM         = 20
T_TEXT_COLOR       = BLACK
T_TEXT_POS         = [WINDOW_SIZE[0]/2,270]
T_BAR_COLOR        = LIGHT_GREY
T_BAR_POS          = [57,290]
T_BAR_WIDTH        = 200
T_BAR_HEIGHT       = 2
T_LEFT_BAR_TEXT    = "0"
T_LEFT_BAR_TEXT_POS= [40,290]
T_RIGHT_BAR_TEXT   = "24"
T_RIGHT_BAR_TEXT_POS=[269,290]
T_SLIDER_COLOR     = GREY
T_SLIDER_POS       = [54,282]
T_SLIDER_WIDTH     = 8
T_SLIDER_HEIGHT    = 16
T_INFO_POS         = [15,282]

TR_TEXT             = "Temperature Range"
TR_TEXT_TAM         = 20
TR_TEXT_COLOR       = BLACK
TR_TEXT_POS         = [WINDOW_SIZE[0]/2,330]
TR_BAR_COLOR        = LIGHT_GREY
TR_BAR_POS          = [57,350]
TR_BAR_WIDTH        = 200
TR_BAR_HEIGHT       = 2
TR_LEFT_BAR_TEXT    = "15"
TR_LEFT_BAR_TEXT_POS= [40,350]
TR_RIGHT_BAR_TEXT   = "30"
TR_RIGHT_BAR_TEXT_POS=[269,350]
TR_SLIDER_COLOR     = BLUE
TR_SLIDER_POS       = [54,342]
TR_SLIDER_WIDTH     = 8
TR_SLIDER_HEIGHT    = 16
TR_INFO_POS         = [15,342]

TRM_TEXT             = ""
TRM_TEXT_TAM         = 20
TRM_TEXT_COLOR       = BLACK
TRM_TEXT_POS         = [WINDOW_SIZE[0]/2,330]
TRM_BAR_COLOR        = LIGHT_GREY
TRM_BAR_POS          = [57,350]
TRM_BAR_WIDTH        = 200
TRM_BAR_HEIGHT       = 2
TRM_LEFT_BAR_TEXT    = ""
TRM_LEFT_BAR_TEXT_POS= [40,350]
TRM_RIGHT_BAR_TEXT   = ""
TRM_RIGHT_BAR_TEXT_POS=[269,350]
TRM_SLIDER_COLOR     = RED
TRM_SLIDER_POS       = [246,342]
TRM_SLIDER_WIDTH     = 8
TRM_SLIDER_HEIGHT    = 16
TRM_INFO_POS         = [15,342]

LT_TEXT             = "Laundry Time"
LT_TEXT_TAM         = 20
LT_TEXT_COLOR       = BLACK
LT_TEXT_POS         = [WINDOW_SIZE[0]/2,390]
LT_BAR_COLOR        = LIGHT_GREY
LT_BAR_POS          = [57,410]
LT_BAR_WIDTH        = 200
LT_BAR_HEIGHT       = 2
LT_LEFT_BAR_TEXT    = "0"
LT_LEFT_BAR_TEXT_POS= [40,410]
LT_RIGHT_BAR_TEXT   = "24"
LT_RIGHT_BAR_TEXT_POS=[269,410]
LT_SLIDER_COLOR     = GREY
LT_SLIDER_POS       = [54,402]
LT_SLIDER_WIDTH     = 8
LT_SLIDER_HEIGHT    = 16
LT_INFO_POS         = [15,402]

