# mpremote-terminal

This program emulates a terminal and establishes serial communication with a Raspberry Pi Pico board connected via USB to the computer.

As of current, the available commands are:
```
connect list - Lists all available connections.
connect auto - Connects to available port.
disconnect - Disconnects
eval [expression] - When connected, sends expression for board to evaluate and prints return value to terminal. When not connected, shows error message.
```