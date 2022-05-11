import RPi.GPIO as gpio
from RPi.GPIO import HIGH, LOW, OUT, BCM
from asyncio import sleep

from libraries.logger import setup_logger

logger = setup_logger(__file__)

# Setup Gpio Mode 
gpio.setmode(BCM)
gpio.setwarnings(False)

# Constantes GPIO
MOTEUR_DEC_PIN_DIR  = 20
MOTEUR_DEC_PIN_STEP = 21

MOTEUR_AD_PIN_DIR  = 23
MOTEUR_AD_PIN_STEP = 24

# Constantes Stepper Motor, Motor Driver, EQ3-2
MOTOR_SPR               =   2400         # P542-M481U-G17L82
MICRO_STEP_MODE         =   16           # TB6560
MIN_STEP_TIME_LEVEL     =   100 * 10**-8 # Voir le data sheet du sheep TMC2209 page 60
STEP_TIME               =   2 * MIN_STEP_TIME_LEVEL
DEC_EQ3_2_GEAR_REDUC    =   65
AD_EQ3_2_GEAR_REDUC     =   130
AXE_DEC_GEAR_REDUC      =   77/14
AXE_AD_GEAR_REDUC       =   44/16
RESOLUTION_ARCSEC_DEC   =   ((((360 / MOTOR_SPR) / MICRO_STEP_MODE) / AXE_DEC_GEAR_REDUC ) / DEC_EQ3_2_GEAR_REDUC ) * 3600.0000001192
RESOLUTION_ARCSEC_AD    =   ((((360 / MOTOR_SPR) / MICRO_STEP_MODE) / AXE_AD_GEAR_REDUC ) / AD_EQ3_2_GEAR_REDUC ) * 3600.0000001192

SLEEP_SPEED = {
    0.5 : (128 * (STEP_TIME)) - STEP_TIME,  # 0.000254s
    1   : (64 * (STEP_TIME)) - STEP_TIME,   # 0.000126s
    8   : (8 * (STEP_TIME)) - STEP_TIME,    # 1.4e-05s
    16  : (4 * (STEP_TIME)) - STEP_TIME,    # 6e-06s
    32  : (2 * (STEP_TIME)) - STEP_TIME,    # 2e-06s
    64  : (1 * (STEP_TIME)) - STEP_TIME     # 0.0s
}

class motor():
    def __init__(self, direction_pin: int, stepper_pin: int, name: str):
        self.name = name
        self.temporize = SLEEP_SPEED[1]
        self.direction_pin = direction_pin
        self.stepper_pin = stepper_pin
        self.busy = False
        # Set up motor pin
        gpio.setup(direction_pin, OUT)
        gpio.setup(stepper_pin, OUT)
    
    def _set_status(self, status: bool):
        self.busy = status
        logger.debug(f"STATUS : MOTOR {self.name} -> {self.busy}")

    def set_speed(self, mode):
        if not self.busy:
            if mode in SLEEP_SPEED:
                logger.success("Speed mode {mode} sets")
                self.temporize = SLEEP_SPEED[mode]
                return 0
            else:
                logger.failures("Speed mode {mode} does not exist")
                return 1
        else:
            logger.warning(f'Unable to set speed. The motor is busy...')
            return 2

    async def _make_a_step(self, step_pin: int):
        gpio.output(step_pin,HIGH)
        await sleep(MIN_STEP_TIME_LEVEL)
        gpio.output(step_pin,LOW)
        await sleep(MIN_STEP_TIME_LEVEL)


    async def do_steps(self, nb_steps: int ):
        #logger.info(f"Nombre de pas : {nb_steps}, Frequence : { (1 / (await self.get_speed() + STEP_TIME))}Hz" )
        # Définition du sens de rotation
        logger.info(f"MOTOR {self.name} : DIR_PIN={self.direction_pin} STEP_PIN={self.stepper_pin} NB STEPS={nb_steps}")
        
        if nb_steps < 0: gpio.output(self.direction_pin,LOW) # Sens horaire
        else: gpio.output(self.direction_pin,HIGH) # Sens anti horaire
        
        # On effectue le nombre de pas
        for _ in range(abs(nb_steps)):
            await self._make_a_step(self.stepper_pin)
            await sleep(self.temporize)
        
        logger.debug(f"MOTOR {self.name} : DIR_PIN={self.direction_pin} STEP_PIN={self.stepper_pin} | Done")