# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time
import threading

playSounds = [
            'S_connection',
            'S_disconnection',
            'S_buttonPushed',
            'S_mode1',
            'S_mode2',
            'S_mode3',
            'S_surprise',
            'S_OhOoh',
            'S_OhOoh2',
            'S_cuddly',
            'S_sleeping',
            'S_happy',
            'S_superHappy',
            'S_happy_short',
            'S_sad',
            'S_confused',
            'S_fart1',
            'S_fart2',
            'S_fart3']

note_C0  = 16.35    #C0
note_Db0 = 17.32    #C#0/Db0
note_D0  = 18.35    #D0
note_Eb0 = 19.45    #D#0/Eb0
note_E0  = 20.6     #E0
note_F0  = 21.83    #F0
note_Gb0 = 23.12    #F#0/Gb0
note_G0  = 24.5     #G0
note_Ab0 = 25.96    #G#0/Ab0
note_A0  = 27.5     #A0
note_Bb0 = 29.14    #A#0/Bb0
note_B0  = 30.87    #B0
note_C1  = 32.7     #C1
note_Db1 = 34.65    #C#1/Db1
note_D1  = 36.71    #D1
note_Eb1 = 38.89    #D#1/Eb1
note_E1  = 41.2     #E1
note_F1  = 43.65    #F1
note_Gb1 = 46.25    #F#1/Gb1
note_G1  = 49       #G1
note_Ab1 = 51.91    #G#1/Ab1
note_A1  = 55       #A1
note_Bb1 = 58.27    #A#1/Bb1
note_B1  = 61.74    #B1
note_C2  = 65.41    #C2 (Middle C)
note_Db2 = 69.3     #C#2/Db2
note_D2  = 73.42    #D2
note_Eb2 = 77.78    #D#2/Eb2
note_E2  = 82.41    #E2
note_F2  = 87.31    #F2
note_Gb2 = 92.5     #F#2/Gb2
note_G2  = 98       #G2
note_Ab2 = 103.83   #G#2/Ab2
note_A2  = 110      #A2
note_Bb2 = 116.54   #A#2/Bb2
note_B2  = 123.47   #B2
note_C3  = 130.81   #C3
note_Db3 = 138.59   #C#3/Db3
note_D3  = 146.83   #D3
note_Eb3 = 155.56   #D#3/Eb3
note_E3  = 164.81   #E3
note_F3  = 174.61   #F3
note_Gb3 = 185      #F#3/Gb3
note_G3  = 196      #G3
note_Ab3 = 207.65   #G#3/Ab3
note_A3  = 220      #A3
note_Bb3 = 233.08   #A#3/Bb3
note_B3  = 246.94   #B3
note_C4  = 261.63   #C4
note_Db4 = 277.18   #C#4/Db4
note_D4  = 293.66   #D4
note_Eb4 = 311.13   #D#4/Eb4
note_E4  = 329.63   #E4
note_F4  = 349.23   #F4
note_Gb4 = 369.99   #F#4/Gb4
note_G4  = 392      #G4
note_Ab4 = 415.3    #G#4/Ab4
note_A4  = 440      #A4
note_Bb4 = 466.16   #A#4/Bb4
note_B4  = 493.88   #B4
note_C5  = 523.25   #C5
note_Db5 = 554.37   #C#5/Db5
note_D5  = 587.33   #D5
note_Eb5 = 622.25   #D#5/Eb5
note_E5  = 659.26   #E5
note_F5  = 698.46   #F5
note_Gb5 = 739.99   #F#5/Gb5
note_G5  = 783.99   #G5
note_Ab5 = 830.61   #G#5/Ab5
note_A5  = 880      #A5
note_Bb5 = 932.33   #A#5/Bb5
note_B5  = 987.77   #B5
note_C6  = 1046.5   #C6
note_Db6 = 1108.73  #C#6/Db6
note_D6  = 1174.66  #D6
note_Eb6 = 1244.51  #D#6/Eb6
note_E6  = 1318.51  #E6
note_F6  = 1396.91  #F6
note_Gb6 = 1479.98  #F#6/Gb6
note_G6  = 1567.98  #G6
note_Ab6 = 1661.22  #G#6/Ab6
note_A6  = 1760     #A6
note_Bb6 = 1864.66  #A#6/Bb6
note_B6  = 1975.53  #B6
note_C7  = 2093     #C7
note_Db7 = 2217.46  #C#7/Db7
note_D7  = 2349.32  #D7
note_Eb7 = 2489.02  #D#7/Eb7
note_E7  = 2637.02  #E7
note_F7  = 2793.83  #F7
note_Gb7 = 2959.96  #F#7/Gb7
note_G7  = 3135.96  #G7
note_Ab7 = 3322.44  #G#7/Ab7
note_A7  = 3520     #A7
note_Bb7 = 3729.31  #A#7/Bb7
note_B7  = 3951.07  #B7
note_C8  = 4186.01  #C8
note_Db8 = 4434.92  #C#8/Db8
note_D8  = 4698.64  #D8
note_Eb8 = 4978.03  #D#8/Eb8

# 파이썬 GPIO 모드
GPIO.setmode(GPIO.BCM)


def delay(ms):
    time.sleep(ms/1000.0)

