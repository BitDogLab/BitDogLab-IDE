from machine import Pin, PWM

  # Seção 1: Preparação do NeoPixel
import neopixel

# Configuração inicial
NUM_LEDS = 25 # define que é uma matriz com 25 LEDs
ledsPIN = 7
np = neopixel.NeoPixel(Pin(ledsPIN), NUM_LEDS)

#define a posição dos LEDs na matriz da BotDogLab
LED_MATRIX = [
  [24, 23, 22, 21, 20],
  [15, 16, 17, 18, 19],
  [14, 13, 12, 11, 10],
  [5, 6, 7, 8, 9],
  [4, 3, 2, 1, 0]
]

def leds(ledsx, ledsy, ledsr=10, ledsg=10, ledsb=10):
  global np
  # os valores r=g=b=10 são assumidos por padrão se não forem atribuidos
  if 0 <= ledsx <= 4 and 0 <= ledsy <= 4:
    # verifica se os valores de x e y estão den6tro do range
    led_index = LED_MATRIX[4-ledsy][ledsx]
    np[led_index] = (ledsr, ledsg, ledsb)
    np.write()
  else:
    print("Invalid coordinates.")

class NeoPixelDesenhos:
  COLOR = (255, 255, 255)

  @staticmethod
  def apaga():
    # apaga a matriz de LEDs
    global np
    for i in range(25):
      np[i] = (0, 0, 0)
    np.write()

  @classmethod
  def coracao(self):
    posicao_x_y_LED_aceso = [(2, 0), (1, 1), (2, 1), (3, 1), (0, 2), (1, 2), (2, 2), (3, 2), (4, 2), (0, 3), (1, 3), (2, 3), (3, 3), (4, 3), (1, 4), (3, 4)]
    for x, y in posicao_x_y_LED_aceso:
      leds(x, y, *self.COLOR)  # Acende os LEDs nas posições especificadas com as cores fornecidas

  @classmethod
  def coracao_pequeno(self):
    posicao_x_y_LED_aceso = [(2, 1), (1, 2), (2, 2), (3, 2), (1, 3), (3, 3)]
    for x, y in posicao_x_y_LED_aceso:
      leds(x, y, *self.COLOR)  # Acende os LEDs nas posições especificadas com as cores fornecidas

  @classmethod
  def sorriso(self):
    posicao_x_y_LED_aceso = [(1, 0), (2, 0), (3, 0), (0, 1), (4, 1), (1, 3), (3, 3)]
    for x, y in posicao_x_y_LED_aceso:
      leds(x, y, *self.COLOR)  # Acende os LEDs nas posições especificadas com as cores fornecidas

  @classmethod
  def triste(self):
    posicao_x_y_LED_aceso =  [(0, 0), (4, 0), (1, 1), (2, 1), (3, 1), (1, 3), (3, 3)]
    for x, y in posicao_x_y_LED_aceso:
      leds(x, y, *self.COLOR)  # Acende os LEDs nas posições especificadas com as cores fornecidas

  @classmethod
  def X(self):
    posicao_x_y_LED_aceso =  [(0, 0), (4, 0), (1, 1), (3, 1), (2, 2), (1, 3), (3, 3), (0, 4), (4, 4)]
    for x, y in posicao_x_y_LED_aceso:
      leds(x, y, *self.COLOR)  # Acende os LEDs nas posições especificadas com as cores fornecidas

  @classmethod
  def x(self):
    posicao_x_y_LED_aceso =  [(1, 1), (3, 1), (2, 2), (1, 3), (3, 3)]
    for x, y in posicao_x_y_LED_aceso:
      leds(x, y, *self.COLOR)  # Acende os LEDs nas posições especificadas com as cores fornecidas

  @classmethod
  def girafa(self): 
    posicao_x_y_LED_aceso =  [(1, 0), (3, 0), (1, 1), (2, 1), (3, 1), (1, 2), (1, 3), (0, 4), (1, 4)]
    for x, y in posicao_x_y_LED_aceso:
      leds(x, y, *self.COLOR)  # Acende os LEDs nas posições especificadas com as cores fornecidas

NeoPixelDesenhos.apaga()

  # Fim da seção 1.
  # Seção 2: Preparação do LED RGB
PWM_ledR = PWM(Pin(12))
PWM_ledG = PWM(Pin(11))
PWM_ledB = PWM(Pin(13))
PWM_ledR.freq(500)
PWM_ledG.freq(500)
PWM_ledB.freq(500)

class LedRGB:
  COLOR = (0, 0, 0)
  LIGADO = True

  @classmethod
  def ligar(self):
    global PWM_ledR, PWM_ledG, PWM_ledB
    if not self.LIGADO:
      PWM_ledR.duty_u16(self.COLOR[0])
      PWM_ledG.duty_u16(self.COLOR[1])
      PWM_ledB.duty_u16(self.COLOR[2])
      self.LIGADO = True
  
  @classmethod
  def desligar(self):
    global PWM_ledR, PWM_ledG, PWM_ledB
    if self.LIGADO:
      PWM_ledR.duty_u16(0)
      PWM_ledG.duty_u16(0)
      PWM_ledB.duty_u16(0)
      self.LIGADO = False

  @classmethod
  def atualizar(self):
    global PWM_ledR, PWM_ledG, PWM_ledB
    if self.LIGADO:
      PWM_ledR.duty_u16(self.COLOR[0])
      PWM_ledG.duty_u16(self.COLOR[1])
      PWM_ledB.duty_u16(self.COLOR[2])

LedRGB.desligar()

  # Fim da seção 2.
  # Seção 3: Preparação dos buzzers A e B
PWM_buzzerA = PWM(Pin(4, Pin.OUT))
PWM_buzzerA.duty_u16(0)
PWM_buzzerA.freq(440)

PWM_buzzerB = PWM(Pin(21, Pin.OUT))
PWM_buzzerB.duty_u16(0)
PWM_buzzerB.freq(440)

class Buzzer:
  BUZZERS = [PWM_buzzerA, PWM_buzzerB]
  @classmethod
  def ligar(self, id: int):
    self.BUZZERS[id].duty_u16(self.VOLUMES[id])
  
  @classmethod
  def desligar(self, id: int):
    self.BUZZERS[id].duty_u16(0)

  @classmethod
  def trocar(self, id: int):
    if self.BUZZERS[id].duty_u16():
      self.desligar(id)
    else:
      self.ligar(id)
  
  @classmethod
  def definirNota(self, id: int, tone: int):
    self.BUZZERS[id].freq(tone)

Buzzer.desligar(0)
Buzzer.desligar(1)

  # Fim da seção 3.
  # Seção 4: Preparação do display OLED.

# NÃO IMPLEMENTADO

  # Fim da seção 4.
  # Seção 5: Preparação dos botões.

buttonA_pin = Pin(5, Pin.IN, Pin.PULL_UP)
buttonB_pin = Pin(6, Pin.IN, Pin.PULL_UP)

# Preparação das funções para interrupção.

class ButtonHandler:
  BUTTONS_IRQ = [lambda: None, lambda: None]
  BUTTONS_MODE = [0, 0] # 0 for toggle on press, 1 for on while holding
