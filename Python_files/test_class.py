from LED_control import LED
from time import sleep
from random import randint

test = LED(bar_data_length=32)
sleep(2)

while True:
    for i in range(test.bar_data_length):
        test.column_height[i] = randint(1,15)
        test.column_color[i] = randint(0,3)
    test.send()
    sleep(0.05)
