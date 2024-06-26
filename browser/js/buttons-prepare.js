serial_setup_str = `\x03\r
import gc\r
from machine import Pin, PWM\r
gc.disable()\r
gc.collect()\r
import neopixel\r
\r
# Secao 1: NeoPixel\r
NUM_LEDS = 25 # define que é uma matriz com 25 LEDs\r
ledsPIN = 7\r
np = neopixel.NeoPixel(Pin(ledsPIN), NUM_LEDS)\r
LED_MATRIX = [\r
[24, 23, 22, 21, 20],\r
[15, 16, 17, 18, 19],\r
[14, 13, 12, 11, 10],\r
[5, 6, 7, 8, 9],\r
[4, 3, 2, 1, 0]\r
]\r
def leds(ledsx, ledsy, ledsr=10, ledsg=10, ledsb=10):\r
global np\r
if 0 <= ledsx <= 4 and 0 <= ledsy <= 4:\r
# verifica se os valores de x e y estão den6tro do range\r
led_index = LED_MATRIX[4-ledsy][ledsx]\r
np[led_index] = (ledsr, ledsg, ledsb)\r
np.write()\r\b
else:\r
print("Invalid coordinates.")\r\b\b
\r
class NeoPixelDesenhos:\r
COLOR = (255, 255, 255)\r
@staticmethod\r
def apaga():\r
# apaga a matriz de LEDs\r
global np\r
for i in range(25):\r
np[i] = (0, 0, 0)\r\b
np.write()\r\b
@classmethod\r
def coracao(self):\r
posicao_x_y_LED_aceso = [(2, 0), (1, 1), (2, 1), (3, 1), (0, 2), (1, 2), (2, 2), (3, 2), (4, 2), (0, 3), (1, 3), (2, 3), (3, 3), (4, 3), (1, 4), (3, 4)]\r
for x, y in posicao_x_y_LED_aceso:\r
leds(x, y, *self.COLOR) # Acende os LEDs nas posições especificadas com as cores fornecidas\r\b\b
@classmethod\r
def coracao_pequeno(self):\r
posicao_x_y_LED_aceso = [(2, 1), (1, 2), (2, 2), (3, 2), (1, 3), (3, 3)]\r
for x, y in posicao_x_y_LED_aceso:\r
leds(x, y, *self.COLOR) # Acende os LEDs nas posições especificadas com as cores fornecidas\r\b\b
@classmethod\r
def sorriso(self):\r
posicao_x_y_LED_aceso = [(1, 0), (2, 0), (3, 0), (0, 1), (4, 1), (1, 3), (3, 3)]\r
for x, y in posicao_x_y_LED_aceso:\r
leds(x, y, *self.COLOR) # Acende os LEDs nas posições especificadas com as cores fornecidas\r\b\b
@classmethod\r
def triste(self):\r
posicao_x_y_LED_aceso = [(0, 0), (4, 0), (1, 1), (2, 1), (3, 1), (1, 3), (3, 3)]\r
for x, y in posicao_x_y_LED_aceso:\r
leds(x, y, *self.COLOR) # Acende os LEDs nas posições especificadas com as cores fornecidas\r\b\b
@classmethod\r
def X(self):\r
posicao_x_y_LED_aceso = [(0, 0), (4, 0), (1, 1), (3, 1), (2, 2), (1, 3), (3, 3), (0, 4), (4, 4)]\r
for x, y in posicao_x_y_LED_aceso:\r
leds(x, y, *self.COLOR) # Acende os LEDs nas posições especificadas com as cores fornecidas\r\b\b
@classmethod\r
def x(self):\r
posicao_x_y_LED_aceso = [(1, 1), (3, 1), (2, 2), (1, 3), (3, 3)]\r
for x, y in posicao_x_y_LED_aceso:\r
leds(x, y, *self.COLOR) # Acende os LEDs nas posições especificadas com as cores fornecidas\r\b\b
@classmethod\r
def girafa(self):\r
posicao_x_y_LED_aceso = [(1, 0), (3, 0), (1, 1), (2, 1), (3, 1), (1, 2), (1, 3), (0, 4), (1, 4)]\r
for x, y in posicao_x_y_LED_aceso:\r
leds(x, y, *self.COLOR) # Acende os LEDs nas posições especificadas com as cores fornecidas\r\b\b\b
\r
NeoPixelDesenhos.apaga()\r
\r
# Fim da secao 1.\r
gc.collect()\r
\r
# Secao 2: Preparação do LED RGB\r
PWM_ledR = PWM(Pin(12))\r
PWM_ledG = PWM(Pin(11))\r
PWM_ledB = PWM(Pin(13))\r
PWM_ledR.freq(500)\r
PWM_ledG.freq(500)\r
PWM_ledB.freq(500)\r
class LedRGB:\r
COLOR = (0, 0, 0)\r
LIGADO = True\r
@classmethod\r
def ligar(self):\r
global PWM_ledR, PWM_ledG, PWM_ledB\r
if not self.LIGADO:\r
PWM_ledR.duty_u16(self.COLOR[0])\r
PWM_ledG.duty_u16(self.COLOR[1])\r
PWM_ledB.duty_u16(self.COLOR[2])\r
self.LIGADO = True\r\b\b
@classmethod\r
def desligar(self):\r
global PWM_ledR, PWM_ledG, PWM_ledB\r
if self.LIGADO:\r
PWM_ledR.duty_u16(0)\r
PWM_ledG.duty_u16(0)\r
PWM_ledB.duty_u16(0)\r
self.LIGADO = False\r\b\b
@classmethod\r
def atualizar(self):\r
global PWM_ledR, PWM_ledG, PWM_ledB\r
if self.LIGADO:\r
PWM_ledR.duty_u16(self.COLOR[0])\r
PWM_ledG.duty_u16(self.COLOR[1])\r
PWM_ledB.duty_u16(self.COLOR[2])\r\b\b\b
\r
LedRGB.desligar()\r
\r
# Fim da secao 2.\r
gc.collect()\r
\r
# Secao 3: Preparação dos buzzers A e B\r
PWM_buzzerA = PWM(Pin(8, Pin.OUT))\r
PWM_buzzerA.duty_u16(0)\r
PWM_buzzerA.freq(440)\r
PWM_buzzerB = PWM(Pin(21, Pin.OUT))\r
PWM_buzzerB.duty_u16(0)\r
PWM_buzzerB.freq(440)\r
class Buzzer:\r
BUZZERS = [PWM_buzzerA, PWM_buzzerB]\r
VOLUMES = [0, 0]\r
@classmethod\r
def ligar(self, id: int):\r
self.BUZZERS[id].duty_u16(self.VOLUMES[id])\r\b
@classmethod\r
def desligar(self, id: int):\r
self.BUZZERS[id].duty_u16(0)\r\b
@classmethod\r
def atualizar(self, id: int):\r
if self.BUZZERS[id].duty_u16() > 0:\r
self.BUZZERS[id].duty_u16(self.VOLUMES[id])\r\b\b
@classmethod\r
def definirNota(self, id: int, tone: int):\r
self.BUZZERS[id].freq(tone)\r\b\b
\r
Buzzer.desligar(0)\r
Buzzer.desligar(1)\r
\r
# Fim da seção 3.\r
gc.collect()\r
\r
# Seção 4: Preparação do display OLED.\r
# NÃO IMPLEMENTADO\r
# Fim da seção 4.\r
gc.collect()\r
# Seção 5: Preparação dos botões.\r
buttonA_pin = Pin(5, Pin.IN, Pin.PULL_UP)\r
buttonB_pin = Pin(6, Pin.IN, Pin.PULL_UP)\r
# Preparação das funções para interrupção.\r
class ButtonHandler:\r
BUTTONS_FALLING_IRQ = [lambda: None, lambda: None] # When button is pressed.\r
BUTTONS_RISING_IRQ = [lambda: None, lambda: None] # When button is released.\r
BUTTONS_MODE = [0, 0] # 0 for toggle on press, 1 for on while holding\r
BUTTONS_STATE = [False, False] # Used on mode 0 (toggle on press). Is True when button is "toggled".\r
@classmethod\r
def buttonA_irq(self, pin):\r
flags = pin.irq().flags()\r
is_falling = flags & Pin.IRQ_FALLING\r
is_rising = flags & Pin.IRQ_RISING\r
if is_falling and self.BUTTONS_MODE[0] == 0:\r
if self.BUTTONS_STATE[0]:\r
self.BUTTONS_RISING_IRQ[0]()\r\b
else:\r
self.BUTTONS_FALLING_IRQ[0]()\r\b
self.BUTTONS_STATE[0] = not self.BUTTONS_STATE[0]\r\b
elif is_falling and self.BUTTONS_MODE[0] == 1:\r
self.BUTTONS_FALLING_IRQ[0]()\r\b
elif is_rising and self.BUTTONS_MODE[0] == 1:\r
self.BUTTONS_RISING_IRQ[0]()\r\b\b
\r
@classmethod\r
def buttonB_irq(self, pin):\r
flags = pin.irq().flags()\r
is_falling = flags & Pin.IRQ_FALLING\r
is_rising = flags & Pin.IRQ_RISING\r
if is_falling and self.BUTTONS_MODE[1] == 0:\r
if self.BUTTONS_STATE[1]:\r
self.BUTTONS_RISING_IRQ[1]()\r\b
else:\r
self.BUTTONS_FALLING_IRQ[1]()\r\b
self.BUTTONS_STATE[1] = not self.BUTTONS_STATE[1]\r\b
elif is_falling and self.BUTTONS_MODE[1] == 1:\r
self.BUTTONS_FALLING_IRQ[1]()\r\b
elif is_rising and self.BUTTONS_MODE[1] == 1:\r
self.BUTTONS_RISING_IRQ[1]()\r\b\b\b
\r
buttonA_pin.irq(trigger=(Pin.IRQ_FALLING | Pin.IRQ_RISING), handler=ButtonHandler.buttonA_irq)\r
buttonB_pin.irq(trigger=(Pin.IRQ_FALLING | Pin.IRQ_RISING), handler=ButtonHandler.buttonB_irq)\r
gc.collect()\r
gc.enable()\r`