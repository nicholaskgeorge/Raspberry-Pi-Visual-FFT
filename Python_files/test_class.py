from LED_control import LED
from time import sleep

test = LED()
test.column_height[0] = 6
test.column_height[4] = 12
sleep(2)
test.send()
