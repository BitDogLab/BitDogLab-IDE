from machine import Pin
import neopixel

np = neopixel.NeoPixel(Pin(7), 25)
np_queue = []

def resetLEDs():
  global np, np_queue
  for i in range(25):
    np[i] = (0, 0, 0)
  np.write()
  np_queue.clear()

def setLED(pos: tuple[int, int], color: tuple[int, int, int]):
  global np_queue
  y = pos[1]
  x = (4 - pos[0]) if y%2==1 else pos[0]
  np_queue.append((5*y + x, color))

def updateLEDs():
  global np, np_queue
  while len(np_queue) > 0:
    i, color = np_queue.pop(0)
    np[i] = color
  np.write()