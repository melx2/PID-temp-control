#tempControl.py
# using Arduino: ThermoDev1
import os
import sys
import time
import serial
import numpy as np
import matplotlib
from QLed import QLed 
from PyQt5 import QtCore
from simple_pid import PID
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from sys import float_repr_style
from engineering_notation import EngNumber 

# Load the QT resources.
dirname = os.path.realpath(os.path.dirname(__file__))
filePath = os.path.join(dirname, "TempCtlGUI.ui")
Ui_MainWindow, QMainWindow = loadUiType(filePath)

# for windows:
ser = serial.Serial(port='COM4', baudrate=9600, timeout=1)
#for linux:
# ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
ser.flush()

class TempControl(QMainWindow, Ui_MainWindow):

    def __init__(self,*args, **kwargs) :
        super(TempControl, self).__init__()
        self.setupUi(self)          # set up the GUI window
        # PID initial
        self.setSetPoint()
        self.pid = PID(1, 0.1, 0.05, setpoint= self.setPoint)
        self.tempControls()     # set up the temperature control panel buttons & display

        # Setup a timer to trigger the redraw by calling update_plot.
        self.timer = QtCore.QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.update_temp)
        self.ledPowerOn.value = False # make sure power led is off

    def start(self):                # start the timer to refresh display
        self.timer.start()

    def update_temp(self):          # update 
        self.pid.setpoint = self.setPoint # update the set point with any change in value
        line = ser.readline().decode('utf-8').rstrip() # read in temperature
        if line == '': line = 0 # catch a null string which causes an error
        actualTemp = float(line) # convert the string to a float number
        # fix the lcd display to always show 2 decimal places
        self.lcdActual.display('{:.1f}'.format(actualTemp))
        output = self.pid(actualTemp)
        delta = 1-actualTemp/self.setPoint
        if delta >= 0 :
            self.ledPowerOn.value = True
            pwmOnTime = delta *1000
        else: 
            pwmOnTime = 1  
            self.ledPowerOn.value = False  
        pwmOn = bytes(str(pwmOnTime) + '\n', 'utf-8') # data convert PWM on time (uS)
        ser.write(pwmOn) # send out the PWM power to meet the set point temperature
        

    # temperature controls and functions
    def tempControls(self):
        self.spinChSetPoint.valueChanged.connect(self.setSetPoint) 
        self.lcdActual.setDigitCount(5)  
    def setSetPoint(self):
        self.setPoint = self.spinChSetPoint.value()
        setValue = float(self.setPoint)
        self.lcdSetPoint.display('{:.1f}'.format(setValue))
        

app = QApplication(sys.argv)
main = TempControl()
main.start()
main.show()
app.exec_()
