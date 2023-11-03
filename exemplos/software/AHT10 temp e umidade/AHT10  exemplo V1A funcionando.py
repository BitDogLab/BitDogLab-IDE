import utime
from machine import Pin, SoftI2C
import ahtx0

# Configuração de I2C para a Raspberry Pi Pico na BitDogLab
# SDA está conectado ao GPIO2 e SCL ao GPIO3, conforme descrito em I2C 1.
i2c1 = SoftI2C(scl=Pin(3), sda=Pin(2))

# Crie o objeto do sensor usando I2C
sensor = ahtx0.AHT10(i2c1)  # Vamos supor que a classe seja AHT10.

while True:
    print("\nTemperature: {:.2f} C".format(sensor.temperature))
    print("Humidity: {:.2f} %".format(sensor.relative_humidity))
    utime.sleep(5)
