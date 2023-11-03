from machine import Pin, SoftI2C, ADC
import neopixel
import time
from ssd1306 import SSD1306_I2C

def atualizar_matriz(temporizador, tempo_inicio):
    tempo_restante = temporizador - time.time()
    tempo_transcorrido = time.time() - tempo_inicio
    percentual_restante = tempo_restante / (temporizador - tempo_inicio) if tempo_inicio != temporizador else 1

    linhas_a_desligar = int((1 - percentual_restante) * 5)
    index = 0
    for i in range(5):
        for j in range(5):
            if i < linhas_a_desligar:
                np[index] = (0, 0, 0)
            else:
                np[index] = (0, 50, 100)
            index += 1

    if time.time() >= temporizador:
        np[12] = (100, 0, 0)
    
    np.write()

    oled.fill(0)
    oled.text('Tempo:', 30, 0)
    oled.text(str(int(tempo_transcorrido)) + ' s', 45, 30)
    oled.show()

# Configurações
NUM_LEDS = 25
tempo_inicio = 0
temporizador = 0
tempo_ligado = 10

i2c = SoftI2C(scl=Pin(15), sda=Pin(14))
oled = SSD1306_I2C(128, 64, i2c)
np = neopixel.NeoPixel(Pin(7), NUM_LEDS)

rele = Pin(0, Pin.OUT)
button_a = Pin(5, Pin.IN, Pin.PULL_UP)
button_b = Pin(6, Pin.IN, Pin.PULL_UP)

red_led = Pin(12, Pin.OUT)
green_led = Pin(13, Pin.OUT)
blue_led = Pin(11, Pin.OUT)

joystick_x = ADC(Pin(27))
joystick_y = ADC(Pin(26))

joystick_button = Pin(22, Pin.IN, Pin.PULL_UP)

oled.fill(0)
oled.show()
for i in range(NUM_LEDS):
    np[i] = (0, 0, 0)
np.write()

while True:
    if button_a.value() == 0:
        red_led.value(1)
        green_led.value(0)
        blue_led.value(0)
        if temporizador != 0:
            print("Desligando o relé pela ação do Botão A")
            rele.value(0)
            temporizador = 0

    elif button_b.value() == 0:
        red_led.value(0)
        green_led.value(0)
        blue_led.value(1)
        if temporizador == 0:
            print("Ligando o relé pela ação do Botão B")
            rele.value(1)
            tempo_inicio = time.time()
            temporizador = time.time() + tempo_ligado

    if temporizador != 0:
        atualizar_matriz(temporizador, tempo_inicio)

    if time.time() >= temporizador and temporizador != 0:
        valor_joystick_x = joystick_x.read_u16()
        print(f"Valor Joystick X: {valor_joystick_x}")

        if valor_joystick_x < 1000 * 64:
            tempo_ligado = max(1, tempo_ligado - 1)
        elif valor_joystick_x > 3000 * 64:
            tempo_ligado += 1

        oled.fill(0)
        oled.text('Tempo Ligado:', 10, 0)
        oled.text(str(tempo_ligado) + ' s', 30, 30)
        oled.show()

        print("Tempo esgotado, desligando relé.")
        rele.value(0)
        temporizador = 0

    time.sleep(0.1)
