from libraries.goto import _loop_comp_rot_earth
from threading import Thread

# On lance le thread contenant la boucle infini pour la compenser 
#  la rotation de la terre (si COMP_ROT_STATUS est a True)
Thread(target=_loop_comp_rot_earth, daemon=True).start()