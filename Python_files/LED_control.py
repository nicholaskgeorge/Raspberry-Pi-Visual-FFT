import threading
import serial

class LED():
    def __init__(self):
        self.bar_data_length=32
        self.column_height = [0]*self.bar_data_length
        self.column_color = [2]*self.bar_data_length
        self.ser = serial.Serial('/dev/ttyACM0', 115200);
    def send(self):
        message = [0x23]
        for i in range(self.bar_data_length):
            message.append(self.column_height[i])
            message.append(self.column_color[i])
        message.append(0xFF)
        print(message)
        self.ser.write(message)