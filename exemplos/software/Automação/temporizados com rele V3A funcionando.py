from machine import Pin, SoftI2C, ADC, PWM
import neopixel
import time
from ssd1306 import SSD1306_I2C

# Configurações iniciais
NUM_LEDS = 25
tempo_inicio = 0
temporizador = 0
tempo_ligado = 120  # tempo padrão de 120 segundos
i2c = SoftI2C(scl=Pin(15), sda=Pin(14))
oled = SSD1306_I2C(128, 64, i2c)
np = neopixel.NeoPixel(Pin(7), NUM_LEDS)
rele = Pin(0, Pin.OUT)
button_b = Pin(6, Pin.IN, Pin.PULL_UP)

adc_vry = ADC(Pin(27))  # Configurando o ADC para o pino VRy do joystick

red_led = Pin(12, Pin.OUT)
green_led = Pin(13, Pin.OUT)
blue_led = Pin(11, Pin.OUT)

def atualizar_matriz(temporizador, tempo_inicio):
    tempo_restante = temporizador - time.time()
    tempo_transcorrido = time.time() - tempo_inicio
    
    total_tempo = temporizador - tempo_inicio
    percentual_restante = tempo_restante / total_tempo

    leds_a_acender = int((1 - percentual_restante) * 25)

    for i in range(25):
        if i < leds_a_acender:
            np[i] = (0, 50, 100)
        else:
            np[i] = (0, 0, 0)

    np.write()

    oled.fill(0)
    oled.text('Tempo:', 30, 0)
    oled.text(str(int(tempo_transcorrido)) + 's/' + str(int(total_tempo)) + 's', 20, 30)
    oled.show()

# Mostrar tempo total inicial no OLED
oled.fill(0)
oled.text('Tempo total:', 0, 0)
oled.text(str(tempo_ligado) + 's', 0, 30)
oled.show()

while True:
    # Ler o valor analógico de VRy
    vry_value = adc_vry.read_u16()
    
    if vry_value < 10922:  # Menor que 0.5V
        tempo_ligado -= 30
    elif vry_value > 54613:  # Maior que 2.5V
        tempo_ligado += 30

    tempo_ligado = max(30, min(600, tempo_ligado))  #  limitando o tempo entre 30s e 600s

    # Atualizar tempo total no OLED
    oled.fill(0)
    oled.text('Tempo total:', 0, 0)
    oled.text(str(tempo_ligado) + 's', 0, 30)
    oled.show()

    if temporizador == 0:
        blue_led.value(1)
        red_led.value(0)
        if button_b.value() == 0:
            red_led.value(1)
            blue_led.value(0)
            rele.value(1)
            tempo_inicio = time.time()
            temporizador = time.time() + tempo_ligado
            time.sleep(0.5)  # Debouncing

    if temporizador != 0:
        atualizar_matriz(temporizador, tempo_inicio)
        if time.time() >= temporizador:
            rele.value(0)
            temporizador = 0
            red_led.value(0)
            blue_led.value(1)

    time.sleep(0.1)

