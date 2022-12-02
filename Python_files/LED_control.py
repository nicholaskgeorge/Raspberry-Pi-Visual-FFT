from threading import Thread
import serial
from time import sleep

class LED(Thread):
    def __init__(self, bar_data_length=15, middle_mode = 1):
        super(LED, self).__init__()
        self.bar_data_length=bar_data_length
        self.column_height = [0]*self.bar_data_length
        self.column_color = [2]*self.bar_data_length
        self.middle_mode = middle_mode;
        self.sending_delay = 0.1
        self.ser = serial.Serial('/dev/ttyACM0', 115200);
    def send(self):
        message = [self.middle_mode]
        for i in range(self.bar_data_length):
            compressed = (self.column_height[i])|(self.column_color[i]<<4)
            message.append(compressed)
        self.ser.write(message)
    def run(self):
        while True:
            self.send()
            sleep(self.sending_delay)
