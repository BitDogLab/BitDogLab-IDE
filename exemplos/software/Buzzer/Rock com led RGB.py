# programa funcional

from machine import Pin, PWM
import time

# Conecte o alto-falante ou buzzer passivo ao pino GP4
alto_falante = PWM(Pin(4))

# Conecte o LED RGB aos pinos GP13, GP12 e GP14
led_red = PWM(Pin(13))
led_green = PWM(Pin(12))
led_blue = PWM(Pin(14))

# Frequências das notas musicais
# Frequências das notas musicais
notas = {
    'C4': {'freq': 261, 'cor': (255, 0, 0)},
    'D4': {'freq': 294, 'cor': (255, 127, 0)},
    'E4': {'freq': 329, 'cor': (255, 255, 0)},
    'F4': {'freq': 349, 'cor': (0, 255, 0)},
    'G4': {'freq': 392, 'cor': (0, 0, 255)},
    'A4': {'freq': 440, 'cor': (75, 0, 130)},
    'B4': {'freq': 494, 'cor': (143, 0, 255)},
    'C5': {'freq': 523, 'cor': (255, 0, 255)},
    'PAUSA': {'freq': 0, 'cor': (0, 0, 0)},
    'G': {'freq': 196, 'cor': (255, 0, 0)},
    'A': {'freq': 220, 'cor': (255, 127, 0)},
    'B': {'freq': 246, 'cor': (255, 255, 0)},
    'C': {'freq': 261, 'cor': (0, 255, 0)},
    'D': {'freq': 294, 'cor': (0, 0, 255)},
    'E': {'freq': 329, 'cor': (75, 0, 130)}
}


# Música "Smoke on the Water" do Deep Purple
musica = [
    ('E', 2), ('PAUSA', 1), ('E', 2), ('PAUSA', 1), ('E', 2), ('PAUSA', 1), ('G', 2),
    ('PAUSA', 1), ('G', 2), ('PAUSA', 1), ('G', 2), ('PAUSA', 1), ('A', 2),
    ('PAUSA', 1), ('A', 2), ('PAUSA', 1), ('A', 2), ('PAUSA', 1), ('PAUSA', 2),
    ('D', 2), ('PAUSA', 1), ('D', 2), ('PAUSA', 1), ('D', 2), ('PAUSA', 1), ('C', 2),
    ('PAUSA', 1), ('C', 2), ('PAUSA', 1), ('C', 2), ('PAUSA', 1), ('PAUSA', 2),
    ('E', 2), ('PAUSA', 1), ('E', 2), ('PAUSA', 1), ('E', 2), ('PAUSA', 1), ('G', 2),
    ('PAUSA', 1), ('G', 2), ('PAUSA', 1), ('G', 2), ('PAUSA', 1), ('A', 2),
    ('PAUSA', 1), ('A', 2), ('PAUSA', 1), ('A', 2), ('PAUSA', 1), ('PAUSA', 2),
    ('C', 2), ('PAUSA', 1), ('C', 2), ('PAUSA', 1), ('D', 2), ('PAUSA', 1), ('D', 2),
    ('PAUSA', 1), ('E', 2), ('PAUSA', 1), ('E', 2), ('PAUSA', 1), ('PAUSA', 4)
]


def tocar_musica():
    for nota, duracao in musica:
        freq = notas[nota]['freq']
        cor = notas[nota]['cor']
        if freq > 0:
            alto_falante.freq(freq)
            alto_falante.duty_u16(32768)
        else:
            alto_falante.duty_u16(0)
        led_red.duty_u16(cor[0]*254)
        led_green.duty_u16(cor[1]*254)
        led_blue.duty_u16(cor[2]*254)
        time.sleep_ms(40 * duracao)
        alto_falante.duty_u16(0)
        led_red.duty_u16(0)
        led_green.duty_u16(0)
        led_blue.duty_u16(0)
        time.sleep_ms(70)
        
        # esse comando mostra o valor do Duth Cycle do LED RGB
        print(cor[0]*254)
        print(cor[1]*254)
        print(cor[2]*254)  
        print()



while True:
    tocar_musica()
    time.sleep(5)

