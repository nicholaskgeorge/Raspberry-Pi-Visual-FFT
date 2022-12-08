from threading import Thread
import serial
from time import sleep

"""
    This class exists to deal with all of the communicatiom between the PI and the Arduino to display
    each of the frequency bars. It is designed to run a thread to constantly send data to the raspberry pi
    while each bar and color can be controlled through different arrays
""" 
class LED(Thread):
    def __init__(self, bar_data_length=15, middle_mode = 1):
        #run all things related the Threading parent class
        super(LED, self).__init__()
        #Number of data points sent
        self.bar_data_length=bar_data_length
        #array describing the bar Height
        self.column_height = [0]*self.bar_data_length
        #array describing the color of each bar. 0 = red, 1 = white, 2 = blue, 3 = green
        self.column_color = [0]*self.bar_data_length
        #used to turn on or off middle mode where the frequencies spread out from the center of the LED screen
        self.middle_mode = middle_mode
        #delay of sending the data
        self.sending_delay = 0.1
        #connect to serial port
        self.ser = serial.Serial('/dev/ttyACM0', 115200);
    
    #function to send the data to the arduino
    def send(self):
        #make the message packet. The first data point is whether to use middle mode or not
        message = [self.middle_mode]
        #Pack the message with the height and color of each column
        for i in range(self.bar_data_length):
            """
            The code here was used in order to shorten how many numbers we had to send. There are 32 bars with 32 different colors. Thats
            is 64 different numbers to send. In order to compress that into 32 number bit shifting was used. Each serial transimssion is 
            1 byte or 8 bits. The first 4 bits are the color of the bar and the last 4 bytes are the height. Bit shifting was used to acomplish
            this 
            """
            compressed = min(self.column_height[i],15)|(self.column_color[i]<<4)
            message.append(compressed)
        self.ser.write(message)
    
    #function which runs in the thread sending the data over and over again.
    def run(self):
        while True:
            self.send()
            sleep(self.sending_delay)
