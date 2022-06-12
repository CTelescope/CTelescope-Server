import RPi.GPIO as gpio
from RPi.GPIO import HIGH, LOW, OUT
from threading import Thread
from time import sleep

from libraries.logger import setup_logger, DEBUG
from libraries.config import MIN_STEP_TIME_LEVEL, DRIVER_MODE, STEP_TIME

logger = setup_logger(__file__, DEBUG)


class motor():
    """
    Constructeur
    """
    def __init__(self, direction_pin: int, stepper_pin: int, log_id: str, step_per_sideral_sec: float):

        self.log_id = log_id
        self.step_per_sideral_sec = step_per_sideral_sec
        # Generation des différentes temporisation correspondant a chaque vitesses
        TIMING_STEP = {
            0.5 :  ((STEP_TIME * self.step_per_sideral_sec) / 0.5) / 1,
            1   :  ((STEP_TIME * self.step_per_sideral_sec) / 1) / 1,
            8   :  ((STEP_TIME * self.step_per_sideral_sec) / 8) / 1,
            16  :  ((STEP_TIME * self.step_per_sideral_sec) / 16) / 1,
            32  :  ((STEP_TIME * self.step_per_sideral_sec) / 32) / 1,
            64  :  ((STEP_TIME * self.step_per_sideral_sec) / 64) / 1,
        }
        self.TIMING_STEP = TIMING_STEP
        # la vitesse par défaut est définit par 1 (correspondant donc a la Vitesse sideral)
        self.delay_speed_steps = TIMING_STEP[1]
        # Buffer des pas a éffectuer
        self.steps_buffer = 0
        # Pin des driver choisi
        self.direction_pin = direction_pin
        self.stepper_pin = stepper_pin
        # Set up des pin
        gpio.setup(self.direction_pin, OUT)
        gpio.setup(self.stepper_pin, OUT)
        # Lancement du Thread qui effectu les pas contenu dans le steps buffer
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

                logger.status(f"MOTOR {self.log_id} + {tmp_steps_buffer} step(s)")
                
                # Définition du sens de rotation
                if tmp_steps_buffer < 0: 
                    gpio.output(self.direction_pin,LOW) # Sens horaire
                else: 
                    gpio.output(self.direction_pin,HIGH) # Sens anti horaire

                # On effectue le nombre de pas
                for _ in range(abs(tmp_steps_buffer)):
                    self._make_a_step(self.stepper_pin)
                    sleep(self.delay_speed_steps)

                # On enleve le nombre de pas effectuer du buffer
                self.steps_buffer -= tmp_steps_buffer

                logger.status(f"MOTOR {self.log_id} step(s) done")
            else:
                sleep(0.001)

    """
    Permet de définir la vitesse
    """ 
    def set_speed(self, mode: any):
        if mode in self.TIMING_STEP:
            logger.success(f"{self.log_id} : speed mode set to {mode}")
            self.delay_speed_steps = self.TIMING_STEP[mode]
        elif mode == 0:
            logger.warning(f"{self.log_id} : no change needed, speed mode {mode}")
        else:
            logger.failures(f"{self.log_id} : Speed mode {mode} does not exist")

    """
    Methode pour récuperer la vitesse qui est utilisé par le moteur
    """
    def get_speed(self):
        return list(self.TIMING_STEP.keys())[list(self.TIMING_STEP.values()).index(self.delay_speed_steps)]

    """
    Permet de rajouter des pas a effectuer 
    """
    def add_steps(self, nb_steps: int, isgotocoord = False):
        if -15000 < self.steps_buffer < 15000 or isgotocoord :
            self.steps_buffer += nb_steps
        else :
            logger.warning(f"MOTOR : {self.log_id} steps_buffer reached the max value.")