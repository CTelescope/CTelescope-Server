#  
#  CTELESCOPE COMPONENTS CONFIG 
#
"""
MOTOR & DRIVER
"""
MOTOR_SPR             =   400          # Step per revolution
MICRO_STEP_MODE       =   64           # 
MIN_STEP_TIME_LEVEL   =   100 * 10**-8 # Voir le data sheet du sheep TMC2209 page 60
STEP_TIME             =   2 * MIN_STEP_TIME_LEVEL
"""
EQUATORIAL MOUNT
"""
DEC_EQ_M_GEAR_REDUC     =   65
AD_EQ_M_GEAR_REDUC      =   130
AXE_DEC_GEAR_REDUC      =   52/16
AXE_AD_GEAR_REDUC       =   44/16
RESOLUTION_ARCSEC_DEC   =   ((((360 / MOTOR_SPR) / MICRO_STEP_MODE) / AXE_DEC_GEAR_REDUC ) / DEC_EQ_M_GEAR_REDUC ) * 3600
RESOLUTION_ARCSEC_AD    =   ((((360 / MOTOR_SPR) / MICRO_STEP_MODE) / AXE_AD_GEAR_REDUC ) / AD_EQ_M_GEAR_REDUC ) * 3600
#
# RASPBERRY PI CONNECTIONS
#      ( BCM mode )
#
import RPi.GPIO as gpio
from RPi.GPIO import BCM, HIGH, LOW, OUT
gpio.setmode(BCM)
gpio.setwarnings(False)
"""
Driver Step/Dir PINs
"""
AD_DRIVER_PIN_DIR    = 20
AD_DRIVER_PIN_STEP   = 21
DEC_DRIVER_PIN_DIR   = 23
DEC_DRIVER_PIN_STEP  = 24
"""
Driver uStep mode (MS1,MS2) PINs
"""
AD_DRIVER   =  [25,8]
DEC_DRIVER  =  [6,13]
for pin in (AD_DRIVER + DEC_DRIVER) : gpio.setup(pin, OUT)
"""
Driver uStep set mode :
    +----------------+
    |   MKSTMC2209   |
    +----+-----+-----+
    | uS | MS1 | MS2 |
    +----+-----+-----+
    | 08 | GND | GND |
    +----+-----+-----+
    | 16 | VCC | VCC |
    +----+-----+-----+
    | 32 | VCC | GND |
    +----+-----+-----+
    | 64 | GND | VCC |
    +----+-----+-----+
DRIVER_MODE -> [MS1, MS2]
"""
DRIVER_MODE = [LOW,HIGH]
gpio.output(AD_DRIVER[0], DRIVER_MODE[0])
gpio.output(AD_DRIVER[1], DRIVER_MODE[1])
gpio.output(DEC_DRIVER[0], DRIVER_MODE[0])
gpio.output(DEC_DRIVER[1], DRIVER_MODE[1])