from libraries.motor import MOTEUR_AD_PIN_DIR, MOTEUR_AD_PIN_STEP, MOTEUR_DEC_PIN_DIR, MOTEUR_DEC_PIN_STEP, RESOLUTION_ARCSEC_AD, RESOLUTION_ARCSEC_DEC
from libraries.motor import motor
from libraries.logger import setup_logger

from astropy.coordinates import SkyCoord
import astropy.units as u

from asyncio import gather, run
import math

logger = setup_logger(__file__)

MOTEUR_AD  = motor(MOTEUR_AD_PIN_DIR, MOTEUR_AD_PIN_STEP)
MOTEUR_DEC = motor(MOTEUR_DEC_PIN_DIR, MOTEUR_DEC_PIN_STEP)

HOME = SkyCoord('8h50m59.75s', '+11d39m22.15s', frame="icrs") # Etoile polaire coord ?
current_position = HOME

def get_position() -> dict:
    return {
        "AD":current_position.ra.to_string(),
        "Dec":current_position.dec.to_string(),
    }

async def goto(destination) -> tuple:
    
    AD, DEC = current_position.spherical_offsets_to(destination)

    logger.debug(f"Goto : AD = {AD.to(u.arcsec)}arc\", DEC = {DEC.to(u.arcsec)}arc\"")
     
    # steps_AD  = round(AD.to(u.arcsec) / RESOLUTION_ARCSEC_AD)
    # steps_Dec = round(DEC.to(u.arcsec) / RESOLUTION_ARCSEC_DEC)

    # logger.debug(f"Steps : AD = {steps_AD}, DEC = {steps_Dec}")

    # TODO : if nb step > tour complet du telescope -> throw error

    coroutines = [
        MOTEUR_AD.do_steps(2400*16), 
        MOTEUR_DEC.do_steps(2400*16),
    ]
    
    res = await gather(*coroutines, return_exceptions=True)
    return res


if __name__ == "__main__":
    res = run(goto(NB_STEPS_MOTEUR_AD = 2400, NB_STEPS_MOTEUR_DEC = -2400))

    if res[0] == None and res[1]==None:
        logger.success("Done")
    else :
        logger.failures("")