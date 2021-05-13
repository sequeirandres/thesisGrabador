# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------
#
#  Title: control de plataforma movil wifi esp8266
#  Code :  main.py  
#  Author: Sequeira Andres
#  gitHub: https://github.com/sequeirandres/
#  Repositorio: https://github.com/sequeirandres/thesisGrabador
#
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------

from parameters import*
from credentials import*
from classPlataform import Plataform
from PyQt5.QtWidgets import*
import requests                # https://IP_esp8266Wifi/action=?&speed=?
import sys
import time
import numpy as np # need round

#__author__ = 'sequera@andres'
#__title__ = 'Plataform_to_control_radar_fwmc'

# GET & POST 
#  /action=?&speed=?  
# 
# http:/DNS_NAME/action=? 
# post and gets 

if __name__ == "__main__":
    app = QApplication(sys.argv)
    pltfm = Plataform()
    pltfm.show()
    app.exec_()