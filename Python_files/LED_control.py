import threading
import serial

class LED():
    def __init__(self, bar_data_length=15):
        self.bar_data_length=bar_data_length
        self.column_height = [0]*self.bar_data_length
        self.column_color = [2]*self.bar_data_length
        self.ser = serial.Serial('/dev/ttyACM0', 115200);
    def send(self):
        message = [0x23]
        for i in range(self.bar_data_length):
            compressed = self.column_height[i]|(self.column_color[i]<<4)
            message.append(compressed)
            #print("{0:b}".format(compressed))
        message.append(0xFF)
        print(message)
        self.ser.write(message)