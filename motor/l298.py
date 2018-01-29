#! /usr/bin/env python
# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time

# 모터 상태
STOP  = 0
FORWARD  = 1
BACKWARD = 2
SOFT_STOP = 3

STAT_STOP = 0
STAT_GO = 1
STAT_BACK = 2
STAT_LEFT = 3
STAT_RIGHT = 4

# 모터 채널
CH1 = 0
CH2 = 1

# PIN 입출력 설정
OUTPUT = 1
INPUT = 0

# PIN 설정
HIGH = 1
LOW = 0

# 실제 핀 정의
#PWM PIN
ENA = 26  #37 pin
ENB = 0   #27 pin

#GPIO PIN
IN1 = 19  #37 pin
IN2 = 13  #35 pin
IN3 = 6   #31 pin
IN4 = 5   #29 pin

#refer to arduino source code
def map(x, in_min, in_max, out_min, out_max):    
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

class l298n():
    def __init__(self, ena = ENA, in1 = IN1, in2 = IN2, enb = ENB, in3 = IN3, in4 = IN4):                
        # GPIO 모드 설정 
        GPIO.setmode(GPIO.BCM)

        self.ena = ena
        self.enb = enb
        self.in1 = in1
        self.in2 = in2
        self.in3 = in3
        self.in4 = in4
               
        self.curStat = STAT_STOP 
        
        #모터 핀 설정        
        #핀 설정후 PWM 핸들 얻어옴 
        self.pwmA = self.setPinConfig(self.ena, self.in1, self.in2)
        self.pwmB = self.setPinConfig(self.enb, self.in3, self.in4)

    # 핀 설정 함수
    def setPinConfig(self, EN, INA, INB):                
        GPIO.setup(EN, GPIO.OUT)
        GPIO.setup(INA, GPIO.OUT)
        GPIO.setup(INB, GPIO.OUT)
        # 100khz 로 PWM 동작 시킴 
        pwm = GPIO.PWM(EN, 100) 
        # 우선 PWM 멈춤.   
        pwm.start(0) 
        return pwm

    # 모터 제어 함수
    def setMotorContorl(self, pwm, INA, INB, speed, stat):

        #모터 속도 제어 PWM
        if speed > 100 or speed < 0:
            return
        pwm.ChangeDutyCycle(speed)  
        
        if stat == FORWARD:
            GPIO.output(INA, HIGH)
            GPIO.output(INB, LOW)
            
        #뒤로
        elif stat == BACKWARD:
            GPIO.output(INA, LOW)
            GPIO.output(INB, HIGH)
            
        #정지
        elif stat == STOP:
            GPIO.output(INA, HIGH)
            GPIO.output(INB, HIGH)
        

            
    # 모터 제어함수 간단하게 사용하기 위해 한번더 래핑(감쌈)
    def setMotor(self, ch, speed, stat):
        if ch == CH1:
            #pwmA는 핀 설정 후 pwm 핸들을 리턴 받은 값이다.
            self.setMotorContorl(self.pwmA, self.in1, self.in2, speed, stat)
        else:
            #pwmB는 핀 설정 후 pwm 핸들을 리턴 받은 값이다.
            self.setMotorContorl(self.pwmB, self.in3, self.in4, speed, stat)

    def MotorGo(self, speed = 80):
        if self.curStat == STAT_GO:
            return
        self.curStat = STAT_GO
        
        self.setMotor(CH1, speed, FORWARD)
        self.setMotor(CH2, speed, FORWARD)        
      
    def MotorLeft(self, speed = 80):
        if self.curStat == STAT_LEFT:
            return
        self.curStat = STAT_LEFT
        
        self.setMotor(CH1, speed, BACKWARD)
        self.setMotor(CH2, speed, FORWARD)

    def MotorRight(self, speed = 80):
        if self.curStat == STAT_RIGHT:
            return
        self.curStat = STAT_RIGHT
        
        self.setMotor(CH1, speed, FORWARD)
        self.setMotor(CH2, speed, BACKWARD)

    def MotorBack(self, speed = 80):    
        if self.curStat == STAT_BACK:
            return
        self.curStat = STAT_BACK
            
        self.setMotor(CH1, speed, BACKWARD)
        self.setMotor(CH2, speed, BACKWARD)

    def MotorStop(self, fastStop = True):    
        if self.curStat == STAT_STOP:
            return
        self.curStat = STAT_STOP
        if fastStop: 
            self.setMotor(CH1, 0, STOP)
            self.setMotor(CH2, 0, STOP)
        else:
            self.setMotor(CH1, 0, SOFT_STOP)
            self.setMotor(CH2, 0, SOFT_STOP)


    '''           
    http://www.impulseadventure.com/elec/robot-differential-steering.html
    '''
    def MotorMove(self, xAxis, yAxis, speed):
        #nMotMixL  # Motor (left)  mixed output           (-128..+127)
        #nMotMixR  # Motor (right) mixed output           (-128..+127)
        # TEMP VARIABLES
        #nMotPremixL # Motor (left)  premixed output        (-128..+127)
        #nMotPremixR # Motor (right) premixed output        (-128..+127)
        #nPivSpeed  # Pivot Speed                          (-128..+127)
        #fPivScale   # Balance scale b/w drive and pivot    (   0..1   )
        fPivYLimit = 32.0
        
        print(xAxis, end='')
        print(" ", end='')
        print(yAxis)
                    
        nJoyX = xAxis
        nJoyY = yAxis

        # Calculate Drive Turn output due to Joystick X input
        if (nJoyY >= 0):
            # Forward
            if (nJoyX>=0):
                nMotPremixL = 127.0 
            else: 
                nMotPremixL = (127.0 + nJoyX)
            if (nJoyX>=0):
                nMotPremixR = (127.0 - nJoyX) 
            else: 
                nMotPremixR = 127.0
        else:
            # Reverse
            if (nJoyX>=0):
                nMotPremixL = (127.0 - nJoyX)
            else:
                nMotPremixL = 127.0
            if (nJoyX>=0):
                nMotPremixR = 127.0
            else: 
                nMotPremixR = (127.0 + nJoyX)
    
        # Scale Drive output due to Joystick Y input (throttle)
        nMotPremixL = nMotPremixL * nJoyY/128.0
        nMotPremixR = nMotPremixR * nJoyY/128.0
  
        # Now calculate pivot amount
        # - Strength of pivot (nPivSpeed) based on Joystick X input
        # - Blending of pivot vs drive (fPivScale) based on Joystick Y input
        nPivSpeed = nJoyX
        if (abs(nJoyY)>fPivYLimit):
            fPivScale = 0.0
        else: 
            fPivScale = (1.0 - abs(nJoyY)/fPivYLimit)
  
        # Calculate final mix of Drive and Pivot
        nMotMixL = (1.0-fPivScale)*nMotPremixL + fPivScale*( nPivSpeed)
        nMotMixR = (1.0-fPivScale)*nMotPremixR + fPivScale*(-nPivSpeed)

        

        if nMotMixL < 0:
            print(nMotMixL)
            print(map(abs(nMotMixL), 0, 127, 0, speed))
            self.setMotor(CH1, map(abs(nMotMixL), 0, 127, 0, speed), BACKWARD)            
        else:
            print(nMotMixL)
            print(map(abs(nMotMixL), 0, 127, 0, speed))
            self.setMotor(CH1, map(abs(nMotMixL), 0, 127, 0, speed), FORWARD)
            
        if nMotMixR < 0:
            print(nMotMixR)
            print(map(abs(nMotMixR), 0, 127, 0, speed))
            self.setMotor(CH2, map(abs(nMotMixR), 0, 127, 0, speed), BACKWARD)            
        else:
            print(nMotMixR)
            print(map(abs(nMotMixR), 0, 127, 0, speed))
            self.setMotor(CH2, map(abs(nMotMixR), 0, 127, 0, speed), FORWARD)
            
    

 

if __name__ == '__main__':
    l298 = l298n()
    l298.MotorMove(-0, 127, 100)
    
    time.sleep(2)
    l298.MotorMove(-0, -127, 100)
    time.sleep(1)
    l298.MotorStop(False)