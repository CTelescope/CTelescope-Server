from time import sleep
import RPi.GPIO as gpio
import asyncio

# Constantes
MOTEUR_DEC_PIN_DIR = 20
MOTEUR_DEC_PIN_STEP = 21

MOTEUR_AD_PIN_DIR = 23
MOTEUR_AD_PIN_STEP = 24

CW = 1
CCW = 0

T = .0001

# 1 Pas = 0.009375°
SPR = 2400*16

DEBUG = True

# Setup Pin 
gpio.setmode(gpio.BCM)
gpio.setup(MOTEUR_DEC_PIN_DIR, gpio.OUT)
gpio.setup(MOTEUR_DEC_PIN_STEP, gpio.OUT)
gpio.setup(MOTEUR_AD_PIN_DIR, gpio.OUT)
gpio.setup(MOTEUR_AD_PIN_STEP, gpio.OUT)

async def makeAStep(step_pin: int):
    gpio.output(step_pin,gpio.HIGH)
    sleep(100*10**-8) # 100*10**-8 -> Voir doc du sheep TMC2209
    gpio.output(step_pin,gpio.LOW)
    sleep(100*10**-8)


async def doSteps(nb_steps: int, step_pin: int, dir_pin: int):
    if DEBUG:
        print("Nombre de pas : ", nb_steps )
        print("Frequence     : ", 1/T, "Hz")

    # Définition du sens de rotation
    if nb_steps < 0: 
        gpio.output(dir_pin,CCW)
    else:
        gpio.output(dir_pin,CW)

    print("...")
    # On effectue le nombre de pas
    for _ in range(abs(nb_steps)):
        await makeAStep(step_pin)
        sleep(T)
        #fais un tour complet en 15 secondes avec sleep(.0001) et environ 1 minutes 24 avec sleep(.001)

async def main():
    await asyncio.gather(
        asyncio.create_task(doSteps(2400*16, MOTEUR_DEC_PIN_STEP, MOTEUR_DEC_PIN_DIR)),
        asyncio.create_task(doSteps(-2400*16, MOTEUR_AD_PIN_DIR, MOTEUR_AD_PIN_STEP))
    )


if __name__ == "__main__":
    asyncio.run(main())