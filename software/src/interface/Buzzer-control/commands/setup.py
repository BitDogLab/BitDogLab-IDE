from machine import Pin, PWM

buzzerA_pin = Pin(4, Pin.OUT)
buzzerA_pwm = PWM(buzzerA_pin)
buzzerA_pwm.duty_u16(0)
buzzerB_pin = Pin(21, Pin.OUT)
buzzerB_pwm = PWM(buzzerB_pin)
buzzerB_pwm.duty_u16(0)