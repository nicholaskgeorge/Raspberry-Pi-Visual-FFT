import serial
from time import sleep
import numpy as np
from LED_control import LED
import RPi.GPIO as GPIO
from threading import Thread

class FFT_Screen(Thread):
    def __init__(self, middle=0):
        super(FFT_Screen, self).__init__()
        self.middle = middle
        self.FFT_size = 64
        self.ser = serial.Serial('/dev/ttyUSB0', 115200);
        self.screen = LED(bar_data_length=32, middle_mode=self.middle)
        self.screen.start()
        self.display_mode = 0 #0 = 3 max mode 1 = 1 max mode
        self.filtering = True
        self.num_maxes = 3
        
        GPIO.cleanup()
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    def run(self):
        while True:
            #button Stuff
            if not GPIO.input(26):
                print("pressed")
                self.display_mode = 1-self.display_mode
                sleep(0.5)
            if not GPIO.input(19):
                self.screen.middle_mode = 1-self.screen.middle_mode
                sleep(0.5)
            #FFT stuff
            values = self.ser.readline().decode('ascii')
            values = values.split(",")[1:-1]
            values = [int(i) for i in values if i != ""]
            yf = np.fft.fft(values)
            N = len(values)
            if(N == self.FFT_size):
                #division by 2 due to FFT shift
                yff = (1.0/N * np.abs(yf[:N//2]))
                if self.filtering == True:
                    yff = np.array([i if i>2 else 0 for i in list(yff)])
                if self.display_mode == 1:
                    print("hey")
                    index = yff[1:].argmax()
                    yff = list(yff)
                    for i in range(self.FFT_size//2):
                        if i==index+1:
                            self.screen.column_color[i] = 2
                        else:
                            self.screen.column_color[i] = 0
                        self.screen.column_height[i] = int(yff[i])
                elif self.display_mode == 0:
                    for i in range(self.FFT_size//2):
                        self.screen.column_height[i] = int(yff[i])
                        self.screen.column_color[i] = 0
                    find_max = yff[1:]
                    for i in range(self.num_maxes):
                        index = find_max.argmax()
                        self.screen.column_color[index+1] = i+1
                        find_max[index] = -1
                else:
                    quit()


if __name__ == "__main__":
    project = FFT_Screen()
    project.start()