from machine import Pin, PWM

pinR = Pin(12)
pinG = Pin(11)
pinB = Pin(13)

pwmR = PWM(pinR)
pwmG = PWM(pinG)
pwmB = PWM(pinB)

pwmR.freq(500)
pwmG.freq(500)
pwmB.freq(500)
pwmR.duty_u16(0)
pwmG.duty_u16(0)
pwmB.duty_u16(0)

def setColor(r: int, g: int, b: int):
  global pwmR, pwmG, pwmB
  pwmR.duty_u16(r)
  pwmG.duty_u16(g)
  pwmB.duty_u16(b)