import spidev
import time

spi = spidev.SpiDev()
spi.open(0, 0)
spi.open(0, 1)
spi.max_speed_hz = 7629


# Repeatedly switch a MCP4151 digital pot off then on
while True:
    spi.xfer([1, 0])

