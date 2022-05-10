import RPi.GPIO as gpio
import asyncio
from libraries.logger import setup_logger

logger = setup_logger(__file__)

gpio.setwarnings(False)

# Constantes
MOTEUR_DEC_PIN_DIR = 20
MOTEUR_DEC_PIN_STEP = 21

MOTEUR_AD_PIN_DIR = 23
MOTEUR_AD_PIN_STEP = 24

CW = 1  # Sens horaire
CCW = 0 # Sens anti horaire

T = .0001

# 1 Pas = 0.009375°
SPR = 2400*16

# Setup Pin 
gpio.setmode(gpio.BCM)
gpio.setup(MOTEUR_DEC_PIN_DIR, gpio.OUT)
gpio.setup(MOTEUR_DEC_PIN_STEP, gpio.OUT)
gpio.setup(MOTEUR_AD_PIN_DIR, gpio.OUT)
gpio.setup(MOTEUR_AD_PIN_STEP, gpio.OUT)

async def make_a_step(step_pin: int):
    gpio.output(step_pin,gpio.HIGH)
    await asyncio.sleep(100*10**-8) # 100*10**-8 -> Voir doc du sheep TMC2209
    gpio.output(step_pin,gpio.LOW)
    await asyncio.sleep(100*10**-8)


async def do_steps(nb_steps: int, step_pin: int, dir_pin: int):
    logger.info(f"Step pin : {step_pin}, Direction pin : {dir_pin}, Nombre de pas : {nb_steps}, Frequence : {1/T}Hz" )

    # Définition du sens de rotation
    if nb_steps < 0: 
        gpio.output(dir_pin,CCW)
    else:
        gpio.output(dir_pin,CW)

    # On effectue le nombre de pas
    for _ in range(abs(nb_steps)):
        await make_a_step(step_pin)
        await asyncio.sleep(T)
        #fais un tour complet en 15 secondes avec sleep(.0001) et environ 1 minutes 24 avec sleep(.001)

async def goto(NB_STEPS_MOTEUR_AD = 0, NB_STEPS_MOTEUR_DEC = 0):
    coroutines = [
        do_steps(NB_STEPS_MOTEUR_AD, MOTEUR_DEC_PIN_STEP, MOTEUR_DEC_PIN_DIR), 
        do_steps(NB_STEPS_MOTEUR_DEC, MOTEUR_AD_PIN_DIR, MOTEUR_AD_PIN_DIR),
    ]
    res = await asyncio.gather(*coroutines, return_exceptions=True)
    logger.debug(res)
    return res

if __name__ == "__main__":
    res = asyncio.run(goto(NB_STEPS_MOTEUR_AD = 2400, NB_STEPS_MOTEUR_DEC = -2400))

    if res[0] == None and res[1]==None:
        logger.success("Done")
    else :
        logger.failures("")


    gpio.cleanup()