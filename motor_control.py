from time import sleep
import RPi.GPIO as gpio

DIR = 20
STEP = 21

CW = 1
CCW = 0

gpio.setmode(gpio.BCM)
gpio.setup(DIR, gpio.OUT)
gpio.setup(STEP, gpio.OUT)

# 1 Pas = 0.009375°
SPR = 2400*16

def doStep(nb_step: int):
    # Sens
    if nb_step < 0: 
        gpio.output(DIR,CW)
    else:
        gpio.output(DIR,CCW)
    
    # On effectue le nombre de pas
    for _ in range(abs(nb_step)):
        gpio.output(STEP,gpio.HIGH)
        sleep(.0001)
        gpio.output(STEP,gpio.LOW)
        sleep(.0001)