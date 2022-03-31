from time import sleep
import RPi.GPIO as gpio

PIN_DIR = 20
PIN_STEP = 21

CW = 1
CCW = 0

gpio.setmode(gpio.BCM)
gpio.setup(PIN_DIR, gpio.OUT)
gpio.setup(PIN_STEP, gpio.OUT)

# 1 Pas = 0.009375°
SPR = 2400*16

def doSteps(nb_steps: int):
    # Sens
    if nb_steps < 0: 
        gpio.output(PIN_DIR,CW)
    else:
        gpio.output(PIN_DIR,CCW)
    
    # On effectue le nombre de pas
    for _ in range(abs(nb_steps)):
        gpio.output(PIN_STEP,gpio.HIGH)
        sleep(.0001)
        gpio.output(PIN_STEP,gpio.LOW)
        sleep(.0001)

if __name__ == "__main__":
    doSteps(2400*16)