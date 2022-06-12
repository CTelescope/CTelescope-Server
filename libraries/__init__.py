from libraries.control import _motors_steps_loop
from threading import Thread

# On lance le thread contenant la boucle infini pour la compenser 
#  la rotation de la terre (si COMP_ROT_STATUS est a True)
Thread(target=_motors_steps_loop, daemon=True).start()