from libraries.motor import MOTEUR_AD_PIN_DIR, MOTEUR_AD_PIN_STEP, MOTEUR_DEC_PIN_DIR, MOTEUR_DEC_PIN_STEP, RESOLUTION_ARCSEC_AD, RESOLUTION_ARCSEC_DEC
from libraries.motor import motor
from libraries.logger import setup_logger

from astropy.coordinates import SkyCoord
import astropy.units as u

from asyncio import gather, run
import math

logger = setup_logger(__file__)

MOTEUR_AD  = motor(MOTEUR_AD_PIN_DIR, MOTEUR_AD_PIN_STEP, "AD")
MOTEUR_DEC = motor(MOTEUR_DEC_PIN_DIR, MOTEUR_DEC_PIN_STEP, "DEC")

HOME = SkyCoord('8h50m59.75s', '+11d39m22.15s') # Etoile polaire coord ?
current_position = HOME

def set_speed_AD(speed):
    MOTEUR_AD.set_speed(speed)

def set_speed_DEC(speed):
    MOTEUR_DEC.set_speed(speed)

def get_position() -> dict:
    return {
        "AD":current_position.ra.to_string(),
        "Dec":current_position.dec.to_string(),
    }

async def goto(destination) -> tuple:
    
    AD, DEC = current_position.spherical_offsets_to(destination)

    logger.debug(f"Goto : AD = {AD}arc\", DEC = {DEC}arc\"")
     
    steps_AD  = AD.to(u.arcsec) / RESOLUTION_ARCSEC_AD
    steps_Dec = DEC.to(u.arcsec) / RESOLUTION_ARCSEC_DEC

    logger.debug(f"Steps : AD = {steps_AD}, DEC = {steps_Dec}")

    # TODO : if nb step > tour complet du telescope -> throw error

    coroutines = [
        MOTEUR_AD.do_steps(2400*16), 
        MOTEUR_DEC.do_steps(-2400*16),
    ]
    
    res = await gather(*coroutines, return_exceptions=True)
    return res