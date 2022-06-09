from libraries.motor import RESOLUTION_ARCSEC_AD, RESOLUTION_ARCSEC_DEC
from libraries.motor import motor
from libraries.logger import setup_logger, DEBUG

from astropy.coordinates import SkyCoord
import astropy.units as u

from threading import Thread
from time import sleep
import RPi.GPIO as gpio
from RPi.GPIO import BCM
import math

logger = setup_logger(__file__, DEBUG)

# Setup Gpio Mode 
gpio.setmode(BCM)
gpio.setwarnings(False)
# Driver Step/Dir PIN
AD_DRIVER_PIN_DIR    = 20
AD_DRIVER_PIN_STEP   = 21
DEC_DRIVER_PIN_DIR   = 23
DEC_DRIVER_PIN_STEP  = 24
# Driver Step mode PIN
AD_DRIVER_PIN_1   = 25
AD_DRIVER_PIN_2   = 8
DEC_DRIVER_PIN_1  = 6
DEC_DRIVER_PIN_2  = 13

# Instantiation des moteurs
MOTEUR_AD  = motor(AD_DRIVER_PIN_DIR, AD_DRIVER_PIN_STEP, "AD")
MOTEUR_DEC = motor(DEC_DRIVER_PIN_DIR, DEC_DRIVER_PIN_STEP, "DEC")
# Compensation rotation de la terre en arc/s
COMP_ROT_ARCSEC       =   (360/23.9345) / 3600 
# On a besoin de 0,016712.. arcsec pour compenser la rotation de la terre.
# Notre résolution de pas est de 0,14160.. arcsec
# On a donc besion d'attendre RESOLUTION_ARCSEC_AD / COMP_ROT_ARCSEC
#     avant de faire un pas.
TEMPO_COMP_ROT_P_STP  =   RESOLUTION_ARCSEC_AD / COMP_ROT_ARCSEC
COMP_ROT_STATUS       =   False

current_position = SkyCoord("2h31m0s", "+89°15\'0\"") # coord étoile polaire 

def set_speed(speedAD, speedDEC):
    MOTEUR_AD.set_speed(speedAD)
    MOTEUR_DEC.set_speed(speedDEC)

def get_speed():
    return { "AD":MOTEUR_AD.get_speed(), "DEC": MOTEUR_DEC.get_speed()}

def get_position():
    return {
        "AD":current_position.ra.to_string(),
        "Dec":current_position.dec.to_string(),
    }

def do_steps(AD_steps, DEC_steps):
    MOTEUR_AD.add_steps(AD_steps)
    MOTEUR_DEC.add_steps(DEC_steps)

def comp_earth_rot(active:bool):
    COMP_ROT_STATUS = active

def set_current_position():
    # WIP
    None

def set_speed_by_distance(nb_steps: int):
    # WIP
    None

def goto(destination):
    # WIP
    logger.info(f"current position : {current_position}")
    logger.info(f"destination : {destination}")
    
    AD, DEC = current_position.spherical_offsets_to(destination)

    logger.info(f"Goto : AD = {AD}\", DEC = {DEC}\"")
     
    steps_AD  = AD / RESOLUTION_ARCSEC_AD
    steps_Dec = DEC / RESOLUTION_ARCSEC_DEC

    logger.debug(f"Steps to do : AD = {steps_AD}, DEC = {steps_Dec}")
   
    # MOTEUR_AD.add_steps(steps_AD)
    # MOTEUR_DEC.add_steps(steps_Dec)
    
    comp_earth_rot(True)

def _loop_comp_rot_earth():
    while True:
        if COMP_ROT_STATUS is True:
            MOTEUR_AD.add_steps(1)
            logger.debug("compensation rotation de la terre")
        sleep(TEMPO_COMP_ROT_P_STP)