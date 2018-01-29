# -*- coding: utf-8 -*-

# 라즈베리파이 GPIO 패키지 
import RPi.GPIO as GPIO
from time import sleep

LED = 4

HIGH = 1
LOW = 0

ON = 1
OFF = 0

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED, GPIO.OUT)

def setLed(on):
    if on == ON:
        GPIO.output(LED, HIGH)
    else:
        GPIO.output(LED, LOW)

setLed(OFF)
