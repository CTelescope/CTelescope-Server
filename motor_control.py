from time import sleep

from raspberry_i2c_tb6612fng import MotorDriverTB6612FNG, TB6612FNGStepper

# Le paramètre est le nombre de tours par minute, la vitesse d'un stepper, 
#  allant de 1 à 300. Notez qu'un régime élevé conduira à un pas lâche, 
#  donc le régime ne doit pas être supérieur à 150
rpm = 90

driver = MotorDriverTB6612FNG(0x0f)

def Goto(mode: int, nb_step: int):
    # NOTE 48 seulement pour les anciens moteurs P542-M481U-G17L82
    driver.stepper_run(mode, nb_step*24, rpm)
    sleep(10)
    driver.stepper_stop()


if __name__ == '__main__':
    Goto(TB6612FNGStepper.FULL_STEP, -10)