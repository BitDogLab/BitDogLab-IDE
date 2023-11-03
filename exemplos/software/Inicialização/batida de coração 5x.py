from machine import PWM, Pin
import neopixel
import time

# Configuração do NeoPixel
NUM_LEDS = 25
np = neopixel.NeoPixel(Pin(7), NUM_LEDS)

# Configuração do Buzzer
buzzer = PWM(Pin(21))
buzzer_freq = 1000  # Frequência para o beep

def beep(duration=0.2):
    ''' Toca um beep com a duração especificada '''
    buzzer.freq(buzzer_freq)
    buzzer.duty_u16(5000)  # Intensidade média
    time.sleep(duration)
    buzzer.duty_u16(0)  # Desliga o buzzer

def dim_leds(led_sequence, current_index):
    # Define o fator de diminuição de intensidade baseado no índice atual do LED
    dim_factor = 255 // (len(led_sequence) - current_index)
    for idx, led in enumerate(led_sequence):
        if idx < current_index:
            r, g, b = np[led]
            r = max(r - dim_factor, 0)
            np[led] = (r, g, b)

def turn_off_all_leds():
    ''' Desliga todos os LEDs '''
    for i in range(NUM_LEDS):
        np[i] = (0, 0, 0)
    np.write()

def heartbeat_effect():
    # Sequência de LEDs para simular o pulso cardíaco
    sequence = [14, 6, 12, 21, 10]
    
    initial_delay = 0.3  # tempo inicial entre LEDs
    decrement = 0.05  # valor a ser decrementado a cada LED
    
    # Limpa todos os LEDs
    turn_off_all_leds()

    for idx, led in enumerate(sequence):
        np[led] = (255, 0, 0)  # Acende o LED vermelho
        dim_leds(sequence, idx)  # Diminui o brilho dos LEDs na sequência
        np.write()
        time.sleep(initial_delay - idx * decrement)
        
    # Toca o beep no buzzer
    beep()
    
    # Aguarda um pouco e depois desliga todos os LEDs
    time.sleep(0.5)
    turn_off_all_leds()

# Especifica o número de repetições desejado
num_repetitions = 5
for _ in range(num_repetitions):
    heartbeat_effect()

