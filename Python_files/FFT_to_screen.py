import serial
from time import sleep
import numpy as np
from LED_control import LED

ser = serial.Serial('/dev/ttyUSB0', 115200);
screen = LED(bar_data_length=32, middle_mode=0)
screen.start()
while True:
    values = ser.readline().decode('ascii')
    values = values.split(",")[1:-1]
    #print(values)
    values = [int(i) for i in values if i != ""]
    yf = np.fft.fft(values)
    N = len(values)
    if(N == 512):
        spacing = 256//32
        yff = 2.0/N * np.abs(yf[:N//2])
        yff = list(yff)     
        averaged = [np.max(yff[i:i+spacing]) for i in range(0,N//2,spacing)]
        for i in range(32):
            screen.column_height[i] = int(averaged[i])
    sleep(0.1)
    
    """
    # Number of sample points
    N = len(values)
    # sample spacing
    T = 10**(-4)
    xf = np.linspace(0.0, 1.0//(2.0*T), N//2)
    fig, ax = plt.subplots()
    yff = 2.0/N * np.abs(yf[:N//2])
    print(len(yff))
    ax.plot(xf, 2.0/N * np.abs(yf[:N//2]))
    plt.show()
    """
    
    
