# Desligar NeoPixel.
NeoPixelDesenhos.apaga()

# Desligar LED RGB.
LedRGB.definirCor(0, 0, 0)

# Desligar buzzers.
Buzzer.desligar(0)
Buzzer.desligar(1)

# Desligar display OLED.
# NÃO IMPLEMENTADO

# Reiniciar Pico.
from machine import reset
reset()