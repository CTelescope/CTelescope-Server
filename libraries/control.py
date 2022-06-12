from libraries.logger import setup_logger, DEBUG
from libraries.config import RESOLUTION_ARCSEC_AD, RESOLUTION_ARCSEC_DEC, SIDERAL_SPEED_IN_SPS
from libraries.config import AD_DRIVER_PIN_DIR, AD_DRIVER_PIN_STEP, DEC_DRIVER_PIN_DIR, DEC_DRIVER_PIN_STEP
from libraries.motor import motor

from astropy.coordinates import SkyCoord
import astropy.units as u

from threading import Thread
from time import sleep, perf_counter
import math

logger = setup_logger(__file__, DEBUG)

# Compensation rot terre
CRT_STATUS = False
# Instantiation des moteurs
MOTEUR_AD  = motor(AD_DRIVER_PIN_DIR, AD_DRIVER_PIN_STEP, "AD", SIDERAL_SPEED_IN_SPS["AD"])
MOTEUR_DEC = motor(DEC_DRIVER_PIN_DIR, DEC_DRIVER_PIN_STEP, "DEC", SIDERAL_SPEED_IN_SPS["DEC"])
# Default user input for the manual control of the mount
hc_output = {"AD":0, "DEC":0} 
timer_last_hc_output = 0
# Initial position debug
current_position = SkyCoord("2h31m0s", "+89°15\'0\"") # coord étoile polaire 

def set_motors_speed(speedAD, speedDEC):
    MOTEUR_AD.set_speed(speedAD)
    MOTEUR_DEC.set_speed(speedDEC)

def get_motors_speed():
    return { 
        "AD":MOTEUR_AD.get_speed(), 
        "DEC": MOTEUR_DEC.get_speed()
    }

def get_position():
    return {
        "AD":current_position.ra.to_string(),
        "Dec":current_position.dec.to_string(),
    }

def comp_earth_rot(active:bool):
    global CRT_STATUS
    CRT_STATUS = active

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


def process_hc_output(AD, DEC):
    timer_last_hc_output = perf_counter()
    hc_output["AD"] = AD
    hc_output["DEC"] = DEC



def _motors_steps_loop():
    
    steps_per_ms_AD = SIDERAL_SPEED_IN_SPS["AD"] / 10
    steps_per_ms_DEC = SIDERAL_SPEED_IN_SPS["DEC"] / 10

    print( steps_per_ms_AD, steps_per_ms_DEC)

    while True:
        global CRT_STATUS
        MOTEUR_AD.add_steps(round(steps_per_ms_AD * MOTEUR_AD.get_speed() * hc_output["AD"]))
        MOTEUR_DEC.add_steps(round(steps_per_ms_DEC * MOTEUR_DEC.get_speed() * hc_output["DEC"]))

        if (perf_counter() - timer_last_hc_output) >= 300:
            # logger.warning("user stop manual control")
            hc_output["AD"] = 0
            hc_output["DEC"] = 0

        # CRT si activé
        if CRT_STATUS is True:
            logger.debug("compensation rotation terre")
            MOTEUR_AD.add_steps(round(steps_per_ms_AD))
        
        sleep(0.1) 