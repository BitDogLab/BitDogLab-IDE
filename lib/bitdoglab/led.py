import sys
from machine import Pin, PWM
from time import sleep_ms
from .base.base import BaseComponent
from .exceptions.common import IllegalArgumentsError

class Led(BaseComponent):
  """RGB LED control class.
  
  Methods:
    limpar(): Turns off the RGB LED by making all pulse wave lengths 0.
    cor(*args): Controls the color of the RGB LED.
  """

  # Declaração de variáveis dos pinos e dicionário de cores.
  __pin_R = PWM(Pin(12), freq=500)
  __pin_G = PWM(Pin(11), freq=500)
  __pin_B = PWM(Pin(13), freq=500)
  __CORES = {
    "vermelho": (65535, 0, 0),
    "verde": (0, 65535, 0),
    "azul": (0, 0, 65535),
    "ciano": (0, 65535, 65535),
    "rosa": (65535, 0, 65535),
    "amarelo": (65535, 65535, 0),
    "branco": (65535, 65535, 65535)
  }
  
  @classmethod
  def limpar(cls):
    """Turns off the RGB LED by making all pulse wave lengths 0."""
    cls.__pin_R.duty_u16(0)
    cls.__pin_G.duty_u16(0)
    cls.__pin_B.duty_u16(0)
  
  @classmethod
  def cor(cls, *args: str | tuple[tuple[int, int, int] | list[int]] | tuple[int, int, int]):
    """Controls the color of the RGB LED. 

    This function accepts arguments in three distinct formats:
    1. String with desired color name
    2. Tuple/list of 3 ints representing 48-bit RGB color code
    3. 3 ints representing 48-bit RGB color code.
    If arguments don't match any of the options listed, the function raises IllegalArgumentsError.
    
    Args:
      *args: Variable length argument list. Must match one of three options listed above.

    Returns:
      None

    Raises:
      IllegalArgumentsError
      
    """
    if len(args) == 1 and isinstance(args[0], str):
      rgb = cls.__CORES[args[0]]
      cls.__pin_R.duty_u16(rgb[0])
      cls.__pin_G.duty_u16(rgb[1])
      cls.__pin_B.duty_u16(rgb[2])
    elif len(args) == 1 and isinstance(args[0], (list, tuple)) and len(args[0]) == 3:
      cls.__pin_R.duty_u16(args[0][0])
      cls.__pin_G.duty_u16(args[0][1])
      cls.__pin_B.duty_u16(args[0][2])
    elif len(args) == 3 and isinstance(args[0], int) and isinstance(args[1], int) and isinstance(args[2], int):
      cls.__pin_R.duty_u16(args[0])
      cls.__pin_G.duty_u16(args[1])
      cls.__pin_B.duty_u16(args[2])
    else:
      import traceback
      tb = sys.exc_info()[-1]
      stk = traceback.extrack_tb(tb, 1)
      fname = stk[0][2]
      raise IllegalArgumentsError("Function \"", fname, "\" accepts string, tuple/list of 3 ints, or 3 ints. Illegal arguments \"", *args, "\" were used instead.")

def demo():
  """Demonstration of Led class methods."""
  Led.limpar()
  sleep_ms(1000)
  Led.cor("vermelho")
  sleep_ms(500)
  Led.cor("verde")
  sleep_ms(500)
  Led.cor("azul")
  sleep_ms(500)
  Led.cor("branco")
  sleep_ms(1000)
  Led.limpar()
