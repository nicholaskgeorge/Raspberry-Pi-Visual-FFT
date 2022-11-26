import threading
import serial

class LED():
    def __init__(self, bar_data_length=15, middle_mode = 0):
        self.bar_data_length=bar_data_length
        self.column_height = [0]*self.bar_data_length
        self.column_color = [2]*self.bar_data_length
        self.middle_mode = middle_mode;
        self.ser = serial.Serial('/dev/ttyACM0', 115200);
    def send(self):
        message = [self.middle_mode]
        for i in range(self.bar_data_length):
            compressed = self.column_height[i]|(self.column_color[i]<<4)
            message.append(compressed)
        self.ser.write(message)