class Tone(threading.Thread):
    def __init__(self, pin):
        threading.Thread.__init__(self)
        self.daemon = True

        #핀 설정
        GPIO.setup(pin, GPIO.OUT)

        self.pwm = GPIO.PWM(pin, 100)
        self.pwm.start(0)

        self.alive = True

        self.startTime = 0
        self.durationMs = 0

        self.isPlaying = False
        self._lock = threading.Lock()

    def stop(self):
        if self.pwm is not None:
            self.pwm.stop()
        self.alive = False
        self.join(2)

    def startTone(self, frequency, duration):
        with self._lock:
            self.pwm.ChangeFrequency(frequency)
            self.pwm.ChangeDutyCycle(50)
            self.startTime = time.time()
            self.durationMs = duration
            self.isPlaying = True

    def run(self):
        while self.alive:
            if ((time.time() - self.startTime)*1000) >= self.durationMs:
                with self._lock:
                    if self.isPlaying == True:
                        self.pwm.ChangeDutyCycle(0)
                        self.ToneStat = False
            time.sleep(0.01)


    def tone(self, frequency, duration):
        self.startTone(frequency, duration)

    def _tone (self, noteFrequency, noteDuration, silentDuration):
        if silentDuration == 0:
            silentDuration = 1
        self.tone(noteFrequency, noteDuration)
        delay(noteDuration)
        delay(silentDuration)

    def bendTones (self,  initFrequency, finalFrequency, prop, noteDuration, silentDuration):
        if silentDuration == 0:
            silentDuration = 1

        if initFrequency < finalFrequency:

            i = initFrequency
            while i < finalFrequency:
                self._tone(i, noteDuration, silentDuration)
                i = i * prop
        else:
            i = initFrequency
            while i > finalFrequency:
                self._tone(i, noteDuration, silentDuration)
                i = i / prop


    def sing(self, songName):
        if songName == 'S_connection':
            self._tone(note_E5,50,30)
            self._tone(note_E6,55,25)
            self._tone(note_A6,60,10)
        elif songName == 'S_disconnection':
            self._tone(note_E5,50,30)
            self._tone(note_A6,55,25)
            self._tone(note_E6,50,10)

        elif songName == 'S_buttonPushed':
            self.bendTones (note_E6, note_G6, 1.03, 20, 2)
            delay(30)
            self.bendTones (note_E6, note_D7, 1.04, 10, 2)

        elif songName == 'S_mode1':
            self.bendTones (note_E6, note_A6, 1.02, 30, 10) #1318.51 to 1760

        elif songName == 'S_mode2':
            self.bendTones (note_G6, note_D7, 1.03, 30, 10) #1567.98 to 2349.32

        elif songName == 'S_mode3':
            self._tone(note_E6,50,100) #D6
            self._tone(note_G6,50,80)  #E6
            self._tone(note_D7,300,0)  #G6

        elif songName == 'S_surprise':
            self.bendTones(800, 2150, 1.02, 10, 1)
            self.bendTones(2149, 800, 1.03, 7, 1)

        elif songName == 'S_OhOoh':
            self.bendTones(880, 2000, 1.04, 8, 3) #A5 = 880
            delay(200);
            i = 880
            while i < 2000:
                self._tone(note_B5,5,10);
                i=i*1.04

        elif songName == 'S_OhOoh2':
            self.bendTones(1880, 3000, 1.03, 8, 3);
            delay(200);
            i = 1880
            while i < 3000:
                self._tone(note_C6,10,10);
                i=i*1.03

        elif songName == 'S_cuddly':
            self.bendTones(700, 900, 1.03, 16, 4)
            self.bendTones(899, 650, 1.01, 18, 7)

        elif songName == 'S_sleeping':
            self.bendTones(100, 500, 1.04, 10, 10)
            delay(500);
            self.bendTones(400, 100, 1.04, 10, 1)

        elif songName == 'S_happy':
            self.bendTones(1500, 2500, 1.05, 20, 8)
            self.bendTones(2499, 1500, 1.05, 25, 8)

        elif songName == 'S_superHappy':
            self.bendTones(2000, 6000, 1.05, 8, 3)
            delay(50);
            self.bendTones(5999, 2000, 1.05, 13, 2)

        elif songName == 'S_happy_short':
            self.bendTones(1500, 2000, 1.05, 15, 8)
            delay(100);
            self.bendTones(1900, 2500, 1.05, 10, 8)

        elif songName == 'S_sad':
            self.bendTones(880, 669, 1.02, 20, 200)

        elif songName == 'S_confused':
            self.bendTones(1000, 1700, 1.03, 8, 2)
            self.bendTones(1699, 500, 1.04, 8, 3)
            self.bendTones(1000, 1700, 1.05, 9, 10)

        elif songName == 'S_fart1':
            self.bendTones(1600, 3000, 1.02, 2, 15)

        elif songName == 'S_fart2':
            self.bendTones(2000, 6000, 1.02, 2, 20)

        elif songName == 'S_fart3':
            self.bendTones(1600, 4000, 1.02, 2, 20)
            self.bendTones(4000, 3000, 1.02, 2, 20)

class OTTOSound(threading.Thread):
    def __init__(self, pin):
        threading.Thread.__init__(self)
        self.daemon = True
        self.alive = True
        print(pin)
        self.t = Tone(pin)
        self.t.start()
        self.isPlaying = False
        self.playList = []
        self.start()

    def run(self):
            while self.alive:
                if len(self.playList) > 0:
                    song = self.playList.pop(0)
                    print(song)
                    self.t.sing(song)
                time.sleep(0.1)

    def sing(self, songName):
        self.isPlaying = True
        self.playList.append(songName)
    



def setup():
    pinBuzzer = 23  # pin Number 7    
    ottoSound = OTTOSound(pinBuzzer)
    
    #playSounds만큼 루프
    for playSound in playSounds:
        print(playSound)
        #플레이
        ottoSound.sing(playSound)
        #지정 시간만큼 정지..
        delay(1000)

    t.stop()



if __name__ == '__main__':
    setup()
