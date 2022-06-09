import RPi.GPIO as gpio
from RPi.GPIO import HIGH, LOW, OUT
from threading import Thread
from time import sleep

from libraries.logger import setup_logger, DEBUG
from libraries.config import MIN_STEP_TIME_LEVEL, DRIVER_MODE, STEP_TIME, SIDERAL_SPEED_IN_SPS

logger = setup_logger(__file__, DEBUG)

"""
Dictionnaire contenant les différentes temporisation
"""
SLEEP_SPEED = {
    0.5 :  ((STEP_TIME * SIDERAL_SPEED_IN_SPS) / 0.5) / 1,
    1   :  ((STEP_TIME * SIDERAL_SPEED_IN_SPS) / 1) / 1,
    8   :  ((STEP_TIME * SIDERAL_SPEED_IN_SPS) / 8) / 1,
    16  :  ((STEP_TIME * SIDERAL_SPEED_IN_SPS) / 16) / 1,
    32  :  ((STEP_TIME * SIDERAL_SPEED_IN_SPS) / 32) / 1,
    64  :  ((STEP_TIME * SIDERAL_SPEED_IN_SPS) / 64) / 1,
}

class motor():
    """
    Constructeur
    """
    def __init__(self, direction_pin: int, stepper_pin: int, id: str):
        self.id = id 
        self.temporize = SLEEP_SPEED[1]
        self.direction_pin = direction_pin
        self.stepper_pin = stepper_pin

        self.steps_buffer = 0

        gpio.setup(direction_pin, OUT)
        gpio.setup(stepper_pin, OUT)

        Thread(target=self._steps_loop, daemon=True).start()

    """
    Permet d'effectuer un pas avec un échelon haut bas 
    """
    def _make_a_step(self, step_pin: int):
        gpio.output(step_pin,HIGH)
        sleep(MIN_STEP_TIME_LEVEL)
        gpio.output(step_pin,LOW)
        sleep(MIN_STEP_TIME_LEVEL)

    """
    Procédure qui est executer dans un trread lors du constructeur
        permettant d'effectuer le nombre de pas dans l'attribus 
        steps_buffer
    """
    def _steps_loop(self):
        while True:
            tmp_steps_buffer = self.steps_buffer
            if tmp_steps_buffer != 0:

                logger.status(f"MOTOR {self.id} + {tmp_steps_buffer} step(s)")
                
                # Définition du sens de rotation
                if tmp_steps_buffer < 0: 
                    gpio.output(self.direction_pin,LOW) # Sens horaire
                else: 
                    gpio.output(self.direction_pin,HIGH) # Sens anti horaire

                # On effectue le nombre de pas
                for _ in range(abs(tmp_steps_buffer)):
                    self._make_a_step(self.stepper_pin)
                    sleep(self.temporize)

                # On enleve le nombre de pas effectuer du buffer
                self.steps_buffer -= tmp_steps_buffer

                logger.status(f"MOTOR {self.id} step(s) done")
            else:
                sleep(0.01)

    """
    Permet de définir la vitesse
    """ 
    def set_speed(self, mode: any):
        if mode in SLEEP_SPEED:
            logger.success(f"{self.id} : speed mode set to {mode}")
            self.temporize = SLEEP_SPEED[mode]
        elif mode == 0:
            logger.warning(f"{self.id} : no change needed, speed mode {mode}")
        else:
            logger.failures(f"{self.id} : Speed mode {mode} does not exist")

    """
    Methode pour récuperer la vitesse qui est utilisé par le moteur
    """
    def get_speed(self):
        return list(SLEEP_SPEED.keys())[list(SLEEP_SPEED.values()).index(self.temporize)]

    """
    Permet de rajouter des pas a effectuer 
    """
    def add_steps(self, nb_steps: int ):
        self.steps_buffer += nb_steps