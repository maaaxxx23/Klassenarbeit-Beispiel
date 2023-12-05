import time
from machine import Pin, I2C

import ahtx0

# I2C for the Wemos D1 Mini with ESP8266
i2c = I2C(scl=Pin(9), sda=Pin(8))

# Create the sensor object using I2C
sensor = ahtx0.AHT10(i2c)

while True:
    print("\nTemperature: %0.2f C" % sensor.temperature)
    print("Humidity: %0.2f %%" % sensor.relative_humidity)
    time.sleep(5)