Documentation
#################

Installation
******************

Conditions
================
Ce projet nécessite un nano-ordinateur de chez Raspberry, une caméra USB, 2 interfaces moteur TMC2209 et deux interfaces WIFI. Il est fortement recommandé d'utiliser une RPI 3 ou 4 pour garantir des performances convenables car la gestion des moteurs et de la vidéo en threading son gourmand en ressources CPU.

Une version récente du système d'exploitation Raspbian est recommandée avec python3. Et enfin assurez-vous que le matériel utilisé est fonctionnel.

Environnements
----------------------

**Circuit**
^^^^^^^^^^^^^

Les branchements par défaut du raspberry correspondent au schéma ci-dessous :

.. figure:: ./images/fig1.PNG
    :align: center
    :alt: schema_raspberry
    :figclass: align-center



.. code-block:: python

   # Driver Step/Dir PIN
   AD_DRIVER_PIN_DIR    = 20
   AD_DRIVER_PIN_STEP   = 21
   DEC_DRIVER_PIN_DIR   = 23
   DEC_DRIVER_PIN_STEP  = 24
   # Driver Step mode PIN
   AD_DRIVER_PIN_1   = 25
   AD_DRIVER_PIN_2   = 8
   DEC_DRIVER_PIN_1  = 6
   DEC_DRIVER_PIN_2  = 13

.. note:: Les PIN choisis peuvent être change dans le fichier *libraries/goto.py* 

**Dévellopement**
^^^^^^^^^^^^^^^^^^^^^^

Procédure d'installation de l'environnement de développement :

.. code-block:: bash

   $ cd $home
   $ git clone https://github.com/CTelescope/CTelescope-Server.git
   $ cd CTelescope-Server
   $ pip install -r requirements.txt
   $ sudo dpkg -i mjpg-streamer_2.0_armhf.deb

Commande pour lancer le flux MJPEG :

.. code-block:: bash
   
   $ mjpg_streamer -i "input_uvc.so -r 640x480 -d /dev/video0 -f 24 -q 80" -o "output_http.so -p 8080"

Commande pour démarrer le serveur :

.. code-block:: bash
   
   $ python3 main.py

**Production**
^^^^^^^^^^^^^^^^^^^^^^

Pour la mise en production du CTelescope-Server sur la Raspberry Pi vous devrez procéder effectuer les étapes ci-dessous : 

.. attention:: Après cette opération le raspberry sera accessible uniquement en WIFI avec l'adresse IPv4 défini dans le script !

.. code-block:: bash

   $ cd $home
   $ git clone https://github.com/CTelescope/CTelescope-Server.git
   $ cd CTelescope-Server/install
   # Options du scripts
   $ nano install.sh
         WLAN="0"
         WLAN_IP="10.0.0.249"
         WLAN_GW="10.0.0.254"
         WLAN_NM="255.255.255.248"

         SSID="CTelescope"
         PWD="telescope_bts_snir"
         NB_CLIENT=1

   $ sudo chmod +x ./install.sh
   $ sudo ./install.sh
   $ sudo reboot

.. note:: Le raspberry lancera automatiquement a son démarrage le point d'accès WIFI, le CTelescope-Server ainsi que le flux MJPEG. 

Documentation du code
=====================

.. toctree::
   :maxdepth: 7

   libraries

.. toctree::
   :maxdepth: 7

   routes

Index
=====

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

