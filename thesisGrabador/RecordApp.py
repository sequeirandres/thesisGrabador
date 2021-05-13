# ------------------------------------------------------
from PyQt5.QtWidgets import*
from PyQt5.QtWidgets import QMessageBox
from PyQt5.uic import loadUi
from PyQt5.QtGui import QIcon 
import sys
import matplotlib.pyplot as plt
import numpy as np
import pyaudio
from scipy import signal
import wave
import os, shutil
from plataforma import Plataform
from parameters import*
# time for back the plataform
import time
from functions import deleteFiles,saveFile
from classRecord import Records

#__author__ = 'sequera@andres'
#__title__ = 'Record_Files_wav_for_radar_fwmc'

# 40 % @1m 
# --- vel  = 0.113 m/s ---

# 4 bottons :
#   1.- start
#   2.- stop
#   3.- back
#   4.- exit

# ---  main ---- 
if __name__ == "__main__":
    app = QApplication(sys.argv)
    rec = Records()
    rec.show()
    app.exec_()
# ----

