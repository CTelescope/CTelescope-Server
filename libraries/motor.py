import RPi.GPIO as gpio
from RPi.GPIO import HIGH, LOW, OUT, BCM
from time import sleep
from threading import Thread

from libraries.logger import setup_logger, DEBUG

logger = setup_logger(__file__, DEBUG)

# Setup Gpio Mode 
gpio.setmode(BCM)
gpio.setwarnings(False)

# Constantes GPIO
MOTEUR_DEC_PIN_DIR  = 20
MOTEUR_DEC_PIN_STEP = 21

MOTEUR_AD_PIN_DIR  = 23
MOTEUR_AD_PIN_STEP = 24

# Constantes Stepper Motor, Motor Driver, EQ3-2
MOTOR_SPR               =   400         # 
MICRO_STEP_MODE         =   64          # TMC2209
MIN_STEP_TIME_LEVEL     =   100 * 10**-8 # Voir le data sheet du sheep TMC2209 page 60
STEP_TIME               =   2 * MIN_STEP_TIME_LEVEL
DEC_EQ3_2_GEAR_REDUC    =   65
AD_EQ3_2_GEAR_REDUC     =   130
AXE_DEC_GEAR_REDUC      =   77/14
AXE_AD_GEAR_REDUC       =   44/16
RESOLUTION_ARCSEC_DEC   =   ((((360 / MOTOR_SPR) / MICRO_STEP_MODE) / AXE_DEC_GEAR_REDUC ) / DEC_EQ3_2_GEAR_REDUC ) * 3600
RESOLUTION_ARCSEC_AD    =   ((((360 / MOTOR_SPR) / MICRO_STEP_MODE) / AXE_AD_GEAR_REDUC ) / AD_EQ3_2_GEAR_REDUC ) * 3600


SLEEP_SPEED = {
    0.5 : (128 * (STEP_TIME)) - STEP_TIME,  # 0.000254s
    1   : (64 * (STEP_TIME)) - STEP_TIME,   # 0.000126s
    8   : (8 * (STEP_TIME)) - STEP_TIME,    # 1.4e-05s
    16  : (4 * (STEP_TIME)) - STEP_TIME,    # 6e-06s
    32  : (2 * (STEP_TIME)) - STEP_TIME,    # 2e-06s
    64  : (1 * (STEP_TIME)) - STEP_TIME     # 0.0s
}

class motor():
    # Constructor
    def __init__(self, direction_pin: int, stepper_pin: int, name: str):
        self.name = name
        self.temporize = SLEEP_SPEED[1]
        self.direction_pin = direction_pin
        self.stepper_pin = stepper_pin

        self.steps_buffer = 0
        self.motor_enable = False
        self.busy = False

        gpio.setup(direction_pin, OUT)
        gpio.setup(stepper_pin, OUT)

        self.motor_loop = Thread(target=self._steps_loop)
        self.motor_enable = True
        self.motor_loop.start()
        
    # Destructor
    def __del__(self):
        self._stop_stepper_loop()

    def _start_stepper_loop(self) :
        if not self.motor_enable:
            self.motor_enable = True
            self.motor_loop.start()

    def _stop_stepper_loop(self) -> None:
        if self.motor_enable:
            self.motor_enable = False
            self.motor_loop.join()

    def _make_a_step(self, step_pin: int):
        gpio.output(step_pin,HIGH)
        sleep(MIN_STEP_TIME_LEVEL)
        gpio.output(step_pin,LOW)
        sleep(MIN_STEP_TIME_LEVEL)

    def _steps_loop(self):
        while True:
            tmp_steps_buffer = self.steps_buffer
            if tmp_steps_buffer != 0:

                logger.status(f"MOTOR {self.name} : NB STEPS={tmp_steps_buffer}")
                
                # Définition du sens de rotation
                if tmp_steps_buffer < 0: gpio.output(self.direction_pin,LOW) # Sens horaire
                else: gpio.output(self.direction_pin,HIGH) # Sens anti horaire

                # On effectue le nombre de pas
                for _ in range(abs(tmp_steps_buffer)):
                    self._make_a_step(self.stepper_pin)
                    sleep(self.temporize)

                self.steps_buffer -= tmp_steps_buffer

                logger.status(f"MOTOR {self.name} : Done")

            else:
                sleep(0.15)
                logger.debug("Waiting steps")

    def set_speed(self, mode):
        if mode in SLEEP_SPEED:
            logger.success(f"Speed mode {mode} sets")
            self.temporize = SLEEP_SPEED[mode]
            return 0
        else:
            logger.failures(f"Speed mode {mode} does not exist")
            return 1

    # Permet de rajouter des pas au "steps buffer" 
    def add_steps(self, nb_steps: int ):
        self.steps_buffer += nb_steps