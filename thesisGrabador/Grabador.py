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
# time for back the plataform
import time

#__author__ = 'sequera@andres'
#__title__ = 'Record_Files_wav_for_radar_fwmc'

# 40 % @1m 
# --- vel  = 0.113 m/s ---

# Parámetros generales 

CHUNK = 2
# FORMAT = pyaudio.paInt16
FORMAT = pyaudio.paInt16                # tipo de codificacion
CHANNELS = 2                            # cantidad de canales
RATE = 44100                            # frecuencia de muentreo 
RECORD_SECONDS = 10                     # tiempo de grabacion, se ajusta segun los requerimientos 
WAVE_OUTPUT_FILENAME = "measurements"   # Nombre por default que los archivos grabados .wav tendran

TIME_FREE = 600 # 10 MINUTOS FREE TO RECORD
SPEED_40 = 20  # cm/s 


MODE_SCAN = 'scan'
MODE_LISEN ='lisen'


# ----------  funciones Generales ----------

# Delete Files 
def deleteFiles(directoryPath):
    for the_file in os.listdir(directoryPath):
        file_path = os.path.join(directoryPath, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            #Elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)

# Save Files 
def saveFile(frames, NameFile , Sample_size):
    wf = wave.open(NameFile,'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(Sample_size)
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    print('Save File [' ,NameFile ,'] Done!' )

# 4 bottons :

#   1.- start
#   2.- stop
#   3.- back
#   4.- exit

class AppRecord(QMainWindow):
    def __init__(self):
    #def __init__(self,pointerToAppSar):
        print(' ---  App Record files  ---')
        print('loaded ')
        QMainWindow.__init__(self)
        loadUi("ReadWavGuiApp.ui",self)  
        #self.radar = pointerToAppSar                   #  <-- pointer to back
        self.setWindowTitle("Record files wav for radar SAR")
        self.setWindowIcon(QIcon('Icono_python.ico')) 

        # set icons
        self.ButtonExit.setIcon(QIcon('icono_exit.ico')) 
        #self.ButtonRecord.setIcon(QIcon('icono_record.ico')) 
        #self.ButtonNext.setIcon(QIcon('icono_next.ico')) 

        # Buttons :
        self.ButtonExit.clicked.connect( self.AppExit )
        self.ButtonStart.clicked.connect( self.AppRecord)
        self.ButtonStop.clicked.connect(self.AppStop)
        self.ButtonBackToInit.clicked.connect(self.AppBackToInit)
        self.ButtonRadarOnOff.clicked.connect(self.AppRadarOnOff)            ######### here  ##
        self.ButtonNext.clicked.connect(self.stepsTorecord)
        self.ButtonSetTimeFree.clicked.connect(self.setTimeFree)
    
        #self.ButtonNext.clicked.connect(self.NextRecord)
        # SpinBox change value 'Distance' :
        self.PlataformDistance.valueChanged.connect(self.UpdateTime)

        # spinbox change value 'Speed'
        self.PlataformSpeed.valueChanged.connect(self.UpdateSpeed)

        self.counter = 0 
        self.statusBar.setValue(0)
        self.NameFile.setText(WAVE_OUTPUT_FILENAME)
        #self.TimeValue.setValue(RECORD_SECONDS)
        #self.RateValue.setValue(RATE)
        #self.groupBoxOptions.setEnabled(False)
        #self.pushButtonNext.setEnabled(False)
       # self.TextStatus.setText('waiting to record')

        # option to record files from input
        self.format = FORMAT
        self.rate = RATE 
        self.frame_per_buffer =CHUNK
        self.channels = CHANNELS

        self.RecordStatus.setText('Stopped')

        self.pltfrm = Plataform()                 ## me creo una variable para utilizar las funciones de la plataforma
        
        # set distance por default :
        #$self.radar.distanceAcimut =  self.PlataformDistance.value()   ### set distance in acimuth 

        self.time_to_record = int( self.PlataformDistance.value()/SPEED_40 )
##        print('Velocidad  :',SPEED_40)
##        print('Distance:',self.PlataformDistance.value() )
##        print('time :',  int( self.PlataformDistance.value()/SPEED_40 ), 'seg')
        self.ButtonStop.setEnabled(False)
        self.ButtonBackToInit.setEnabled(False)
        self.ButtonNext.setEnabled(False)

        
        self.ButtonModeScan.setChecked(True)
        self.ButtonRunManual.setChecked(True)

        self.ButtonModeScan.clicked.connect(self.setMode)
        self.ButtonModeLisen.clicked.connect(self.setMode)
        
        self.mode = MODE_SCAN 
        ##
        #self.groupBoxPlataformOptions.setEnabled(False)
        #self.PlataformSpeed.setEnabled(False)
    def setMode(self):
        if self.ButtonModeScan.isChecked() :
            self.mode = MODE_SCAN
            print('set mode scan')
        else:
            self.mode = MODE_LISEN
            print('set mode lisen')

        

    def setTimeFree(self):
        if self.ButtonSetTimeFree.isChecked() :
            print('set up time free ON')
            self.time_to_record = TIME_FREE  # 10 minutos, extremadamente grande
        else:
            print('set up time free OFF')
            self.UpdateTime()
            #self.time_to_record = self. 
#

    def UpdateTime(self):
        #print('Nuevo valor del spin :',self.PlataformDistance.value())
        self.time_to_record = int( self.PlataformDistance.value()/SPEED_40 )
        print('Upadate  parameters ----')
        print('Distance :', int(self.PlataformDistance.value()) )
        print('Time :', self.time_to_record )
        

    def UpdateSpeed(self):
        print('update speed to : ', int( self.PlataformSpeed.value() ))

    def AppExit(self):
        # print all file recorded 

      #  for nameFiles in self.AppSar.fileToProccess:
      #      print(nameFiles)
        self.close()

    def recordConfiguration(self, condition):

        self.PlataformSpeed.setEnabled(condition)
        self.PlataformDistance.setEnabled(condition)
        self.NameFile.setEnabled(condition)
        self.spinBoxNumber.setEnabled(condition)
        self.ButtonRadarOnOff.setEnabled(condition)
        #self.ButtonRadarOnOff.setEnabled(condition)

    def NextRecord(self):
        # shutdown button net
        self.ButtonNext.setEnabled(False)
        #self.pushButtonNext.setEnabled(False)
        # ----- record files to proccess -------
        if self.counter < self.spinBoxNumber.value() :
            self.counter += 1
            #self.TextStatus.setText('Recording ... ')
            print('recording [', self.counter,'/',self.spinBoxNumber.value(),']' )
            self.RecordStatus.setText('recording')
            # Init strem to record file 
            p = pyaudio.PyAudio()
            stream = p.open(format= self.format, # FORMAT,
                            channels= self.channels, # CHANNELS,
                            rate= self.rate, # RATE,
                            input=True,
                            frames_per_buffer= self.frame_per_buffer) # CHUNK)
            frames = []
            max_value = int(self.rate / self.frame_per_buffer * self.time_to_record)
            #print('Init Recording : ', int(self.rate / self.frame_per_buffer * self.time_to_record))  # just for testing 
            for i in range(0, max_value ):
                #print('i :' , i )  # just for testing
                data = stream.read(self.frame_per_buffer)
                frames.append(data)
                self.statusBar.setValue(int((i+1)*100/max_value ))
            #print(int(RATE / CHUNK * RECORD_SECONDS))
            #print("* done recording")
            # --- close recording stream ----
            stream.stop_stream()
            stream.close()
            p.terminate()
            # --- save file -----,
            saveFile(frames,self.NameFile.text()+'/'+self.NameFile.text()+str(self.counter)+'.wav',p.get_sample_size(self.format))
          
            print('Recorded ',self.counter,' of ', self.spinBoxNumber.value() )  # for debug 

            #self.TextStatus.setText('Recorded '+str(self.counter+1)+' de '+str(self.spinBoxNumber.value()) )
            #self.pushButtonNext.setEnabled(True)
             #  actualizar barra status 
            #self.statusBar.setValue( int ( (self.counter+1 )*100/self.spinBoxNumber.value()  ))
            

            #if self.counter == (self.spinBoxNumber.value()) :
            #    print('recorded')
                ##self.NextRecord()
            #else:
            #    pass
            #self.AppSar.filesToProccess.append(os.path.dirname(__file__)+'/'+ self.NameFile.text()+'/'+self.NameFile.text()+str(self.counter)+'.wav')
            self.RecordStatus.setText('recorded')
            # activar boton back  y 
            #if self.ButtonRunAuto.isChecked():
                #self.delayTime(5)    # 5 segundos to going back
                #self.AppBackToInit()
                
            if self.ButtonRunManual.isChecked():
                self.ButtonBackToInit.setEnabled(True)
            else:
                pass
            
        else:
            self.counter = 0 
            self.ButtonStart.setEnabled(False)
            self.groupBoxPlataformOptions.setEnabled(True)
            self.groupBoxOptions.setEnabled(True)
            self.ButtonRadarOnOff.setEnabled(True)
            #self.pushButtonNext.setEnabled(False)
            #self.TextStatus.setText('waiting to record')

    def AppRecord(self):

        self.counter = 0
        self.radar.distanceAcimut =  self.PlataformDistance.value()   ### set distance in acimut
        self.recordConfiguration(False)
        #  cantidad de segundos a grabar 
        #self.time_to_record =  self.TimeValue.value()
        self.ButtonStart.setEnabled(False)
        self.ButtonStop.setEnabled(True)
        self.ButtonBackToInit.setEnabled(False)
        # make directory
        try:
            os.makedirs(self.NameFile.text())
        except OSError as e:
            if os.path.exists(self.NameFile.text()):
                deleteFiles(self.NameFile.text())
                print('Directory ["'+ self.NameFile.text() +'"] already exits')
        
        # save first file to proccess
        print('Directorio : ', os.path.dirname(__file__))
        # Set label of path files
        # self.AppSar.label_NameDirectory.setText(os.path.dirname(__file__)+'/'+self.NameFile.text())
        # set folder to proccess
        self.AppSar.filesToProccess = []
        self.stepsTorecord()
        # iniciar radar : turn on the radar !!then 
        # wait 1 secord to stability and then start to move the plataform
        # -- run the plataform()  run up  
        # save first file to proccess
        #self.RecordStatus.setText('recording')
        # inicio el movimiento del radar      
    
    def delayTime(self,time_to_delay):
        for ii in range(time_to_delay):
            time.sleep(1)
        #print('Init ...')

    def stepsTorecord(self):
        
        # delay time
        if self.delayValue.value() !=0 :
            self.delayTime(self.delayValue.value())
        else:
            pass

        if self.ButtonModeScan.isChecked():     # the radar is 
            print('mode : scan ')
            self.pltfrm.turnRadarOn()           # turn on the radar .
            print('turn the radar on')
            self.pltfrm.plataformMoveUp()       # move up the plataform .
            print('move up the plataform')
            self.NextRecord()                   # start recording .
            print('start recording ')
            self.pltfrm.plataformStop()         # stop the plataform . 
            print('stop the plataform')
            self.pltfrm.turnRadarOff()          # turn the radar off .
            print('turn the radar off')
            if self.ButtonRunAuto.isChecked():
                self.delayTime(5)               # 5 seg delay time
                self.AppBackToInit()            # going back to init automatic
            else:
                pass

        elif  self.ButtonModeLisen.isChecked(): # the radar is not moving
            print('mode : lisen ')
            self.pltfrm.turnRadarOn()           # turn on the radar 
            self.NextRecord()                   # start recording
            self.pltfrm.turnRadarOff()          # turn the radar off
            self.recordConfiguration(True)
            self.statusBar.setValue(0)


        else:
            print('error - no mode selected')
            
#        self.pltfrm.turnRadarOn()           # turn on the radar .
#        print('turn the radar on')
#        self.pltfrm.plataformMoveUp()       # move up the plataform .
#        print('move up the plataform')
#        self.NextRecord()                   # start recording .
#        print('start recording ')
#        self.pltfrm.plataformStop()         # stop the plataform . 
#        print('stop the plataform')
#        self.pltfrm.turnRadarOff()          # turn the radar off .
#        print('turn the radar off')

    def AppStop(self):
        print('stop to emergency')  ## only if you need it
        self.pltfrm.plataformStop()

    def AppBackToInit(self):
        self.pltfrm.plataformMoveDown() 
        max_value = self.time_to_record
        print('going back to the start')
        self.RecordStatus.setText('going back to the start')
        for ii in range(self.time_to_record,-1,-1):
            self.statusBar.setValue(int(ii*100/max_value))
            time.sleep(1)
        self.pltfrm.plataformStop()    
        self.ButtonBackToInit.setEnabled(False)  # turn off the buttonStop.
        self.RecordStatus.setText('Stopped to the start')

        if self.counter < (self.spinBoxNumber.value()) :
            self.ButtonNext.setEnabled(True)
            print(' next set up ')
            self.RecordStatus.setText('wait for next record ...')
        else:
            self.ButtonStart.setEnabled(True)
            self.ButtonStop.setEnabled(False)
            self.recordConfiguration(True)


    def AppRadarOnOff(self):
        if self.ButtonRadarOnOff.isChecked() :
            print('tun the radar on')
            self.pltfrm.turnRadarOn()
        else:
            print('turn the radar off')
            self.pltfrm.turnRadarOff()
#
# ---  main ---- 
if __name__ == "__main__":
    app = QApplication(sys.argv)
    recApp = AppRecord()
    recApp.show()
    app.exec_()
# ----

