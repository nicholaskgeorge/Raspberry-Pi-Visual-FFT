import threading
import serial

class LED():
    def __init__(self):
        self.bar_data_length=3
        self.column_height = [0]*self.bar_data_length
        self.column_color = [1]*self.bar_data_length
        self.ser = serial.Serial('/dev/ttyACM0', 115200);
    def send(self):
        message = [0x23] + self.column_height + self.column_color + [0xFF]
        self.ser.write([0x23,15,1,7,1,0xFF])