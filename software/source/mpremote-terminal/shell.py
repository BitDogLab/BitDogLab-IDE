import os, sys
import serial
import serial.tools.list_ports

from .commands import *

class State:
    def __init__(self):
        self.connected = False
        self.serial = None
        self.buf = ""

        import serial

    def connect(self, port, baudrate):
        try:
            self.serial = serial.Serial(port, baudrate)
        except Exception as err:
            raise err
            return
        self.connected = True

    def hasBuf(self):
        return len(self.buf) > 0
    
    def appendToBuf(self, line: str, end: str = '\n'):
        self.buf += line + end

    def readBufLines(self):
        lines = self.buf.split('\n')
        print(lines)
        if len(lines[-1]) == 0:
            lines.pop()
        self.buf = ""
        return lines

COMMANDS = {
    "connect": do_connect,
    "disconnect": do_disconnect,
    "eval": do_eval
}

state = State()

def _runCommand(state, command):
    global COMMANDS

    command_split = command.split()
    print(command_split)
    keyword = command_split[0]

    # Verify if command is valid. return None if not.
    try:
        command_func = COMMANDS[keyword]
    except KeyError:
        state.appendToBuf(f"Error: '{keyword}' is not a valid command")
        return
    
    # Verify if sufficient arguments. return None if not.
    try:
        command_func(state, *command_split[1:])
        return
    except IndexError as err:
        state.appendToBuf("Error: insufficient arguments")
        raise err
        return

if __name__=="__main__":
    while True:
        command_split = input("\r\n>>> ").split()
        keyword = command_split[0]
        
        if keyword == "exit":
            print("Exiting program...\n")
            break

        # Verify if command is valid. Warn and ignore if not.
        try:
            command_func = COMMANDS[keyword]
        except KeyError:
            print(f"Error: '{keyword}' is not a valid command")
            continue

        # Verify if sufficient arguments. Warn and ignore if not.
        try:
            command_func(state, *command_split[1:])
        except IndexError:
            print("Error: insufficient arguments")
            continue

        # Print output.
        if state.serial is not None:
            while state.serial.readable():
                line = state.serial.readline()
                print(line)