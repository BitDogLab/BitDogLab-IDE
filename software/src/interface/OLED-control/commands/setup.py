from machine import Pin, SoftI2C
from ssd1306 import SSD1306_I2C

i2c = SoftI2C(scl=Pin(15), sda=Pin(14))
oled = SSD1306_I2C(128, 64, i2c)

def sendStringToOLED(lines: list[str]):
  oled.fill(0)
  for i, line in enumerate(lines):
    oled.text(line, 0, 16*i)
  oled.show()

oled.fill(0)
oled.show()