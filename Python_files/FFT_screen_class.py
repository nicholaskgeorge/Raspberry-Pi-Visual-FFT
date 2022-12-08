import serial
from time import sleep
import numpy as np
from LED_control import LED
import RPi.GPIO as GPIO
from threading import Thread

#class to manage all of the project
class FFT_Screen(Thread):
    def __init__(self, middle=0):
        #run needed threading components
        super(FFT_Screen, self).__init__()
        #control whether middle mode on or not
        self.middle = middle
        #number of FFT points coming in 
        self.FFT_size = 64
        #setting up the serial port to be used
        self.ser = serial.Serial('/dev/ttyUSB0', 115200);
        #make class to control the LED display
        self.screen = LED(bar_data_length=32, middle_mode=self.middle)
        #start sending data to the arduino
        self.screen.start()
        #to control the display mode
        self.display_mode = 0 #0 = 3 max mode 1 = 1 max mode
        #if true all diaplyed bars have the be greater than 2
        self.filtering = True
        #number of maximums to highlight
        self.num_maxes = 3
        #gpio related stuff
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
            #decode the Data coming in from the Pico
            values = self.ser.readline().decode('ascii')
            #remove the first element from the data it does not contai anything
            values = values.split(",")[1:-1]
            #remove blanks form the data
            values = [int(i) for i in values if i != ""]
            #run the FFT
            yf = np.fft.fft(values)
            #only run if 64 data points sent
            N = len(values)
            if(N == self.FFT_size):
                #division by 2 due to FFT shift. Only use half of the values since only half are positive frequencies
                yff = (1.0/N * np.abs(yf[:N//2]))
                #filter off anything under 2 in height
                if self.filtering == True:
                    yff = np.array([i if i>2 else 0 for i in list(yff)])
                #Single maximum display mode
                if self.display_mode == 1:
                    #get the position of the highest value frequency
                    index = yff[1:].argmax()
                    #convert back to a list
                    yff = list(yff)
                    #make the maximum frequency bar blue, make the rest red
                    for i in range(self.FFT_size//2):
                        if i==index+1:
                            self.screen.column_color[i] = 2
                        else:
                            self.screen.column_color[i] = 0
                        self.screen.column_height[i] = int(yff[i])
                #3 Maximum mode where the highest 3 frequencies are highlighted
                elif self.display_mode == 0:
                    #make all of the bars red
                    for i in range(self.FFT_size//2):
                        self.screen.column_height[i] = int(yff[i])
                        self.screen.column_color[i] = 0
                    find_max = yff[1:]
                    #make the 3 highest red blue and green (high to low)
                    for i in range(self.num_maxes):
                        index = find_max.argmax()
                        self.screen.column_color[index+1] = i+1
                        find_max[index] = -1
                #quit if any other mode is given
                else:
                    quit()


if __name__ == "__main__":
    #run the project
    project = FFT_Screen()
    project.start()