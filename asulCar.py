#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from time import sleep
import led
from ottosound import OttoBuzzer as OB
from tcp import tcpServer as server
from motor import l298


pinBuzzer = 23
ottoTone = OB.OTTOSound(pinBuzzer)
ottoTone.sing('S_connection')


def statusChanged(stat, parm = None):
    if stat == server.CONNECTED:
        print ('success {}:{}'.format(parm[0], parm[1]));
        led.setLed(led.ON)
        ottoTone.sing('S_mode3')
    elif stat == server.DISCONNECTED:
        led.setLed(led.OFF)
        ottoTone.sing('S_disconnection')


led.setLed(led.OFF)
ser = server.tcpServer(callbackFunc = statusChanged)
motor = l298.l298n()

  
while True:
    sleep(0.01)
    pack = ser.pull()
    if pack is None:
        continue
    print(pack)
    pack.replace('\n', '')
    pack.replace('\r', '')        
    p = pack.split(',')        
    if len(p) >= 2:
        cmd = p[0].strip()        
        if cmd == 'joy':
            xaxis = int(p[1].strip())
            yaxis = int(p[2].strip())
            motor.MotorMove(xaxis,yaxis, 100)
        else:
            stat = p[1].strip()
            direction = cmd
            if stat == 'd': #push
                if direction == 'up':
                    motor.MotorGo()

                elif direction == 'dn':
                    motor.MotorBack()

                elif direction == 'le':
                    motor.MotorLeft()

                elif direction == 'ri':
                    motor.MotorRight()
                elif direction == 'a':
                    ottoTone.sing('S_buttonPushed')
            else: #pull
                motor.MotorStop()
ser.close()
