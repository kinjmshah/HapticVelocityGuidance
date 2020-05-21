import sys
import time
import numpy as np
import csv
from Adafruit_BNO055 import BNO055
import RPi.GPIO as GPIO
import guidance as gS

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)

# define pins - MAY CHANGE
topLEDpin = 17 #11
botLEDpin = 4 #7
topMotorPin = 24 #18
botMotorPin = 23 #16

# setup gpio pins as output pins
GPIO.setup(topLEDpin, GPIO.OUT)
GPIO.setup(botLEDpin, GPIO.OUT)
GPIO.setup(topMotorPin, GPIO.OUT)
GPIO.setup(botMotorPin, GPIO.OUT)

# initialize pwm
topLED = GPIO.PWM(topLEDpin,50)
botLED = GPIO.PWM(botLEDpin,50)
topMotor = GPIO.PWM(topMotorPin,150)
botMotor = GPIO.PWM(botMotorPin,150)

topLED.start(0)
botLED.start(0)
topMotor.start(0)
botMotor.start(0)

#input arguments
    #first command line argument should be the subject number
    #second command line argument should be the mode if mode is needed
subjectNum = sys.argv[1]
targetVel = sys.argv[2]
# mode = 0 - fixed target
# mode = 1 - non Linear velocity profile
mode = sys.argv[3]

# Store Data Files
filename = str(subjectNum)+'Mode'+str(mode)
timestr = time.strftime(filename+"TS%H%M%S.csv")

# run the algorithm
gS.callGuidanceSystem(topLED, botLED, topMotor, botMotor, 0,timestr,targetVel,mode)
