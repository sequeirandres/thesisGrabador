from PyQt5.QtWidgets import*
from PyQt5.uic import loadUi
from PyQt5.QtGui import QIcon
class Plataform(QMainWindow):
    def __init__(self):
        print('loading ... ')
        QMainWindow.__init__(self)
        loadUi("plataforma.ui",self)
        self.setWindowTitle("Control de Plataforma wifi esp8266 NodeMcu")
        self.setWindowIcon(QIcon('wifi.ico')) 

        self.labelSpeed.setText('30%')

      # Buttons control, MoveUp, MoveDown and Stop 
        self.ButtonExit.clicked.connect( self.plataformExit )
        self.ButtonMoveUp.clicked.connect( self.plataformMoveUp)
        self.ButtonMoveDown.clicked.connect(self.plataformMoveDown)
        self.ButtonStop.clicked.connect(self.plataformStop)
        self.ButtonRadarOn.clicked.connect(self.plataformRadar)
        self.SliderSpeed.valueChanged.connect(self.plataformSpeed)
        self.timeInit = 0
        self.timeEnd = 0
       # set time LCD 
        self.lcdTime.display(00.00)

    def plataformMoveUp(self):
        print(' Runnig motor Up ')
        self.labelControl.setText('Moving Up')
        print('http:/'+IP_ESP8266wifi+'/'+MOTOR_UP)
        self.timeInit = time.time()  # init time
        r= requests.get('http://'+IP_ESP8266wifi+'/'+MOTOR_UP)
    
    def plataformMoveDown(self):
        print('Running motor down')
        self.labelControl.setText('Moving Down')
        print('http:/'+IP_ESP8266wifi+'/'+MOTOR_DOWN)
        self.timeInit = time.time()  # set Init time 
        r= requests.get('http://'+IP_ESP8266wifi+'/'+MOTOR_DOWN)

    def plataformStop(self):
        print('Plataform just stopped ')
        self.labelControl.setText('Stoped')
        print('http:/'+IP_ESP8266wifi+'/'+MOTOR_STOP)
        r= requests.get('http://'+IP_ESP8266wifi+'/'+MOTOR_STOP)
        self.timeEnd = time.time()  # set end time
        # updata time to LCD :
        self.lcdTime.display(np.round( self.timeEnd-self.timeInit  ,2))
        

    def plataformRadar(self):
        if self.ButtonRadarOn.isChecked():
            print('radar on ')
            self.labelRadar.setText('radar on')
            print('http:/'+IP_ESP8266wifi+'/'+ RADAR_ON)
            r= requests.get('http://'+IP_ESP8266wifi+'/'+RADAR_ON)
        else :
            print('radar off')
            self.labelRadar.setText('radar off')
            print('http:/'+IP_ESP8266wifi+'/'+ RADAR_OFF)
            r= requests.get('http://'+IP_ESP8266wifi+'/'+RADAR_OFF)

    def turnRadarOn(self):
        r= requests.get('http://'+IP_ESP8266wifi+'/'+RADAR_ON)

    def turnRadarOff(self):
        r= requests.get('http://'+IP_ESP8266wifi+'/'+RADAR_OFF)

    def plataformSpeed(self):
        sliderValue = self.SliderSpeed.value()
        print('value speed :' , sliderValue )
        self.labelSpeed.setText(str(sliderValue)+'%')
        if sliderValue < 30 :
            print('too slow, the plataform will be stopped ')
            self.plataformStop()
        else:
            speedMotorUpdata = 'http://'+IP_ESP8266wifi+'/'+MOTOR_SPEED+str(int(self.SliderSpeed.value()/10)*10 ) 
            print('Velocidad :', speedMotorUpdata)
            r=requests.get(speedMotorUpdata)

    def plataformExit(self):
        print('Exit!')
        self.close()