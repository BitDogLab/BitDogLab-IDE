from machine import Pin, SoftI2C, ADC, PWM
import neopixel
import time
from ssd1306 import SSD1306_I2C

def atualizar_matriz(tempo_ligado, tempo_transcorrido):
    percentual_concluido = tempo_transcorrido / tempo_ligado
    
    # Acende LEDs da matriz como uma ampulheta invertida
    for i in range(NUM_LEDS):
        if i <= int(NUM_LEDS * percentual_concluido):
            np[i] = (0, 50, 100)  # Azul
        else:
            np[i] = (0, 0, 0)  # Desligado
    np.write()
    
def beep_agudo():
    buzzer.duty_u16(10000)
    buzzer.freq(4000)
    time.sleep(0.1)
    buzzer.duty_u16(0)

def beep_grave():
    buzzer.duty_u16(10000)
    buzzer.freq(1000)
    time.sleep(0.1)
    buzzer.duty_u16(0)


# Configurações iniciais
NUM_LEDS = 25
tempo_ligado = 120  # Inicialmente definido para 120s
i2c = SoftI2C(scl=Pin(15), sda=Pin(14))
oled = SSD1306_I2C(128, 64, i2c)
np = neopixel.NeoPixel(Pin(7), NUM_LEDS)
rele = Pin(0, Pin.OUT)
button_a = Pin(5, Pin.IN, Pin.PULL_UP)
button_b = Pin(6, Pin.IN, Pin.PULL_UP)
red_led = Pin(12, Pin.OUT)
green_led = Pin(13, Pin.OUT)
blue_led = Pin(11, Pin.OUT)

joystick_y = ADC(Pin(27))

buzzer = PWM(Pin(21))  # Supondo que o pino 16 está conectado ao buzzer
buzzer.duty_u16(0)  # Inicialmente desligado


tempo_inicio = 0

while True:
    # Atualizar o OLED para mostrar o tempo_ligado e tempo_transcorrido
    oled.fill(0)
    oled.text('Tempo Total: {}s'.format(tempo_ligado), 0, 0)
    
    if tempo_inicio != 0:
        tempo_transcorrido = int(time.time() - tempo_inicio)
        oled.text('Tempo: {}s'.format(tempo_transcorrido), 0, 30)
    oled.show()
    
    valor_joystick_y = joystick_y.read_u16()

    if valor_joystick_y > 50000:  # Mais de 2.5V
        tempo_ligado = min(600, tempo_ligado + 30)
    elif valor_joystick_y < 10000:  # Menos de 0.5V
        tempo_ligado = max(30, tempo_ligado - 30)

    if button_b.value() == 0 and tempo_inicio == 0:
        beep_grave()  # Toca um beep grave
        tempo_inicio = time.time()
        red_led.value(1)
        green_led.value(0)
        blue_led.value(0)
    
    if button_a.value() == 0:
        beep_agudo()  # Toca um beep agudo
        rele.value(0)
        tempo_inicio = 0
        green_led.value(1)
        red_led.value(0)
        blue_led.value(0)
        
        # Apaga todos os LEDs da matriz
        for i in range(NUM_LEDS):
            np[i] = (0, 0, 0)
        np.write()

    if tempo_inicio != 0:
        tempo_transcorrido = time.time() - tempo_inicio

        if tempo_transcorrido < tempo_ligado:
            atualizar_matriz(tempo_ligado, tempo_transcorrido)
            rele.value(1)
        else:
            rele.value(0)
            tempo_inicio = 0
            blue_led.value(1)
            green_led.value(0)
            red_led.value(0)
            
            # Apaga todos os LEDs da matriz quando a contagem termina
            for i in range(NUM_LEDS):
                np[i] = (0, 0, 0)
            np.write()

    time.sleep(0.1)

