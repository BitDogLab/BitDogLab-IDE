from machine import Pin, SoftI2C
import ahtx0
from ssd1306 import SSD1306_I2C
import time
import neopixel

# Configuração OLED
i2c_oled = SoftI2C(scl=Pin(15), sda=Pin(14))
oled = SSD1306_I2C(128, 64, i2c_oled)

# Número de LEDs na sua matriz 5x5
NUM_LEDS = 25

# Inicializar a matriz de NeoPixels no GPIO7
np = neopixel.NeoPixel(Pin(7), NUM_LEDS)

# Configuração Sensor AHT10/AHT20
i2c_sensor = SoftI2C(scl=Pin(3), sda=Pin(2))
sensor = ahtx0.AHT10(i2c_sensor)

# Função para apagar todos os LEDs
def clear_matrix():
    for i in range(NUM_LEDS):
        np[i] = (0, 0, 0)
    np.write()

while True:
    # Executa a função para apagar todos os LEDs
    clear_matrix()

    # Ler dados do sensor
    temp = sensor.temperature
    humidity = sensor.relative_humidity

    # Limpar display
    oled.fill(0)

    # Exibir dados no OLED
    oled.text('Temp.: {:.2f}C'.format(temp), 0, 0)
    oled.text('Humidity: {:.2f}%'.format(humidity), 0, 30)

    # Atualizar display
    oled.show()

    # Aguardar antes de atualizar novamente
    time.sleep(1)

