import sys

class BaseComponent:
  @staticmethod
  def out(msg):
    sys.stdout.write(msg)

  @staticmethod
  def err(msg):
    sys.stderr.write(msg)