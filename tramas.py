TRAMAS = {  
    # The tramas contain 4 modules:
        # A - 1byte: For the item
        # B - 1byte: Read/Write
        # C - 1byte: Status
        # D - 1byte: Value
    #  _  _  _  _
    # |A||B||C||D|
    # |_||_||_||_|

    # Trama for the led
    'LED_WRITE'     :   '10',
    'LED_READ'      :   '11',
        # 

    # Trama for the TV
    'TV_WRITE'      :   '20',
    'TV_READ'       :   '21',

    # Trama for the air
    'AIR_WRITE_OFF' :   '300',
    'AIR_WRITE_HOT' :   '301',  
        # Next to it will come a D module:
        # '301' + bytes(temperature selected)
    'AIR_WRITE_COLD':   '302',
        # Next to it will come a D module:
        # '302' + bytes(temperature selected)
    'AIR_READ'      :   '31',
    
    # Trama for the appliance
    'APPLIANCE_WRITE'       :   '40',
    'APPLIANCE_READ'        :   '41',

    # Trama for the blinds
    'BLIND_WRITE_OFF'       :   '500',
    'BLIND_WRITE_UP'        :   '501',
        # Next to it will come a D module:
        # '501' + bytes(position of the blind)
    'BLIND_WRITE_DOWN'      :   '502',
        # Next to it will come a D module:
        # '502' + bytes(position of the blind)
    'BLIND_READ'            :   '51'

    }
