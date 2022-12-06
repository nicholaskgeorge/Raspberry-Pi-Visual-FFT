import serial
from time import sleep
import numpy as np
from LED_control import LED

ser = serial.Serial('/dev/ttyUSB0', 115200);
screen = LED(bar_data_length=32, middle_mode=0)
display_mode = "1 max"
filtering = True
screen.start()
while True:
    values = ser.readline().decode('ascii')
    values = values.split(",")[1:-1]
    #print(values)
    values = [int(i) for i in values if i != ""]
    yf = np.fft.fft(values)
    N = len(values)
    #print(N)
    if(N == 64):
        #division by 2 due to FFT shift
        yff = (1.0/N * np.abs(yf[:N//2]))
        if filtering == True:
            yff = np.array([i if i>2 else 0 for i in list(yff)])
        if display_mode == "1 max":
            index = yff[1:].argmax()
            yff = list(yff)
            print(yff[0])
            for i in range(32):
                if i==index+1:
                    screen.column_color[i] = 2
                else:
                    screen.column_color[i] = 0
                screen.column_height[i] = int(yff[i])
        elif display_mode == "3 max":
            for i in range(32):
                screen.column_height[i] = int(yff[i])
                screen.column_color[i] = 0
            find_max = yff[1:]
            for i in range(3):
                index = find_max.argmax()
                screen.column_color[index+1] = i+1
                find_max[index] = -1
        else:
            quit()
        #print(f"Max freq is {(index+1)*(10000/64)}")
        
    #sleep(0.1)
    
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
    
    
